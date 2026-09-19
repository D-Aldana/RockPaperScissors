### Demo:
https://youtu.be/9qtuz4oOwE8

# Webcam Rock Paper Scissors

This project implements the classic Rock, Paper, Scissors game with a React frontend, a Python backend for the game logic, and Redis for storing and retrieving high scores. The frontend and backend communicate via websockets.

## Project Structure

The project is structured as follows:

- `react-app/`: Contains the React frontend code.
- `game/`: Contains the Python backend code for the game logic.

## Setup

Requires Python 3.11 (TensorFlow 2.15 doesn't support newer versions), Node, and Redis (`brew install python@3.11 redis` on macOS).

```bash
git clone https://github.com/D-Aldana/RockPaperScissors.git
cd RockPaperScissors
make install   # Python venv in game/.venv + npm install
make dev       # starts Redis, the game server (port 5001) and the React app
```

The gesture model isn't tracked in git. Place it at `game/src/utils/models/hand-gesture-recognition-code/` (it can be restored from commit `15ebd180^`).

On macOS, allow camera access for your terminal when prompted.

## How to Play

Once the servers are running, you can access the game by opening your web browser and navigating to `http://localhost:3000`. Follow the prompts on the web interface to play the game.

## High Scores

High scores are stored and retrieved from the Redis database. Make sure the Redis server is running to save and retrieve high scores.

## Credit
This project a TensorFlow model written by TechVidvan. 
https://techvidvan.com/tutorials/hand-gesture-recognition-tensorflow-opencv/
