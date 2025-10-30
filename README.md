### Demo:
https://youtu.be/9qtuz4oOwE8

# Webcam Rock Paper Scissors

This project implements the classic Rock, Paper, Scissors game with a React frontend, a Python backend for the game logic, and Redis for storing and retrieving high scores. The frontend and backend communicate via websockets.

## Project Structure

The project is structured as follows:

- `react-app/`: Contains the React frontend code.
- `game/`: Contains the Python backend code for the game logic.

## Setup

To set up and run the project locally, follow these steps:

### 1. Clone the Repository

```bash
git clone https://github.com/D-Aldana/RockPaperScissors.git
```

### 2. Install Dependencies

#### Backend Dependencies

In the `game/` directory, install Python dependencies:

```bash
cd game
pip install -r requirements.txt
```

#### Frontend Dependencies

In the `react-app/` directory, install npm dependencies:

```bash
cd ../react-app
npm install
```

### 3. Run Redis Server

Make sure you have Redis installed on your machine. If not, you can install it via package managers like Homebrew (for macOS) or apt (for Ubuntu).

Start the Redis server on your local machine:

```bash
redis-server
```

### 4. Run the Backend Server

In the `game/` directory, start the Python backend server:

```bash
python rock_paper_scissors.py
```

### 5. Run the Frontend Server

In the `react-app/` directory, start the React frontend server:

```bash
npm start
```

## How to Play

Once the servers are running, you can access the game by opening your web browser and navigating to `http://localhost:3000`. Follow the prompts on the web interface to play the game.

## High Scores

High scores are stored and retrieved from the Redis database. Make sure the Redis server is running to save and retrieve high scores.

## Credit
This project a TensorFlow model written by TechVidvan. 
https://techvidvan.com/tutorials/hand-gesture-recognition-tensorflow-opencv/
