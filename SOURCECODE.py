# import cv2
# import os
# from cvzone.HandTrackingModule import HandDetector

# cap = cv2.VideoCapture(0)
# cap.set(3,640)
# cap.set(4,480)

# imgbackground = cv2.imread('Resources/Background.png')

# #IMPORTING ALL THE MODE IMAGES TO A  LIST
# #creating a list of Modes folder to change them dynamically
# folderpathModes = 'Resources/Modes'
# print(os.listdir(folderpathModes))
# listImgModesPath = os.listdir(folderpathModes) # contains the path of modes floder as string
# listImgModes = []
# #filling Modes images in list
# for imgMode in listImgModesPath:
#     listImgModes.append( cv2.imread(os.path.join(folderpathModes,imgMode)))
#     print(listImgModes)

# #IMPORTING ALL THE ICONS TO A LIST
# folderpathIcons = 'Resources/Icons'
# print(os.listdir(folderpathModes))
# listImgIconsPath = os.listdir(folderpathIcons) # contains the path of icons floder as string
# listImgIcons = []
# #filling icon images in list
# for imgIconspath in listImgIconsPath:
#     listImgIcons.append( cv2.imread(os.path.join(folderpathIcons,imgIconspath)))
#     print(listImgIcons)


# Modetype = 0  #  changing the selection Modes images on o/p
# selection = -1 # finger selection ctr
# counter = 0 # for time delay in selection
# selectionspeed = 10# multiplier for ellipse speed
# modeposition = [(1136,196),(1000,384),(1136,581)] # center positions of mode images 1,2,3 options
# counterpause = 0 # for delay in next selection, to let customer think about order
# SelectionList = [-1,-1,-1] # storing order icons

# detector = HandDetector(detectionCon=0.8, maxHands=1) # 

# while True:
#     success,img = cap.read()

#       # Find the hand and its landmarks
#     hands, img = detector.findHands(img) 

#     #overlaying the webcam feed on the background image height,width
#     imgbackground[139:139+480,50:50+640]=img

#      #overlaying the selection images on the background image height,width
#     imgbackground[0:720,847:1280]=listImgModes[Modetype]

#      # Find the hand and its landmarks
#     hands, img = detector.findHands(img) 



# # selection is done here ...

#     # if couterpause is 0 that is delay in selecting next item, and modetype list's 3rd index has last image so to 
#     # not select afterwards  it is <3
#     if hands and counterpause == 0 and Modetype<3:
#             # Hand 1
#             hand1 = hands[0]
#             fingers1 = detector.fingersUp(hand1) # checks how many fingers are up
#             print(fingers1)

#             if fingers1 == [0,1,0,0,0]:# if index finger detected change counter and selection to 1 
#                 if selection != 1:
#                     counter =1
#                 selection = 1

#             elif fingers1 == [0,1,1,0,0]:# if index finger detected change counter and selection to 2
#                 if selection != 2:
#                     counter =1
#                 selection = 2

#             elif fingers1 == [0,1,1,1,0]:# if index finger detected change counter and selection to 2 
#                 if selection != 3:
#                     counter =1
#                 selection = 3

#             else:
#                 selection = -1
#                 counter =0
            
#             # if finger is up  then we'll increase the counter
#             if counter>0:
#                 counter+=1
#                 print(counter)
#                 # an ellipse is an fuction in opencv that will allow us to create a variable arc
#                 # it will go round and round and finally selects objects    
#                 cv2.ellipse(imgbackground,modeposition[selection-1],(103,103),0,0,counter*selectionspeed,(0,255,0),20)
                
#                 if counter*selectionspeed>360: # it works when selection is completed
#                     SelectionList[Modetype] = selection 
#                     Modetype+=1 
#                     counter = 0
#                     selection = -1
#                     counterpause = 1
    
#     # once the selection is done, and now counterpause =1 ,make the next selection  delay some time
#     if counterpause>0:
#         counterpause+=1
#         if counterpause>60: #since frame rate is 30fps , then 60 means 2 sec delay for next selection
#             counterpause =0

#     # ADD SELECTION ITEM AT THE BOTTOM
#     if SelectionList[0] != -1:
#         imgbackground[636:636+65,133:133+65] = listImgIcons[SelectionList[0] - 1]
    
#     if SelectionList[1] != -1:
#         imgbackground[636:636+65,340:340+65] = listImgIcons[SelectionList[0] + 2]
    
#     if SelectionList[2] != -1:
#         imgbackground[636:636+65,542:542+65] = listImgIcons[SelectionList[0] + 5]



#     #Displaying 
#    # cv2.imshow("Image",img), for webcam only
#     cv2.imshow("B.TECH CHAI WALA",imgbackground)
#     if cv2.waitKey(1) & 0xff == ord('q'):
#         break






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

