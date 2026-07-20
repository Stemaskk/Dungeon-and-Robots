"""Hand gesture recognition: start gesture + Rock-Paper-Scissors hand signs.

Owner: A
"""

import time
import cv2

import mediapipe as mp
from pathlib import Path
from src.game_logic import Move

class Gesture:

    GESTURE_TO_RPS = {
        "Closed_Fist": "ROCK",
        "Open_Palm": "PAPER",
        "Victory": "SCISSORS"
        }

    def __init__(self, confidence_threshold=0.6):
        """
        Initializes the Gesture class. Referenced from: https://developers.google.com/edge/mediapipe/solutions/vision/gesture_recognizer/python#video

        Args:
            confidence_threshold: The minimum confidence score for a gesture to be considered valid.
        """

        current_directory = Path(__file__).resolve().parent
        model_path = (current_directory / "gesture_model" / "gesture_recognizer.task")

        if not model_path.exists():
            raise FileNotFoundError(f"Gesture model was not found: {model_path}")
        
        options = mp.tasks.vision.GestureRecognizerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path=str(model_path)),
            running_mode=mp.tasks.vision.RunningMode.VIDEO,
            num_hands=1,
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5,
            canned_gesture_classifier_options=mp.tasks.components.processors.ClassifierOptions(max_results = 1, score_threshold=confidence_threshold, category_allowlist=["Closed_Fist", "Open_Palm", "Victory",]),
        )

        self.recognizer = (mp.tasks.vision.GestureRecognizer.create_from_options(options))
        
        # Time is needed to ensure that the timestamp for each frame is unique, as well as not the previous one.
        self.start_time = time.monotonic()
        self.last_timestamp_ms = -1

    def detect(self, frame):
        """
        Detects hand gestures in the given image.

        Args:
            frame: The input frame in which to detect hand gestures.

        Returns:
            The detected hand gesture.
        """
        if frame is None:
            return None
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        # The timestamp is calculated in milliseconds since the start of the program, due to Mediapipe's requirements.
        timestamp_ms = int((time.monotonic() - self.start_time) * 1000)

        # Ensure that the timestamp is always increasing
        if timestamp_ms <= self.last_timestamp_ms:
            timestamp_ms = self.last_timestamp_ms + 1

        self.last_timestamp_ms = timestamp_ms
        result = self.recognizer.recognize_for_video(mp_image, timestamp_ms)

        # result.gesture has nested list, where the outer list holds the hands detected, and the inner list holds the accuarcy of gestures detected for that hand. 
        # Since we are only detecting one hand as well as see the most likely gesture out of rock paper scissors, we only need to check the first element of both lists.
        
        # If no hands are detected
        if not result.gestures:
            return None
        
        # If a hand is detected, but no gesture is recognized
        elif not result.gestures[0]:
            return None

        # If a gesture is recognized, return the corresponding RPS value
        else:
            return self.GESTURE_TO_RPS.get(result.gestures[0][0].category_name)

    def rps(self, camera):
        """
        Detects hand gestures in the given image and returns the corresponding Rock-Paper-Scissors value.

        Args:
            frame: The input frame in which to detect hand gestures.

        Returns:
            The corresponding Rock-Paper-Scissors value.
        """
        while True:
            ret, img, timestamp = camera.getImage()
            frame = self.detect(img)

            # Display image
            cv2.imshow("Frame", img)
            cv2.waitKey(1)

            if frame is not None:
                return Move(frame)

    def close(self):
        """
        Release the MediaPipe recognizer. Run when the Gesture class is no longer needed to free up resources.
        """

        self.recognizer.close()