# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 21:18:03 2024

@author: humai
"""

#from pyimagesearch.transform import four_point_transform
from skimage.filters import threshold_local
from utils import four_point_transform,order_points,get_euler_distance
import numpy as np
import imutils
import cv2
import pytesseract
from pytesseract import Output
from PIL import Image
from matplotlib import cm
from textblob import TextBlob
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from spellchecker import SpellChecker
import re
from scipy.ndimage import interpolation as inter


def highboostfilter(img):
    # Read the image


    # Define the High Boost Filter with central value=4 and A=1.
    HBF = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])

    # Convolve the image 'a' with HBF.
    img = cv2.filter2D(img, -1, HBF, borderType=cv2.BORDER_CONSTANT)
    

    # Normalize the intensity values.
    img = np.uint8(img)
    
    img = cv2.bilateralFilter(img, 5, 30, 30) 
    
    return img

def contrast(img):
    # read the input image


    # define the contrast and brightness value
    contrast = 1.1 # Contrast control ( 0 to 127)
    #brightness = 2. # Brightness control (0-100)

    # call addWeighted function. use beta = 0 to effectively only

    out = cv2.addWeighted( img, contrast, img, 0,1.0)

    # display the image with changed contrast and brightness
    return out

def correct_skew(image, delta=1, limit=5):
    def determine_score(arr, angle):
        data = inter.rotate(arr, angle, reshape=False, order=0)
        histogram = np.sum(data, axis=1, dtype=float)
        score = np.sum((histogram[1:] - histogram[:-1]) ** 2, dtype=float)
        return histogram, score

    gray = image
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1] 

    scores = []
    angles = np.arange(-limit, limit + delta, delta)
    for angle in angles:
        histogram, score = determine_score(thresh, angle)
        scores.append(score)

    best_angle = angles[scores.index(max(scores))]

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, best_angle, 1.0)
    corrected = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC)

    return corrected


def find_each_line(img):
    
    img_list=[]
    
    img2=img.copy()

    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1] 

    img=255-img

    # define the kernel 

    kernel2 = np.ones((4, 40), np.uint8) #kernel for dilation
      
    img = cv2.dilate(img, kernel2, iterations=1) 

    cv2.imshow("dilation",img)
    cv2.waitKey(0)
    
    #cv2.imwrite("dilation.jpg",img)
    #cv2.waitKey(0)
      
    # Finding Contours 
    # Use a copy of the image e.g. edged.copy() 
    # since findContours alters the image 
    contours, hierarchy = cv2.findContours(img,  
        cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
    
    print(contours)

    for i,contour in enumerate(contours):
        perimeter=cv2.arcLength(contour,True)
        print(i,perimeter)
        if(perimeter<50 or perimeter>2500):   #have to automate this by removing outliers 
            pass
        else:
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            print(box)
            box = np.int0(box)
            #print(box)
            #cv2.drawContours(img,[box],0,(255,0,255),2)
            x, y, w, h = cv2.boundingRect(contour)
           
           # Crop the region of interest (ROI) from the original image
            roi = img2[y:y+h, x:x+w]
            #cv2.imshow("ssdf",roi)
            #cv2.imwrite(f'box{i}.jpg',roi)
            cv2.waitKey(0)
            # Save the cropped image
            img_list.append(roi)

    return img_list

def boundary_clear(img):
    
    mask=img.copy()
    #mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY )

    marker=np.zeros(mask.shape)        
    for i in range(mask.shape[0]):
        marker[i,0]=mask[i,0]
        marker[i,mask.shape[1]-1]=marker[i,mask.shape[1]-1]
        
    for i in range(mask.shape[1]):
        marker[0,i]=mask[0,i]
        marker[mask.shape[0]-1,i]=mask[mask.shape[0]-1,i]
        
    radius=1
    kernel = np.ones((3,3),np.uint8)
    #kernel = np.ones((5,5),np.uint8)
    while True:
       marker_prev = marker
       dilation = cv2.dilate(marker, kernel, iterations=1)
       marker = np.minimum(dilation, mask)
       if np.array_equal(marker, marker_prev):
           break
    
    
    return marker


  
def predict(img):
    img = cv2.resize(img, None, fx=3, fy=3)

    for psm in range(6,13+1):
        config = '--oem 3 --psm %d' % psm
        txt = pytesseract.image_to_string(img, config = config, lang='eng')
        print('psm ', psm, ':',txt)
    
    

# load the image and compute the ratio of the old height
# to the new height, clone it, and resize it
image = cv2.imread('corrected.jpg')
#image = cv2.imread('ocr.png')
ratio = image.shape[0] / 1200.0
orig = image.copy()
image = imutils.resize(image, height = 1200)
padding = 20


# Calculate the new dimensions for the padded image
height, width, _ = image.shape
padded_height = height + 2 * padding
padded_width = width + 2 * padding

# Create a black canvas with the new dimensions
padded_image = np.zeros((padded_height, padded_width, 3), dtype=np.uint8)

# Copy the original image onto the center of the padded canvas
padded_image[padding:padding+height, padding:padding+width, :] = image

# Replace the original image with the padded image
image = padded_image
# convert the image to grayscale, blur it, and find edges
# in the image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
kernel = np.ones((5,5),np.uint8)
#gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel, iterations= 3)

gray = cv2.GaussianBlur(gray, (7, 7), 0)
edged = cv2.Canny(gray, 75, 200)
#edged = cv2.dilate(edged, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
kernel = np.ones((9, 9), np.uint8)
closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)


# show the original image and the edge detected image
print("STEP 1: Edge Detection")
#cv2.imwrite("Image", image)
#cv2.imwrite("Edged.jpg", edged)
# find the contours in the edged image, keeping only the
# largest ones, and initialize the screen contour

contours, _ = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filter out small contours
contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 300]
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]
cv2.drawContours(closed, contours[0], 0, (255, 255, 255), 3)
cv2.imshow("dfdfg",closed)
cv2.waitKey(0)
epsilon = 0.03 * cv2.arcLength(contours[0], True)
approx = cv2.approxPolyDP(contours[0], epsilon, True)
print(len(approx))
# loop over the contours
# Ensure that we have exactly 4 points
if len(approx) > 4:
    # Use minAreaRect to get the minimum area rectangle
    sorted_points = sorted(approx, key=lambda x: cv2.contourArea(np.array([x])))

    
    approx = sorted_points[-4:]
    approx = np.array(approx)
    hull = cv2.convexHull(np.array(approx))

   # Check if the points form a convex hull
    is_convex_hull = cv2.isContourConvex(approx)

    if is_convex_hull:
       print("The points form a convex hull.")
    else:
       print("The points do not form a convex hull.")
       approx = cv2.convexHull(np.array(approx))
       rect = cv2.minAreaRect(contours[0])
    
    # Get the box points of the rectangle
       approx = cv2.boxPoints(rect)
       approx = np.intp(approx)
      
       bgdModel = np.zeros((1,65),np.float64)
       fgdModel = np.zeros((1,65),np.float64)
       x, y, w, h = cv2.boundingRect(np.array(approx))
       img=image[y:y+h,x:x+w]
       cv2.imwrite("plot.jpg",img)
       mask = np.zeros(img.shape[:2],np.uint8)
       rect = (x,y,w,h)
       cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
       mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
       img = img*mask2[:,:,np.newaxis]
       cv2.imwrite("Outline2.jpg", img)
    
    # Draw the rectangle on the image
       #approx= approx.reshape((-1, 1, 2))
    #cv2.polylines(image, [box], isClosed=True, color=(0, 255, 0), thickness=2)
    # Draw the rectangle on the image
    #cv2.drawContours(image, [box], 0, (0, 255, 0), 2)
# show the contour (outline) of the piece of paper
print("STEP 2: Find contours of paper")
cv2.drawContours(image, [approx], -1, (0, 255, 0), 2)
cv2.imwrite("Outline.jpg", image)
screenCnt=approx
print(approx)
#applying perspective transform & threshold

print("approx",approx[0])
warped,rect = four_point_transform(image, screenCnt.reshape(4, 2))
print(rect)
# convert the warped image to grayscale, then threshold it
# to give it that 'black and white' paper effect


src_pts = np.array(rect, dtype=np.float32)
cv2.polylines(image, [src_pts.astype(int)], isClosed=True, color=(0, 255, 255), thickness=2)

width = int(get_euler_distance(src_pts[0], src_pts[1]))
height = int(get_euler_distance(src_pts[0], src_pts[3]))

dst_pts = np.array([[0, 0],   [0, width],  [height,width], [height, 0]], dtype=np.float32)

M = cv2.getPerspectiveTransform(src_pts, dst_pts)
warp = cv2.warpPerspective(image, M, (int(height), int(width)),flags=cv2.INTER_CUBIC)

warp= cv2.cvtColor(warp, cv2.COLOR_BGR2GRAY)

warp=correct_skew(warp)

warp = warp[10:warp.shape[0]-10, 10:warp.shape[1]-10]  #for cropping

cv2.imwrite("test8_align.jpg",warp)


#after projective transformation,resulatant image is warp
  
warp=highboostfilter(warp)  #apply sharpening and bilateral noise removing
#warp=contrast(warp)   #increase brightness

#warp = cv2.cvtColor(warp, cv2.COLOR_BGR2GRAY) 

#cv2.imwrite("original3.jpg",warp)

image_list=[]

image_list=find_each_line(warp)


for i in range(len(image_list)):
     image_list[i] = cv2.threshold(image_list[i], 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1] 
     image_list[i]=255-image_list[i]
     mask=boundary_clear(image_list[i])
     image_list[i]=image_list[i]-mask
     #cv2.imshow("sdfsdf",image_list[i])
     #cv2.waitKey(0)
     

output=""
for i in range(len(image_list)-1,-1,-1):
    image_list[i] = cv2.resize(image_list[i], None, fx=2, fy=2)
    im = Image.fromarray(np.uint8(cm.gist_earth(image_list[i])*255))
    config = '--oem 3 --psm 7'
    txt = pytesseract.image_to_string(im, config = config, lang='eng')
    #tb = TextBlob(txt)
    #corrected = tb.correct()
    #output+=str(corrected)
    #output+=str(corrected)
    output+=txt
    output+=" "
    

out=""
docx=re.findall("[a-zA-Z0-9]+",output)
spell=SpellChecker(distance=1)
for word in docx:
  yo=str(word)
  mis=spell.unknown(yo.split())
  #print(yo.split())
  #print(mis)
  if(len(mis)>0):
      tb = TextBlob(word)
      corrected = tb.correct()
      out+=str(corrected)
      out+=" "
  else:
      out+=word
      out+=" "

print(out)




