import boto3
import numpy as np
import cv2 as cv
import time
from PIL import Image

def detect_labels(photo):

    client=boto3.client('rekognition')

    with open(photo, 'rb') as image:
        response = client.detect_labels(Image={'Bytes': image.read()})
    '''
    print('Detected labels for ' + photo) 
    print()   
    for label in response['Labels']:
        print ("Label: " + label['Name'])
        print ("Confidence: " + str(label['Confidence']))
        print ("Instances:")
        for instance in label['Instances']:
            print ("  Bounding box")
            print ("    Top: " + str(instance['BoundingBox']['Top']))
            print ("    Left: " + str(instance['BoundingBox']['Left']))
            print ("    Width: " +  str(instance['BoundingBox']['Width']))
            print ("    Height: " +  str(instance['BoundingBox']['Height']))
            print ("  Confidence: " + str(instance['Confidence']))
            print()

        print ("Parents:")
        for parent in label['Parents']:
            print ("   " + parent['Name'])
        print ("----------")
        print ()
        '''
    print (response)
    print('')
    return response

def open_camera():
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    
    while True:
        time.sleep(5)
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # Our operations on the frame come here
        gray = cv.cvtColor(frame, cv.COLOR_BGR2BGRA)
        
        # Salva imagem        
        cv.imwrite('.temp/temp.jpg', gray)

        # Detect Label
        response = detect_labels('.temp/temp.jpg')

        # Draw rectangle
        for label in response['Labels']:
            print(label)
            if label['Name'] == "Person":
                print('***********Name == Person***********')
                for instance in label['Instances']:
                    print('***********inside instance***********')
                    start_point = (instance['BoundingBox']['Top'], instance['BoundingBox']['Left'])
                    end_point = (instance['BoundingBox']['Width'], instance['BoundingBox']['Height'])
                    color = (0, 255, 0)
                    thickness = 2
                    gray = cv.rectangle(gray, start_point, end_point, color, thickness)

        # Display the resulting frame
        cv.imshow('frame', gray)

        # Save AWS
        # client = boto3.client('s3', region_name='us-east-1')
        # reconhecer(exite exite pjb/exite pessoa) X identificar(qual o objeito/qual pessoa)
        # testes (cenário de testes)
        # client.upload_file('images/image_0.jpg', 'mybucket', 'image_0.jpg')

        if cv.waitKey(1) == ord('q'):
            break
    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()

def main():
    photo='ComCapacete-ComCaneta.jpeg'
    bucket='bucket-epi-us'
    label_count=detect_labels(photo)
    print("Labels detected: " + str(label_count))


if __name__ == "__main__":
    open_camera()