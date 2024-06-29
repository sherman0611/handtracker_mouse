import cv2
import mediapipe as mp
import pyautogui
import time

dpi = 1.5
cam = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands(max_num_hands=1)
drawing_utils = mp.solutions.drawing_utils
screen_w, screen_h = pyautogui.size()
click_y = 0
prev_time = 0

while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1) # flip frame to mirror movements
    frame_h, frame_w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    hands = hand_detector.process(rgb_frame)
    hands = hands.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand) # display hand keypoints
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)

                # index finger: cursor control
                if id == 8:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    index_x = screen_w / frame_w * x * dpi
                    index_y = screen_h / frame_h * y * dpi
                    pyautogui.moveTo(index_x, index_y)

                # if id == 5:
                #     # click_x = screen_w / frame_w * x
                #     click_y = screen_h / frame_h * y

                # # thumb: click
                # if id == 4:
                #     cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                #     # thumb_x = screen_w / frame_w * x
                #     thumb_y = screen_h / frame_h * y

                #     # thumb click trigger
                #     if abs(click_y - thumb_y) < 20:
                #         pyautogui.click()
                #         pyautogui.sleep(1)
                #         print('click')

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
