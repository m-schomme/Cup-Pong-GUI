from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from adafruit_servokit import ServoKit
from time import sleep
import os
import board
import asyncio
from Launcher import move_to_state


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

@app.get("/")
def read_root():
    return {"status": "Backend Running"}



@app.post("/robot-turn")
async def robot_turn():
    print("Robot turn started")
    move_to_state(0)
    await asyncio.sleep(1)
    print("Robot turn complete")
    return {"message": "Robot's turn completed"}


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
   
   
@app.post("/reset-cups")
async def reset_cups():
    print("Resetting all cups")
    kit = ServoKit(channels=16)
    for cup_id in range(11):
        kit.servo[servo_map[cup_id]].angle = 100
        sleep(0.5)
    await asyncio.sleep(0.02)
    return {"message": "All cups reset"}

def open_servo(servo_id):
        kit = ServoKit(channels=16)
        print("Moving servo {servo_id}")
        kit.servo[servo_id].angle =0
        sleep(0.5)

       

servo_map = {
    0: lambda: open_servo(2),
    1: lambda: open_servo(1),
    2: lambda: open_servo(0),
    3: lambda: open_servo(4),
    4: lambda: open_servo(3),
    5: lambda: open_servo(5),
    6: lambda: open_servo(6),
    7: lambda: open_servo(7),
    8: lambda: open_servo(8),
    9: lambda: open_servo(9),
    10: lambda: open_servo(10),
    11: lambda: open_servo(11),
}
