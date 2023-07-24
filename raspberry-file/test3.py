# import the GPIO and time package
import RPi.GPIO as GPIO
import time

from picamera2 import Picamera2, Preview

# ! /usr/bin/python

# import the necessary packages
import face_recognition
import imutils
import pickle
import time
import cv2
import numpy as np

# Initialize 'currentname' to trigger only when a new person is identified.
currentname = "unknown"
# Determine faces from encodings.pickle file model created from train_model.py
encodingsP = "/home/group6/Documents/fr1/encodings.pickle"

# load the known faces and embeddings along with OpenCV's Haar
# cascade for face detection
print("[INFO] loading encodings + face detector...")
data = pickle.loads(open(encodingsP, "rb").read())
print(type(data))
# initialize the video stream and allow the camera sensor to warm up
# Set the ser to the followng
# src = 0 : for the build in single web cam, could be your laptop webcam
# src = 2 : I had to set it to 2 inorder to use the USB webcam attached to my laptop
# vs = VideoStream(src=2,framerate=10).start()

# start the FPS counter

# loop over frames from the video file stream
# grab the frame from the threaded video stream and resize it
# to 500px (to speedup processing)

# frame = cv2.imread('/home/group6/Documents/fr1/dataset/test/test4.jpg')
# frame = cv2.imread('/home/group6/Documents/SRC/src05/face/test1.jpg')

# Detect the fce boxes

# Pin  Definitions
pirSensorPin = 12

# Pin Setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pirSensorPin, GPIO.IN)

print("Program running... Press CTRL+C to exit")

picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start_preview(Preview.QTGL)
picam2.start()
time.sleep(2)
i = 1
try:

    while True:
        if GPIO.input(pirSensorPin):
            print('Motion detected!')
            picam2.capture_file(f"./face1/test{i}.jpg")
            frame = cv2.imread(f"./face1/test{i}.jpg")
            frame = imutils.resize(frame, width=500)
            boxes = face_recognition.face_locations(frame)
            # compute the facial embeddings for each face bounding box
            encodings = face_recognition.face_encodings(frame, boxes)
            names = []
            i = i + 1
            # loop over the facial embeddings
            for encoding in encodings:

                # attempt to match each face in the input image to our known
                # encodings
                matches = face_recognition.compare_faces(data["encodings"],
                                                         encoding, tolerance=0.37)
                print(matches)
                name = "Unk"  # if face is not recognized, then print Unknown

                # check to see if we have found a match
                if True in matches:
                    # find the indexes of all matched faces then initialize a
                    # dictionary to count the total number of times each face
                    # was matched
                    # matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                    # counts = {}

                    # loop over the matched indexes and maintain a count for
                    # each recognized face face
                    # for i in matchedIdxs:
                    # name = data["names"][i]
                    # counts[name] = counts.get(name, 0) + 1

                    face_distances = face_recognition.face_distance(data["encodings"], encoding)
                    # print(face_distances)
                    best_match_index = np.argmin(face_distances)
                    print('distance: {}'.format(face_distances[best_match_index]))
                    if matches[best_match_index]:
                        name = data["names"][best_match_index]

                    # determine the recognized face with the largest number
                    # of votes (note: in the event of an unlikely tie Python
                    # will select first entry in the dictionary)
                    # name = max(counts, key=counts.get)

                    # If someone in your dataset is identified, print their name on the screen
                # if currentname != name:
                #	currentname = name
                #	print(currentname)

                # update the list of names
                names.append(name)
                print(name)
                wrl = open('/home/group6/name.txt', 'w')
                wrl.write(name)

            # loop over the recognized faces
            for ((top, right, bottom, left), name) in zip(boxes, names):
                # draw the predicted face name on the image - color is in BGR
                cv2.rectangle(frame, (left, top), (right, bottom),
                              (0, 255, 225), 2)
                y = top - 15 if top - 15 > 15 else top + 15
                cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                            .8, (0, 255, 255), 2)

            # display the image to our screen
            # cv2.imshow("Facial Recognition is Running", frame)
            # key = cv2.waitKey(0) & 0xFF

            # quit when 'q' key is pressed

            # update the FPS counter
            # stop the timer and display FPS information

            # do a bit of cleanup
            cv2.destroyAllWindows()



        else:

            print('No motion detected...')

        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("Program terminated!")
