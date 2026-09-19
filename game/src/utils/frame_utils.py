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
        Stream the live video feed while the frontend shows a countdown.

        Args:
            video: VideoUtils object
            cap: VideoCapture object
            seconds: Number of seconds to countdown from
            socketio: SocketIO server

        Returns:
            None
        """

        end = time.time() + seconds
        last_count = None
        while (remaining := end - time.time()) > 0:
            count = math.ceil(remaining)
            if count != last_count:
                socketio.emit('round', {'phase': 'countdown', 'count': count})
                last_count = count
            _, frame = video.readFrame(cap)
            self.showFrame(frame, socketio)

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

