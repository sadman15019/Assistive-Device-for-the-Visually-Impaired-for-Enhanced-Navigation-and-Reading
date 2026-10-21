import cv2
import subprocess

cam = cv2.VideoCapture(0)

for i in range(150):
	ret, image = cam.read()
	cv2.imshow('Imagetest',image)
cv2.imwrite('/home/pi/myyolov5-main/data/images/testimage.jpg', image)
cam.release()
cv2.destroyAllWindows()   
command =['python3','/home/pi/myyolov5-main/detect.py','--source', '/home/pi/myyolov5-main/data/images','--weights', '/home/pi/myyolov5-main/test.pt','--conf', '0.5']
subprocess.run(command, capture_output=True, text=True)
	   

