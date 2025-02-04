import cv2
import os
import streamlit as st
from cvzone.HandTrackingModule import HandDetector
import numpy as np

# Streamlit App Title
st.title("Beverage Booking System")

# Sidebar Controls for User
start_camera = st.sidebar.button("Start Camera")
stop_camera = st.sidebar.button("Stop Camera")

if start_camera:
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    # Load Resources
    img_background = cv2.imread('Resources/Background.png')

    # Load mode images and icons
    folder_modes = 'Resources/Modes'
    folder_icons = 'Resources/Icons'

    list_img_modes = [cv2.imread(os.path.join(folder_modes, img)) for img in os.listdir(folder_modes)]
    list_img_icons = [cv2.imread(os.path.join(folder_icons, img)) for img in os.listdir(folder_icons)]

    detector = HandDetector(detectionCon=0.8, maxHands=1)

    Modetype = 0
    selection = -1
    counter = 0
    selectionspeed = 10
    mode_positions = [(1136, 196), (1000, 384), (1136, 581)]
    counterpause = 0
    selection_list = [-1, -1, -1]  # This stores the selections for each mode (drink, sugar level, size)

    # Create a placeholder for displaying the video
    video_placeholder = st.empty()
    result_placeholder = st.empty()

    while cap.isOpened():
        success, img = cap.read()
        if not success:
            st.warning("Failed to capture image. Please try again.")
            break

        hands, img = detector.findHands(img)
        img_background[139:139 + 480, 50:50 + 640] = img

        if Modetype < 3:
            img_background[0:720, 847:1280] = list_img_modes[Modetype]

        if hands and counterpause == 0 and Modetype < 3:
            hand = hands[0]
            fingers = detector.fingersUp(hand)

            # Detect selections based on fingers
            if fingers == [0, 1, 0, 0, 0]:
                if selection != 1:
                    counter = 1
                selection = 1
            elif fingers == [0, 1, 1, 0, 0]:
                if selection != 2:
                    counter = 1
                selection = 2
            elif fingers == [0, 1, 1, 1, 0]:
                if selection != 3:
                    counter = 1
                selection = 3
            else:
                selection = -1
                counter = 0

            if counter > 0:
                counter += 1
                # Display selection circle animation
                cv2.ellipse(img_background, mode_positions[selection - 1], (103, 103), 0, 0, counter * selectionspeed, (0, 255, 0), 20)
                if counter * selectionspeed > 360:
                    selection_list[Modetype] = selection
                    Modetype += 1
                    counter = 0
                    selection = -1
                    counterpause = 1

        if counterpause > 0:
            counterpause += 1
            if counterpause > 60:
                counterpause = 0

        # Display Selected Items in Correct Locations
        if selection_list[0] != -1:
            img_background[636:701, 133:198] = list_img_icons[selection_list[0] - 1]
        if selection_list[1] != -1:
            img_background[636:701, 340:405] = list_img_icons[selection_list[1] + 2]
        if selection_list[2] != -1:
            img_background[636:701, 542:607] = list_img_icons[selection_list[2] + 5]

        img_display = cv2.cvtColor(img_background, cv2.COLOR_BGR2RGB)
        video_placeholder.image(img_display, channels="RGB")

        # Display result after final selection
        if Modetype >= 3:
            beverage_sizes = ["Small", "Medium", "Large"]
            beverages = ["Latte", "Black", "Tea"]  # Update to reflect correct beverage options
            
            # Correct indexing to handle the selections properly
            size_index = selection_list[2] - 1 if 0 < selection_list[2] <= len(beverage_sizes) else 0
            result_text = f"You selected: {beverages[selection_list[0] - 1]}, Sugar Level: {selection_list[1]}, Size: {beverage_sizes[size_index]}"

            result_placeholder.success(result_text)
            cap.release()
            break

        if stop_camera:
            cap.release()
            st.write("Camera Stopped.")
            break

    cap.release()
else:
    st.write("Click 'Start Camera' to begin.")

