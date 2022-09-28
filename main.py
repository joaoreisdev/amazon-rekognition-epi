import boto3
import numpy as np
import cv2 as cv
import time
from PIL import Image
import asyncio

#@asyncio.coroutine
def detect_labels(photo):

    client=boto3.client('rekognition')

    with open(photo, 'rb') as image:
        response = client.detect_labels(Image={'Bytes': image.read()})

    #print(response)   

    obj_inds = [objs['Name'] for objs in response['Labels'] if objs['Confidence'] > 85]
    print(obj_inds)

    if ('Person' in obj_inds) and ('Hardhat' not in obj_inds):
        print('BIP')
    elif ('Person' in obj_inds) and ('Hardhat' in obj_inds):
        print('OK')
            


    '''for label in response['Labels']:

        if (label['Confidence'] > 80 and ( label['Name'] in ['Hardhat','Person'])):
            print ("Label: " + label['Name'])
            print ("Confidence: " + str(label['Confidence']))
            if (label['Name'] in ['Hardhat']):
                print ("==============CAPACETE IDENTIFICADO===============")'''
    #print (response)
    print('')
    return response

def open_camera():
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    
    while True:

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
    #print("Labels detected: " + str(label_count))


if __name__ == "__main__":
    open_camera()


#asdas
#asasd
#AS

