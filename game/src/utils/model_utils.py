import mediapipe as mp
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
import cv2

class ModelUtils:
    
    def __init__(self):
        pass
        
    def initializeMediaPipe(self):
        """
        Initialize the MediaPipe hands object.

        Returns:
            hands: MediaPipe hands object
            mpDraw: MediaPipe drawing utils object
        """

        mpHands = mp.solutions.hands
        hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        mpDraw = mp.solutions.drawing_utils
        return hands, mpDraw


    def loadModel(self):
        """
        Load the gesture recognizer model.

        Returns:
            model: Gesture recognizer model
        """ 

        ## TODO: Make envrionment variable for path
        # model = load_model('src/utils/models/hand-gesture-recognition-code/mp_hand_gesture')
        model = load_model('utils/models/hand-gesture-recognition-code/mp_hand_gesture')

        return model


    def getClassNames(self):
        """
        Load the class names.

        Returns:
            classNames: List of class names
        """
        
        ## TODO: Make envrionment variable for path
        # f = open('src/utils/models/hand-gesture-recognition-code/gesture.names', 'r')
        f = open('utils/models/hand-gesture-recognition-code/gesture.names', 'r')
        classNames = f.read().split('\n')
        f.close()
        return classNames

    def processGesture(self, frame, hands, model, classNames):
            """
            Process the gesture in the frame.

            Args:
                frame: Frame to process
                hands: Hands object
                model: Model to predict the gesture
                classNames: List of class names

            Returns:
                frame: Frame with landmarks
                className: Predicted gesture
            """
            # The model was trained on pixel coords from a 640x480 webcam
            x, y = 480, 640

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(frame_rgb)
            className = None

            if result.multi_hand_landmarks:
                landmarks = []
                for hand_landmarks in result.multi_hand_landmarks:
                    for lm in hand_landmarks.landmark:
                        lmx = int(lm.x * x)
                        lmy = int(lm.y * y)
                        landmarks.append([lmx, lmy])

                prediction = model.predict([landmarks], verbose=0)
                classID = np.argmax(prediction)
                className = classNames[classID]

                if className not in ["rock", "paper", "scissors"]:
                    className = None

            return frame, className