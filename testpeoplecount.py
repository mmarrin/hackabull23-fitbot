import cv2

import requests
import json


def updaterooms(rooms):
    url = "https://us-central1-aiot-fit-xlab.cloudfunctions.net/fitbot"

    payload = json.dumps({
    "action": "populaterooms",
    "rooms": [
        0,
        1,
        1,
        0
    ]
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

# Load the Haar Cascade face classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_default.xml')

# Create a VideoCapture object to capture video from the webcam
cap = cv2.VideoCapture(0)

# Define the dimensions of the screen and the four rectangles
screen_width = 640
screen_height = 480
rect_width = screen_width // 2
rect_height = screen_height // 2

# Define the rectangles
rectangles = [
    (0, 0, rect_width, rect_height),
    (rect_width, 0, rect_width, rect_height),
    (0, rect_height, rect_width, rect_height),
    (rect_width, rect_height, rect_width, rect_height)
]

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()
    
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the frame using the face cascade classifier
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    # Draw rectangles on the frame
    for x, y, w, h in rectangles:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # Count the number of faces in each rectangle
    rooms = []
    for i, rect in enumerate(rectangles):
        x, y, w, h = rect
        count = 0
        for (fx, fy, fw, fh) in faces:
            if fx >= x and fy >= y and fx + fw <= x + w and fy + fh <= y + h:
                count += 1
                print ("room "+str(i) + " population is " + str(count) )
                
                rooms.append(count)
                
        cv2.putText(frame, f"Count: {count}", (x + 10, y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    # Show the frame
    cv2.imshow('frame', frame)
    
    # Exit if the user presses 'q'
    if cv2.waitKey(1) == ord('q'):
        break

# Release the VideoCapture object and close all windows
cap.release()
cv2.destroyAllWindows()

print (rooms)

updaterooms(rooms)

