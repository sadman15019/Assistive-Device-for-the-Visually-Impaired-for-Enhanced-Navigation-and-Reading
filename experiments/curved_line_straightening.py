import cv2
import numpy as np

# Load the image
img = cv2.imread('box_40.jpg')
img2 = cv2.imread('box_40.jpg')

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply GaussianBlur to reduce noise
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# Apply Canny edge detection
edges = cv2.Canny(blur, 50, 150, apertureSize=3)

# Use Hough Line Transform to detect lines
lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)


# Check if any lines are detected
if lines is not None and len(lines) > 0:
    # Iterate through detected lines
    for line in lines:
        x1, y1, x2, y2 = line[0]
        # Draw the detected lines on the original image (optional)
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Calculate the angle of rotation required to straighten the line
        angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi

        # Perform affine transformation to straighten the line
        center = ((x1 + x2) // 2, (y1 + y2) // 2)
        
        print(center,angle)
    
    center=(234, 26) 
    angle=0.8852947869817718
    
    M = cv2.getRotationMatrix2D(center=center, angle=angle,scale= 1)
    #rotated_img = cv2.warpAffine(img, M, (img.shape[1], img.shape[0]), flags=cv2.INTER_CUBIC)
    
    center=(217, 28) 
    angle=0.9594090203960215
    
    M = cv2.getRotationMatrix2D(center=center, angle=angle,scale= 1)
    #rotated_img = cv2.warpAffine(img, M, (img.shape[1], img.shape[0]), flags=cv2.INTER_CUBIC)
    
    center=(70, 22)
    angle= 0.9166542563852879
    
    
    M = cv2.getRotationMatrix2D(center=center, angle=angle,scale= 1)
    #rotated_img = cv2.warpAffine(img, M, (img.shape[1], img.shape[0]), flags=cv2.INTER_CUBIC)
    
    center=(220, 31) 
    angle=-1.8183029644518336
    
    
    M = cv2.getRotationMatrix2D(center=center, angle=angle,scale= 1)
    rotated_img = cv2.warpAffine(img2, M, (img.shape[1], img.shape[0]), flags=cv2.INTER_CUBIC)
    
    center=(414, 25) 
    angle=-0.920334966849057
    
    
    M = cv2.getRotationMatrix2D(center=center, angle=angle,scale= 1)
    #rotated_img = cv2.warpAffine(img, M, (img.shape[1], img.shape[0]), flags=cv2.INTER_CUBIC)
    
    center=(301, 33)
    angle= 0.6780249107513011 
    
    
    M = cv2.getRotationMatrix2D(center=center, angle=angle,scale= 1)
    #rotated_img = cv2.warpAffine(img, M, (img.shape[1], img.shape[0]), flags=cv2.INTER_CUBIC)
    
    center=(235, 33) 
    angle=0.9655677874009163
    
    
    M = cv2.getRotationMatrix2D(center=center, angle=angle,scale= 1)
    #rotated_img = cv2.warpAffine(img, M, (img.shape[1], img.shape[0]), flags=cv2.INTER_CUBIC)
    
    center=(124, 26)
    angle= 0.9628636256362129 
    
    
    M = cv2.getRotationMatrix2D(center=center, angle=angle,scale= 1)
    #rotated_img = cv2.warpAffine(img, M, (img.shape[1], img.shape[0]), flags=cv2.INTER_CUBIC)
    
    center=(566, 17) 
    angle=-2.1210963966614536
    
    
    M = cv2.getRotationMatrix2D(center=center, angle=angle,scale= 1)
    #rotated_img = cv2.warpAffine(img, M, (img.shape[1], img.shape[0]), flags=cv2.INTER_CUBIC)
    
    center=(431, 26) 
    angle=-1.0291548043059815
    
    
    M = cv2.getRotationMatrix2D(center=center, angle=angle,scale= 1)
    #rotated_img = cv2.warpAffine(img, M, (img.shape[1], img.shape[0]), flags=cv2.INTER_CUBIC)
    
 
    

    # Show the straightened image
    cv2.imshow('Straightened Image', rotated_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite("yoyo.jpg",rotated_img)
else:
    print("No lines detected in the image. Skipping straightening process.")
