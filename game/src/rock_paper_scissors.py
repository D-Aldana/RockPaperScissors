from utils.model_utils import ModelUtils
from utils.frame_utils import VideoUtils, DisplayUtils
from utils.game_utils import GameUtils, GameStart
from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import redis


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")
redis = redis.Redis(host='localhost', port=6379, db=0)
game_trigger = GameStart()
game = GameUtils()

def rockPaperScissors(video, cap):

    # Initialize the display utils
    display = DisplayUtils()

    # Initialize the model utils
    model = ModelUtils()

    # Initialize MediaPipe
    hands, mpDraw = model.initializeMediaPipe()

    # Load the gesture recognizer model
    gesture_model = model.loadModel()

    # Load class names
    classNames = model.getClassNames()

    game.sendTopScores(socketio, redis)
    
    # Play the game
    while True:
        try:
            # Get a frame from the webcam
            res, frame = video.readFrame(cap)
            
            # Show the game start screen
            display.showFrame(frame, socketio)

            if game_trigger.getGameStart():
                # Display the countdown
                # frame = display.countdown(frame, 3, socketio)

                # Read gesture
                res, frame = video.readFrame(cap)

                # Get the computer gesture
                computer_gesture = game.rockPaperScissors()

                # Process the gesture
                frame, player_gesture = model.processGesture(frame, hands, gesture_model, classNames)
            
                # Process the game result
                result = game.processGameResult(player_gesture, computer_gesture)

                # Display the result
                frame = display.displayResult(frame, result, player_gesture, computer_gesture)

                # Check high score
                if game.checkHighScore(redis, game.getConsecutiveWins(), socketio):
                    game.sendTopScores(socketio, redis)

                # Display the frame
                display.showFrame(frame, socketio)

                # Display the score
                # frame = display.displayScore(frame, game.getPlayerScore(), game.getComputerScore())
                game.sendScore(socketio)
                display.wait(3000)

                game_trigger.setGameStart(False)

            # Check for quit
            if video.checkQuit():
                break
        except Exception as e:
            # Release the webcam
            video.destroyVideoCapture(cap)
            raise e        
    
    

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('start_game')
def handle_start_game():
    game_trigger.setGameStart(True)

@socketio.on('reset_game')
def handle_reset_game():
    game.resetScore()
    game.sendScore(socketio)

@socketio.on('username')
def set_username(data):
    game.setUsername(data)

if __name__ == "__main__":
    # macOS only shows the camera permission prompt from the main thread
    video = VideoUtils()
    cap = video.initializeVideoCapture()
    socketio.start_background_task(rockPaperScissors, video, cap)
    # 5000 is taken by AirPlay Receiver on macOS; the reloader would also open the camera twice
    socketio.run(app, port=5001, debug=True, use_reloader=False, allow_unsafe_werkzeug=True)



