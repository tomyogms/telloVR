# Reference link: https://face-recognition.readthedocs.io/en/latest/face_recognition.html#module-face_recognition.api

import face_recognition
from PIL import Image
import cv2
import os
import sys
import time

input_folder = sys.argv[1]
input_device = sys.argv[2]
known_face_encodings=[]
known_face_names=[]
criminal_face_encodings=[]
criminal_face_names=[]

def trainingFaces():
   for root, dirs, files in os.walk(input_folder):
       for filename in files:
            dir,category = root.split("/")
            if filename.endswith(".jpeg") or filename.endswith(".jpg") or filename.endswith(".png"):
                name,extension = filename.split(".")
                temp = face_recognition.load_image_file(os.path.join(root,filename))
                temp_face_encoding = face_recognition.face_encodings(temp, num_jitters=40)[0]
                #fine tune num_jitters (number of times to re-sample the face), lower number - less accurate but faster (old value 100)
                criminal_face_encodings.append(temp_face_encoding)
                criminal_face_names.append(name)
                print(category + " " + name)
                #print(" Testing face_endocing =" + temp_face_encoding)
                #print(" Testing " + temp_face_encoding)

trainingFaces()

#Logic for 3rd Param to set to TX2 device startup to set video capture device
#if sys.argv[2] == "TX2":
#    video_capture = cv2.VideoCapture("nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)800, height=(int)720, format=(string)I420, framerate=(fraction)30/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink")
#else:
#    video_capture_target = 0
#    video_capture = cv2.VideoCapture(video_capture_target)



# Get a reference to webcam #0 (the default one)

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
face_profile = []
process_this_frame = True

while True:
    # Grab a single frame of video
    frame=cv2.imread("test.png")
    print(frame)


    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        
        
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]
    
	# Only process every other frame of video to save time
    #Logic for 3rd Param to set to TX2 device startup to set face_location
    if process_this_frame:
        if sys.argv[2] == "TX2":
            face_locations = face_recognition.face_locations(rgb_small_frame, model="cnn", number_of_times_to_upsample=1)
        else:
            face_locations = face_recognition.face_locations(rgb_small_frame)
        # Find all the faces and face encodings in the current frame of video
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []
        face_profile=[]

        for face_encoding in face_encodings:
            name = "Unknown"
            profile = "Unknown"
            
            distances = face_recognition.face_distance(criminal_face_encodings, face_encoding)
            print("distances = ", distances)
            best_distance, best_index = min((distances[i],i ) for i in range(len(distances)))
            if(best_distance <= 0.5):
                name = criminal_face_names[best_index]
                time.sleep(0.1)
                profile = "Criminal"
                f = open("data.txt", "w+")
                f.write(name)
                f.close()
           
            face_names.append(name)
            print(face_names)
            face_profile.append(profile)
            print(face_profile)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name, profile in zip(face_locations, face_names, face_profile):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4


        # Draw a box around the face
        font = cv2.FONT_HERSHEY_DUPLEX
        #print(profile)
        #initial
        topFrame= 0
        bottomFrame= 0
        leftFrame= 0
        rightFrame= 0
        #Boundries
        topFrame= top-60
        bottomFrame= bottom+60
        leftFrame= left-60
        rightFrame= right+60
        #Limits 
        limT=61
        limB=459
        limL=61
        limR=639

        if topFrame>limT:
            topFrame= topFrame
        else:
            topFrame= top

        if bottomFrame>limB:
            bottomFrame= bottomFrame
        else:
            bottomFrame= bottom

        if leftFrame>limL:
            leftFrame= leftFrame
        else:
            leftFrame= left

        if rightFrame>limR:
            rightFrame= rightFrame
        else:
            rightFrame= right

	
        if profile=="Criminal":
            cv2.rectangle(frame, (left, top), (right, bottom+50), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom + 15), (right, bottom+50), (0, 0, 255), cv2.FILLED)
            cv2.putText(frame, name, (left + 6, top + 30), font, 1.0, (255, 255, 255), 1)
            cv2.putText(frame, profile, (left + 6, bottom + 45), font, 1.0, (255, 255, 255), 1)
            #Create picture of the face
            cropped = frame[topFrame:bottomFrame, leftFrame:rightFrame]
            #cv2.imshow('image',frame)
            cv2.imwrite("pics/test.jpg", cropped)
        
        if profile=="Unknown":
            cv2.rectangle(frame, (left, top), (right, bottom +50), (244, 232, 65), 2)
            cv2.rectangle(frame, (left, bottom + 15), (right, bottom+50), (244, 232, 65), cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom +45), font, 1.0, (0, 0, 0), 1)

    # Display the resulting image
    cv2.imshow('Frame', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
#video_capture.release()
cv2.destroyAllWindows()

