import cv2
import mediapipe as mp
import pyautogui
import time
import math

# adjustable variables
lerp_spd = 0.5
roi_dimension = 0.5
click_detect = 0.07

# global variables
cam = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands(max_num_hands=1)
drawing_utils = mp.solutions.drawing_utils
screen_w, screen_h = pyautogui.size()
index_palm_x, index_palm_y, index_palm_z = 0, 0, 0
thumb_z = 0
prev_index_x, prev_index_y = screen_w / 2, screen_h / 2
prev_time = 0

pyautogui.FAILSAFE = False # disabled to prevent program halt

def lerp(a, b, t):
    return a + (b - a) * t

while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1) # flip frame to mirror movements
    frame_h, frame_w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    hands = hand_detector.process(rgb_frame)
    hands = hands.multi_hand_landmarks

    # ROI dimensions
    roi_w = int(frame_w * roi_dimension)
    roi_h = int(frame_h * roi_dimension)
    # center ROI dimensions
    roi_x_start = (frame_w - roi_w) // 2
    roi_y_start = (frame_h - roi_h) // 2

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)  # draw hand keypoints
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)

                # index finger palm joint
                if id == 5:
                    index_palm_x = landmark.x
                    index_palm_y = landmark.y
                    index_palm_z = landmark.z

                # thumb: click
                if id == 4:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    thumb_x = landmark.x
                    thumb_y = landmark.y
                    thumb_z = landmark.z

                    dist = math.sqrt((index_palm_x - thumb_x) ** 2 + (index_palm_y - thumb_y) ** 2 + (index_palm_z - thumb_z) ** 2)

                    if dist < click_detect:
                        pyautogui.click()
                        pyautogui.sleep(1)
                        print('click')

                # index finger: cursor control
                if id == 8:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))

                    if roi_x_start <= x <= roi_x_start + roi_w and roi_y_start <= y <= roi_y_start + roi_h:
                        # hand is inside ROI
                        norm_x = (x - roi_x_start) / roi_w
                        norm_y = (y - roi_y_start) / roi_h

                        index_x = norm_x * screen_w
                        index_y = norm_y * screen_h
                    else:
                         # hand is outside ROI
                        if x < roi_x_start:
                            # move along left edge
                            index_x = 0
                            index_y = (y - roi_y_start) / roi_h * screen_h
                        elif x > roi_x_start + roi_w:
                            # move along right edge
                            index_x = screen_w
                            index_y = (y - roi_y_start) / roi_h * screen_h
                        elif y < roi_y_start:
                            # move along top edge
                            index_y = 0
                            index_x = (x - roi_x_start) / roi_w * screen_w
                        elif y > roi_y_start + roi_h:
                            # move along bottom edge
                            index_y = screen_h
                            index_x = (x - roi_x_start) / roi_w * screen_w


                    # Interpolate between previous and current cursor position
                    smooth_index_x = lerp(prev_index_x, index_x, lerp_spd)
                    smooth_index_y = lerp(prev_index_y, index_y, lerp_spd)

                    pyautogui.moveTo(smooth_index_x, smooth_index_y)

                    prev_index_x, prev_index_y = smooth_index_x, smooth_index_y

    # draw ROI rectangle
    cv2.rectangle(frame, (roi_x_start, roi_y_start), (roi_x_start + roi_w, roi_y_start + roi_h), (0, 255, 0), 2)

    # Calculate and display fps
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time
    cv2.putText(frame, f'fps: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow('Hand controlled mouse', frame)
    cv2.waitKey(1)
    # Exit on close
    if cv2.getWindowProperty('Hand controlled mouse', cv2.WND_PROP_VISIBLE) < 1:
        break

cam.release()
cv2.destroyAllWindows()
