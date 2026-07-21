"""Hand gesture recognition: start gesture + Rock-Paper-Scissors hand signs.

Owner: A
"""

import time

from anyio import current_time
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

    HAND_CONNECTIONS = (
        (0, 1), (1, 2), (2, 3), (3, 4),
        (0, 5), (5, 6), (6, 7), (7, 8),
        (5, 9), (9, 10), (10, 11), (11, 12),
        (9, 13), (13, 14), (14, 15), (15, 16),
        (13, 17), (17, 18), (18, 19), (19, 20),
        (0, 17)
    )

    def __init__(self, confidence_threshold=0.70, hold_time=2.0):
        """
        Initializes the Gesture class. Referenced from: https://developers.google.com/edge/mediapipe/solutions/vision/gesture_recognizer/python#video

        Args:
            confidence_threshold: The minimum confidence score for a gesture to be considered valid.
            hold_time: The time in seconds to hold a gesture before considering it valid.
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
        self.start_time = time.monotonic()g
        self.last_timestamp_ms = -1

        self.hold_time = hold_time
        self.last_result = None


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
        self.last_result = self.recognizer.recognize_for_video(mp_image, timestamp_ms)

        # result.gesture has nested list, where the outer list holds the hands detected, and the inner list holds the accuarcy of gestures detected for that hand. 
        # Since we are only detecting one hand as well as see the most likely gesture out of rock paper scissors, we only need to check the first element of both lists.
        
        # If no hands are detected
        if not self.last_result.gestures:
            return None
        
        # If a hand is detected, but no gesture is recognized
        elif not self.last_result.gestures[0]:
            return None

        # If a gesture is recognized, return the corresponding RPS value
        else:
            return self.GESTURE_TO_RPS.get(self.last_result.gestures[0][0].category_name)

    def rps(self, camera):
        """
        Detects hand gestures in the given image and returns the corresponding Rock-Paper-Scissors value.

        Args:
            camera: The camera object from which to get images.

        Returns:
            The corresponding Rock-Paper-Scissors value.
        """
        current_gesture = None
        gesture_start_time = 0.0

        while True:
            ret, img, timestamp = camera.getImage()
            frame = self.detect(img)
            self.draw(img)

            current_time = time.monotonic()
            elapsed_time = 0.0
            if frame is None:
                current_gesture = None
                gesture_start_time = 0.0
                message = "Show ROCK, PAPER, or SCISSORS"

            elif frame != current_gesture:
                current_gesture = frame
                gesture_start_time = current_time
                remaining_time = max(0.0, self.hold_time - elapsed_time)
                message = (f"Hold for {remaining_time:.1f}s")

            else:
                elapsed_time = current_time - gesture_start_time
                remaining_time = max(0.0, self.hold_time - elapsed_time)
                message = (f"Hold for {remaining_time:.1f}s")


            if elapsed_time >= self.hold_time:
                cv2.destroyWindow("Frame")
                return frame


            cv2.putText(img, message, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
            
            # Display image
            cv2.imshow("Frame", img)
            cv2.waitKey(1)

            if frame is not None:
                return Move(frame)


    def wait_for_start(self, camera):
        """
        Blocks until the player shows a hand gesture, and reports whether it was
        paper (hand up) — the signal to start the game.

        Returns:
            True if the shown gesture was paper, False for rock or scissors.
        """
        return self.rps(camera) == Move.PAPER
    

    def draw(self, frame):
        if self.last_result is None:
            return frame

        if not self.last_result.hand_landmarks:
            return frame

        height, width = frame.shape[:2]

        for hand_landmarks in self.last_result.hand_landmarks:
            points = []

            for landmark in hand_landmarks:
                x = int(landmark.x * width)
                y = int(landmark.y * height)
                points.append((x, y))

            for start_index, end_index in self.HAND_CONNECTIONS:
                cv2.line(frame, points[start_index], points[end_index], (255, 255, 255), 2)

            for point in points:
                cv2.circle(frame, point, 5, (0, 255, 0), -1)

        return frame


    def close(self):
        """
        Release the MediaPipe recognizer. Run when the Gesture class is no longer needed to free up resources.
        """

        self.recognizer.close()