from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from game_sim import CupPongSimulator

app = FastAPI()

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production you can restrict this
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
    result = sim.simulate_shot()
    if result is None:
        return {"message": "Game over!", "state": sim.get_game_state()}
    return {"hit": result, "state": sim.get_game_state()}


    
