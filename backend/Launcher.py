# --- Imports ---
import RPi.GPIO as GPIO
import time
from adafruit_servokit import ServoKit  # Controls the PCA9685 servo board (for jitter-free servo motion)

# --- Flywheel TB6612FNG (Board 1, using your existing GPIO pins) ---
AIN1 = 17          # Left flywheel motor direction pin 1
AIN2 = 27          # Left flywheel motor direction pin 2
PWMA = 22          # Left flywheel motor PWM pin (speed control)

BIN1 = 23          # Right flywheel motor direction pin 1
BIN2 = 24          # Right flywheel motor direction pin 2
PWMB = 25          # Right flywheel motor PWM pin (speed control)

STBY = 5           # Standby pin for the TB6612FNG (must be HIGH to enable motors)

BUTTON_PIN = 6     # Button used to cycle through the 3 states

# --- Servo (controlled via PCA9685 board) ---
kit = ServoKit(channels=16)     # Create ServoKit instance for PCA9685 (16-channel PWM driver)
servo_channel = 15               # Gate servo connected to channel 0 on the PCA9685

# --- Stepper TB6612FNG (Board 2, separate from flywheels) ---
ST_AIN1, ST_AIN2 = 12, 16       # Stepper motor coil A pins
ST_BIN1, ST_BIN2 = 20, 21       # Stepper motor coil B pins
ST_STBY = 26                    # Standby pin for the stepper’s TB6612FNG (must be HIGH to enable)

# PWMA/PWMB on the stepper driver should be tied directly to 3.3V so the coils are always powered when STBY is HIGH.

# --- IR Home Sensor (used to home at 0° for State 1) ---
HOME_SENSOR = 4                 # GPIO pin for IR sensor OUT (detects reflective marker)

# --- GPIO Setup ---
GPIO.setmode(GPIO.BCM)          # Use BCM pin numbering
GPIO.setwarnings(False)

# Configure all flywheel motor control pins as outputs and initialize LOW
for pin in [AIN1, AIN2, BIN1, BIN2, STBY]:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Configure all stepper motor control pins as outputs and initialize LOW
for pin in [ST_AIN1, ST_AIN2, ST_BIN1, ST_BIN2, ST_STBY]:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Configure the button and IR sensor as inputs (button has a pull-up)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(HOME_SENSOR, GPIO.IN)

# Configure PWM for the two flywheel motors (1kHz frequency)
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(PWMB, GPIO.OUT)
pwmA = GPIO.PWM(PWMA, 1000)     # Left motor PWM
pwmB = GPIO.PWM(PWMB, 1000)     # Right motor PWM
pwmA.start(0)
pwmB.start(0)

# --- Flywheel Speeds (duty cycle %) for each state ---
# Each tuple is (Left motor duty %, Right motor duty %)
states = [
    (17.5, 17.5),   # State 1 speed
    (17.75, 17.75),   # State 2 speed
    (18.0, 18.0),   # State 3 speed
]
state_index = 0      # Start at State 1

# --- Stepper Setup ---
# Stepper sequence for full-step rotation (4-step pattern)
step_delay = 0.002   # Delay between each step (controls speed)
sequence = [
    (GPIO.HIGH, GPIO.LOW,  GPIO.HIGH, GPIO.LOW),
    (GPIO.HIGH, GPIO.LOW,  GPIO.LOW,  GPIO.HIGH),
    (GPIO.LOW,  GPIO.HIGH, GPIO.LOW,  GPIO.HIGH),
    (GPIO.LOW,  GPIO.HIGH, GPIO.HIGH, GPIO.LOW),
]

# Steps for each state (0°, some angle, another angle)
steps_per_state = [0, 18, 34]  # Adjust these values based on your target angles
current_position = 0             # Tracks current stepper position (in steps)

# --- Servo Gate Function ---
def open_gate():
    """
    Opens the gate briefly to drop a ball, then closes it.
    Uses the PCA9685 servo control for smooth movement.
    """
    kit.servo[servo_channel].angle = 30    # Move servo to open position
    time.sleep(0.3)                        # Keep gate open for ~0.3 seconds
    kit.servo[servo_channel].angle = 110   # Return servo to closed position

# --- Flywheel Helper Functions ---
def enable_flywheels():
    """Enable the flywheel H-bridge by pulling STBY HIGH."""
    GPIO.output(STBY, GPIO.HIGH)

def disable_flywheels():
    """Disable the flywheel H-bridge by pulling STBY LOW (motors off)."""
    GPIO.output(STBY, GPIO.LOW)

def set_motor_direction(motor, forward=True):
    """
    Sets the direction for either motor A (left) or motor B (right).
    forward=True rotates forward; forward=False reverses.
    """
    if motor == 'A':
        GPIO.output(AIN1, GPIO.HIGH if forward else GPIO.LOW)
        GPIO.output(AIN2, GPIO.LOW if forward else GPIO.HIGH)
    elif motor == 'B':
        GPIO.output(BIN1, GPIO.HIGH if forward else GPIO.LOW)
        GPIO.output(BIN2, GPIO.LOW if forward else GPIO.HIGH)

def ramp_to_speed(left_target, right_target, step=0.5, delay=0.05):
    """
    Gradually ramps both motors up to their target duty cycle
    for smooth spin-up (avoids sudden jerks).
    Accepts decimal duty cycles.
    """
    left_current, right_current = 0, 0
    while left_current < left_target or right_current < right_target:
        left_current = min(left_current + step, left_target)
        right_current = min(right_current + step, right_target)
        pwmA.ChangeDutyCycle(left_current)
        pwmB.ChangeDutyCycle(right_current)
        time.sleep(delay)

def spin_and_fire(left_duty, right_duty):
    """
    Spins up the flywheels, waits 3 seconds for speed stabilization,
    opens the servo gate to release one ball, keeps motors running
    for 2 seconds after launch, then shuts everything down.
    """
    enable_flywheels()
    set_motor_direction('A', True)
    set_motor_direction('B', True)
    ramp_to_speed(left_duty, right_duty)   # Ramp up speed
    time.sleep(3)                          # Allow spin-up time
    open_gate()                            # Release one ball
    time.sleep(2)                          # Keep motors running after launch
    pwmA.ChangeDutyCycle(0)                # Stop motors
    pwmB.ChangeDutyCycle(0)
    disable_flywheels()

# --- Stepper Helper Functions ---
def step_motor(steps):
    """
    Moves the stepper by the specified number of steps.
    Positive steps = clockwise, negative steps = counterclockwise.
    """
    direction = 1 if steps > 0 else -1
    total_steps = abs(steps)
    for _ in range(total_steps):
        for step in (sequence if direction > 0 else reversed(sequence)):
            GPIO.output(ST_AIN1, step[0])
            GPIO.output(ST_AIN2, step[1])
            GPIO.output(ST_BIN1, step[2])
            GPIO.output(ST_BIN2, step[3])
            time.sleep(step_delay)

def home_stepper():
    """
    Slowly rotates the stepper counterclockwise until the IR sensor
    detects the reflective marker (LOW signal), which marks 0°.
    Resets current_position to 0.
    """
    print("Homing stepper to 0°...")
    GPIO.output(ST_STBY, GPIO.HIGH)  # Enable stepper driver
    while GPIO.input(HOME_SENSOR) == GPIO.HIGH:
        # Rotate counterclockwise slowly until the sensor detects the tab
        for step in reversed(sequence):
            GPIO.output(ST_AIN1, step[0])
            GPIO.output(ST_AIN2, step[1])
            GPIO.output(ST_BIN1, step[2])
            GPIO.output(ST_BIN2, step[3])
            time.sleep(0.004)  # Slow for precision
    GPIO.output(ST_STBY, GPIO.LOW)  # Disable driver after homing
    print("Stepper homed at 0°.")
    return 0  # Reset position tracking

def move_to_state(state):
    """
    Moves the stepper motor to the target position for the given state
    (relative to current position).
    """
    global current_position
    target_position = steps_per_state[state]
    move_steps = target_position - current_position
    current_position = target_position
    GPIO.output(ST_STBY, GPIO.HIGH)  # Enable stepper driver
    step_motor(move_steps)
    GPIO.output(ST_STBY, GPIO.LOW)   # Disable after movement (no holding torque)
    print(f"Moved to state {state + 1} at {target_position}°.")

# --- Main Loop (Button-Controlled State Cycling) ---
if __name__ == "__main__":
    try:
        print("Press button to cycle through states (1 → 2 → 3 → back to 1, with homing).")
        while True:
            if GPIO.input(BUTTON_PIN) == GPIO.LOW:  # If button is pressed
                # Increment state index and loop back to 0 after 2
                state_index = (state_index + 1) % len(states)
                print(f"State {state_index + 1}: Moving and firing")

                # If we’re returning to State 1 (0°), home using IR sensor
                #global current_position
                if state_index == 0:
                    current_position = home_stepper()
                else:
                    move_to_state(state_index)

                # Spin up flywheels and fire one ball
                spin_and_fire(*states[state_index])

                time.sleep(0.3)  # Debounce to avoid multiple triggers
            time.sleep(0.01)     # Small loop delay to reduce CPU usage

    except KeyboardInterrupt:
        print("\nShutting down...")

    finally:
        # Cleanup all resources safely on exit
        pwmA.stop()
        pwmB.stop()
        disable_flywheels()
        GPIO.cleanup()
