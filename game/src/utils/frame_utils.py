import cv2
import base64
import math
import sys
import time

class VideoUtils:

    def __init__(self):
        pass


    def initializeVideoCapture(self):
        """
        Initialize the video capture object.

        Args:
            None

        Returns:
            cap: VideoCapture object
        """

        # DirectShow only exists on Windows
        backend = cv2.CAP_DSHOW if sys.platform == 'win32' else cv2.CAP_ANY
        cap = cv2.VideoCapture(0, backend)
        if not cap.isOpened():
            raise Exception("Error opening the camera")

        cv2.waitKey(1000)
        print("Camera opened successfully")
        return cap


    def readFrame(self, cap):
        """
        Get a frame from the video capture object.

        Args:
            cap: VideoCapture object

        Returns:
            frame: Frame from the video capture object
        """

        res, frame = cap.read()
        if not res:
            raise Exception("Error reading the frame")
        frame = cv2.flip(frame, 1)
        # cv2.imshow("Rock Paper Scissors", frame)
        # frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return res, frame

    def checkQuit(self):
        """
        Check if the user wants to quit the game.

        Args:
            None

        Returns:
            True if the user wants to quit, False otherwise
        """

        return cv2.waitKey(1) & 0xFF == ord('q')


    def destroyVideoCapture(self, cap):
        """
        Release the video capture object.

        Args:
            cap: VideoCapture object

        Returns:
            None
        """
        
        cap.release()
        cv2.destroyAllWindows()
        print("Camera released successfully")


class DisplayUtils:

    def __init__(self):
        pass

    
    def showFrame(self, frame, socketio):
        """
        Display a frame.

        Args:
            frame: Frame to display

        Returns:
            None
        """

        # cv2.imshow("Rock Paper Scissors", frame)
        if frame is None:
            raise Exception("Error displaying the frame")
        _, buffer = cv2.imencode('.jpg', frame)
        frame_encoded = base64.b64encode(buffer)

        socketio.emit('video_feed', frame_encoded.decode('utf-8'))
        socketio.sleep(0.01)

    def wait(self, ms):
        """
        Wait for a specified number of milliseconds.

        Args:
            ms: Number of milliseconds to wait

        Returns:
            None
        """

        cv2.waitKey(ms)


    # def checkGameStart(self, sockietio):
    #     """
    #     Check if the user wants to start the game.

    #     Args:
    #         None

    #     Returns:
    #         True if the user wants to start the game, False otherwise
    #     """


    #     # If receive a message from the socketio server, start the game
    #     socketio.on('start_game', namespace='/game')
    #     # Explain the line above:
    #     #  - socketio.on() is a decorator that registers a handler for a particular event
    #     # - 'start_game' is the event name
    #     # - namespace='/game' is the namespace to which the event belongs
    #     # - The function below is the handler for the event
    
    #     return 

    def countdown(self, video, cap, seconds, socketio):
        """
        Display a countdown over the live video feed.

        Args:
            video: VideoUtils object
            cap: VideoCapture object
            seconds: Number of seconds to countdown from
            socketio: SocketIO server

        Returns:
            None
        """

        end = time.time() + seconds
        while (remaining := end - time.time()) > 0:
            _, frame = video.readFrame(cap)
            self.showFrame(self.centerText(str(math.ceil(remaining)), frame, font_scale=4, font_thickness=8), socketio)

    def centerText(self, msg, frame, colour=(255, 255, 255), font_scale=1, font_thickness=2):
        """
        Display text in the center of the frame.

        Args:
            msg: Message to display
            frame: Frame to display the message on
            colour: Colour of the text

        Returns:
            frame: Frame with the text displayed on it
        """

        text = msg
        font = cv2.FONT_HERSHEY_SIMPLEX
        text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
        text_x = (frame.shape[1] - text_size[0]) // 2
        text_y = (frame.shape[0] + text_size[1]) // 2
        cv2.putText(frame, text, (text_x, text_y), font, font_scale, colour, font_thickness)
        return frame


    def displayResult(self, frame, result, player_gesture, computer_gesture):
        """
        Display the result of the game.

        Args:
            frame: Frame to display the result on
            result: Result of the game

        Returns:
            frame: Frame with the result displayed on it
        """

        if result == 1:
            msg = "You win!"
        elif result == -1:
            msg = "You lose!"
        elif result == 0:
            msg = "It's a draw!"
        else:
            msg = "Invalid gesture!"

        result = f"You played {player_gesture} | Computer played {computer_gesture}"
        cv2.putText(frame, result, (10, frame.shape[0] - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2, cv2.LINE_AA)
        frame = self.centerText(msg, frame, colour=(0, 255, 0))
        return frame

    # def displayScore(self, frame, player_score, computer_score):
    #     """
    #     Display the score of the game.

    #     Args:
    #         frame: Frame to display the score on
    #         player_score: Player's score
    #         computer_score: Computer's score

    #     Returns:
    #         frame: Frame with the score displayed on it
    #     """

    #     msg = f"Player: {player_score} | Computer: {computer_score}"
    #     frame = cv2.putText(frame, msg, (10, frame.shape[0] - 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    #     return frame

