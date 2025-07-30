from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from game_sim import CupPongSimulator
from pydantic import BaseModel
# from adafruit_servokit import ServoKit
from time import sleep
import os
# import board


app = FastAPI()

class CupRequest(BaseModel):
    cup_id: int

# front 2 back comms
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sim = CupPongSimulator()
# Health check route
@app.get("/")
def read_root():
    return {"status": "Backend Running"}

# Example game start route
@app.post("/start-game")
def start_game():
    sim.__init__()  
    return {"message": "Game started!", "state": sim.get_game_state()}

@app.post("/shoot")
def shoot():
    result = sim.simulate_player_shot()
    if result is None:
        return {"message": "Game over!", "state": sim.get_game_state()}
    return {"hit": result, "state": sim.get_game_state()}

@app.post("/robot-turn")
def robot_turn():
    hits = []
    for _ in range(2):
        result = sim.simulate_robot_shot()
        if result is not None:
            hits.append(result)
    return {"hits": hits, "state": sim.get_game_state()}


@app.post("/drop-cup")
async def drop_cup(request: CupRequest):
    cup_id = request.cup_id
    print(f"Dropping cup ID: {cup_id}")
    servo_fn = servo_map.get(cup_id)
    if servo_fn is None:
        print(f"No servo function defined for cup {cup_id}")
    try:
        servo_fn()
    except Exception as e:
        print(f" srevo function falled: {e}")
   
    if cup_id not in servo_map:
        raise HTTPException(status_code=400, detail="Invalid cup ID")
    print("calling servo function")
    servo_map[cup_id]()
   
    return {"message": f"cup {cup_id} dropped"}
   
   

def open_servo(servo_id):
        # kit = ServoKit(channels=16)
        print("Moving servo {servo_id}")
        #kit.servo[servo_id].angle =0
        #sleep(0.5)

       



servo_map = {
    0: open_servo(1),
    1: open_servo(2),
    2: open_servo(3),
    3: open_servo(4),
    4: open_servo(11),
    5: open_servo(10),
    6: open_servo(9),
    7: open_servo(8),
    8: open_servo(7),
    9: open_servo(6),
    10: open_servo(5),
    11: open_servo(0)
}
