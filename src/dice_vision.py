"""Colored dice detection via camera.

Owner: X
"""

# Import required modules
from time import time

import cv2
import imutils
from gretchen.camera import Camera



# ============================================================
# Square Detector
# ============================================================
class SquareDetector:
    def __init__(self):
        # Blue HSV range
        self.blue_lower = (100, 100, 50)
        self.blue_upper = (130, 255, 255)

        # Green HSV range
        self.green_lower = (40, 50, 50)
        self.green_upper = (90, 255, 255)

        # Red HSV range (split into two ranges)
        self.red_lower = (0, 180, 50)
        self.red_upper = (10, 255, 255)

        self.red_lower2 = (170, 180, 50)
        self.red_upper2 = (180, 255, 255)

    def detect(self, frame):
        """Detect the largest colored square in the image. Returns: frame-image with drawings added
            best_color - detected color ("red", "green", "blue")"""
        # Most OpenCV camera images are BGR, not RGB
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Reduce noise while keeping edges
        hsv = cv2.bilateralFilter(hsv, 15, 100, 100)

        # Create masks
        blue_mask = cv2.inRange(hsv, self.blue_lower, self.blue_upper)
        green_mask = cv2.inRange(hsv, self.green_lower, self.green_upper)
        red_mask1 = cv2.inRange(hsv, self.red_lower, self.red_upper)
        red_mask2 = cv2.inRange(hsv, self.red_lower2, self.red_upper2)

        # cv2.imshow("Blue Mask", blue_mask)
        # cv2.imshow("Green Mask", green_mask)
        # cv2.imshow("Red Mask", red_mask1 + red_mask2)

        masks = {
            "blue": blue_mask,
            "green": green_mask,
            "red": red_mask1 + red_mask2
        }

        best_color = None
        best_area = 0

        for color, mask in masks.items():

            # Remove noise
            mask = cv2.erode(mask, None, iterations=3)
            mask = cv2.dilate(mask, None, iterations=2)

            # Find contours
            cnts = cv2.findContours(
                mask,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )

            cnts = imutils.grab_contours(cnts)

            for cnt in cnts:
                area = cv2.contourArea(cnt)
                # Ignore tiny objects
                if area < 500:
                    continue
                perimeter = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(
                    cnt,
                    0.04 * perimeter,
                    True
                )
                # Must have 4 corners
                if len(approx) != 4:
                    continue
                x, y, w, h = cv2.boundingRect(approx)
                # Check if shape is square-ish
                aspect_ratio = float(w) / h
                if not 0.8 <= aspect_ratio <= 1.2:
                    continue
                # Keep the largest square found
                if area > best_area:
                    best_area = area
                    best_color = color
                    cv2.drawContours(
                        frame,
                        [approx],
                        -1,
                        (0, 255, 255),
                        3
                    )
                    cv2.putText(
                        frame,
                        color.upper(),
                        (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 255, 255),
                        2
                    )

        return frame, best_color

# ============================================================
# Helper Function
# ============================================================

def robot_see_color(camera, detector):
    """Capture image from camera and detect square color."""

    try:
        ret, img, timestamp = camera.getImage()
    except cv2.error:
        # camera.getImage() can throw on an occasional bad/empty read instead
        # of returning ret=False - treat it the same as a failed read.
        return None

    if not ret:
        return None

    img, color = detector.detect(img)

    # Display camera feed
    cv2.imshow("Frame", img)
    cv2.waitKey(1)

    return color


def get_dice_color(cam):
    detector = SquareDetector()
    stable_count = 0
    last_color = None

    while True:
        color = robot_see_color(cam, detector)

        if color == last_color and color is not None:
            stable_count += 1
        else:
            stable_count = 1
            last_color = color

        if stable_count >= 10:
            detected_color = color
            break

    return detected_color
