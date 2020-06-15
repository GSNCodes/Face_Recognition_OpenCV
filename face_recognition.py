import os
import cv2
import time
import argparse
import face_recognition

## Face recognition computation
def face_from_video(video, known_faces, known_names):

    while True:
        ret, image = video.read()
        locations = face_recognition.face_locations(image, model=MODEL)
        encodings = face_recognition.face_encodings(image, locations)

        for face_encoding, face_location in zip(encodings, locations):
            results = face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE)
            match = None
            if True in results:
                match = known_names[results.index(True)]
                print(f"Match Found: {match}")

                top_left = (face_location[3], face_location[0])
                bottom_right = (face_location[1], face_location[2])

                color = [0, 255, 0]

                cv2.rectangle(image, top_left, bottom_right, color, FRAME_THICKNESS)

                top_left = (face_location[3], face_location[2])
                bottom_right = (face_location[1], face_location[2]+22)

                cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)
                cv2.putText(image, match, (face_location[3]+10, face_location[2]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), FONT_THICKNESS)

        cv2.imshow("Match", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

## Image files
def face_from_images(TEST_FACES_DIR, known_faces, known_names):

    for filename in os.listdir(TEST_FACES_DIR):
        image = face_recognition.load_image_file(f"{TEST_FACES_DIR}/{filename}")
        locations = face_recognition.face_locations(image, model=MODEL)
        encodings = face_recognition.face_encodings(image, locations)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        for face_encoding, face_location in zip(encodings, locations):
            results = face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE)
            match = None
            if True in results:
                match = known_names[results.index(True)]
                print(f"Match Found: {match}")

                top_left = (face_location[3], face_location[0])
                bottom_right = (face_location[1], face_location[2])

                color = [0, 255, 0]

                cv2.rectangle(image, top_left, bottom_right, color, FRAME_THICKNESS)

                top_left = (face_location[3], face_location[2])
                bottom_right = (face_location[1], face_location[2] + 22)

                cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)
                cv2.putText(image, match, (face_location[3] + 10, face_location[2] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), FONT_THICKNESS)

        cv2.imshow(filename, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == '__main__':
    ## Arguments to give before running
    ap = argparse.ArgumentParser()
    ap.add_argument('-v', '--video', help='Path to video file', default=None)
    ap.add_argument('-u', '--users', help='Path to user images', required=True)
    ap.add_argument('-i', '--image', help='Path to the folder containing test images', default=None)
    ap.add_argument('-c', '--camera', help='To use the live feed from web-cam', default=True)
    ap.add_argument('-m', '--model', help='Choose the model to use', choices=['hog', 'cnn'], default='hog')
    ap.add_argument('-t', '--tolerance', help='Tolerance value for the model', default=0.6)
    args = vars(ap.parse_args())

    ## Constants under use
    TOLERANCE = args['tolerance']
    FRAME_THICKNESS = 3
    FONT_THICKNESS = 2
    MODEL = args['model']

    ## Generate face encodings
    known_faces = []
    known_names = []
    USER_FACES_DIR = args["users"]

    for name in os.listdir(USER_FACES_DIR):
        for filename in os.listdir(f"{USER_FACES_DIR}/{name}"):
            image = face_recognition.load_image_file(f"{USER_FACES_DIR}/{name}/{filename}")
            encoding = face_recognition.face_encodings(image)[0]
            known_faces.append(encoding)
            known_names.append(name)

    if args["camera"] == True or args["video"]:
        ## Webcam part
        if args["camera"] == True:
            video = cv2.VideoCapture(0)
            time.sleep(2.0)
            
        ## Video file
        else:
            VIDEO_PATH = args["video"]
            video = cv2.VideoCapture(VIDEO_PATH)

        face_from_video(video, known_faces, known_names)

    if args["image"]:
        TEST_FACES_DIR = args["image"]
        face_from_images(TEST_FACES_DIR, known_faces, known_names)