import cv2
import matplotlib.pyplot as plt
import numpy as np

img=cv2.imread("test8.jpeg",cv2.IMREAD_GRAYSCALE)  # to actually read
img2=cv2.imread("test8.jpeg")  # to crop each line, same image with no modification

img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1] 

img=255-img

cv2.imshow("sdfsdf",img)

cv2.waitKey(0)




  
# define the kernel 

kernel2 = np.ones((8, 40), np.uint8) #kernel for dilation
  
img = cv2.dilate(img, kernel2, iterations=1) 

cv2.imshow("dilation",img)
cv2.waitKey(0)
 

#img = cv2.Canny(img, 30, 200) 

#cv2.imshow('image', img) 
#cv2.waitKey(0) 

#cv2.imwrite("line detected image.png",img)
  
# Finding Contours 
# Use a copy of the image e.g. edged.copy() 
# since findContours alters the image 
contours, hierarchy = cv2.findContours(img,  
    cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 

# for contour in contours:
#     # Calculate the bounding box for the contour
#     x, y, w, h = cv2.boundingRect(contour)
    
#     # Calculate xmax, xmin, ymax, ymin
#     xmax = x + w
#     ymax = y + h
    
#     # Print or use these values as needed
#     print("xmin:", x)
#     print("xmax:", xmax)
#     print("ymin:", y)
#     print("ymax:", ymax)
    
#     # Draw the bounding box on the original image (optional)
#     cv2.rectangle(img2, (x, y), (xmax, ymax), (255, 255, 0), 2)
print(contours)
for i,contour in enumerate(contours):
    area=cv2.contourArea(contour)
    perimeter=cv2.arcLength(contour,True)
    #print(i,perimeter)
    if(perimeter<1000 or perimeter>2500):
        pass
    else:
          rect = cv2.minAreaRect(contour)
          box = cv2.boxPoints(rect)
          #print(box)
          box = np.int0(box)
          #print(box)
          cv2.drawContours(img,[box],0,(255,0,255),2)
          x, y, w, h = cv2.boundingRect(contour)
       
        # Crop the region of interest (ROI) from the original image
          roi = img2[y:y+h, x:x+w]
          # Save the cropped image
          cv2.imwrite(f'test8_{i}.jpg', roi)
    
   #  rect = cv2.minAreaRect(contour)
   #  box = cv2.boxPoints(rect)
   #  print(box)
   #  box = np.int0(box)
   #  #print(box)
   #  cv2.drawContours(img,[box],0,(255,0,255),2)
   #  x, y, w, h = cv2.boundingRect(contour)
   
   # # Crop the region of interest (ROI) from the original image
   #  roi = img2[y:y+h, x:x+w]
   #  # Save the cropped image
   #  cv2.imwrite(f'test8_{i}.jpg', roi)



# Show the image with bounding boxes (optional)
cv2.imwrite('Bounding Boxes.png', img)
cv2.waitKey(0)
cv2.destroyAllWindows()


# temp=np.zeros(img.shape,dtype=np.uint8)  
# for i in range (len(contours[1])):
#     x=int(contours[1][0][0][0])
#     y=int(contours[1][0][0][1])
#     print(x,y)
#     temp[x,y]=255
# #print("Number of Contours found = " + str(len(contours))) 
  
# Draw all contours 
# -1 signifies drawing all contours 
#cv2.drawContours(img, contours, -1, (255, 255, 0), 3) 
  
#cv2.imwrite("contour image.png",img)
cv2.waitKey(0) 
cv2.destroyAllWindows() 
