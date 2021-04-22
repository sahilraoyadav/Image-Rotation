"""
Paul Witt
340 redo Project 0
"""

import cv2
from numpy import *
from numpy import int as npint

def main(x):
    # Load Image
    origIm = cv2.imread("1.jpg")

    # Sizes
    imH = origIm.shape[0]
    imW = origIm.shape[1]
    
    # This is the largest size I need the new image to be
    size = int(((imH**2.0) + (imW**2.0))**.5)+10
    #print(size**2)
    
    # Angles
    angleDeg = x
    angleR = radians(angleDeg)


    # Rotate Matrix as a numpy array
    rotMat = array(((cos(angleR), (-1*(sin(angleR)))),(sin(angleR),  cos(angleR))))
    
    coords = zeros([2,1], float32)
    outImage  = zeros([size,size,3], float32)
    fromImage = zeros([size,size,3], float32)

    # Shift image to center 
    offsetX = (size - imH)//2
    offsetY = (size - imW)//2

    # Used for error calculation
    original = zeros([size,size,3], float32)
    for i in range(imW):
        for j in range(imH):
            for k in range(3):
                outImage[j + offsetX][i + offsetY][k] = origIm[j][i][k]
                original[j + offsetX][i + offsetY][k] = origIm[j][i][k]

    distSum = 0
    for r in range(360//angleDeg):
        for i in range(size): 
            for j in range(size):
                coords[0][0] = j - size//2      
                coords[1][0] = i - size//2
                
                # rotate image
                outImageXY = matrixMult(rotMat,coords)

                x = int(round(outImageXY[0][0] + size//2))
                y = int(round(outImageXY[1][0] + size//2))
                
                distSum += dist(x,y,j,i)
                
                try:
                    if ( 0 < x < size) and (0 < y < size):
                        for k in range(3):
                            fromImage[j][i][k] = outImage[x][y][k]
                except IndexError:
                    pass

        # Write the image
        cv2.imwrite("pics/angleFromZero_{}.png".format(str(angleDeg * r+ angleDeg)) , fromImage)
        
        # Swap matrix instead of deep copying
        tmp = outImage
        outImage = fromImage
        fromImage = tmp
		

    # Use the Last image and the original to calculate error
    errorSum = 0.0
    counter  = 0
    for i in range(size): 
        for j in range(size):
            for k in range(3):
                errorSum += abs(outImage[i][j][k] - original[i][j][k])
                counter += 1
                    
    #err = round((errorSum/counter)*100,2)
    err = errorSum/counter
    print("Error: ",err)

    # Pixel distance
    print("Pixel: ",distSum/(counter*(360//angleDeg)))
    print("Pixel * rot: ",(distSum/counter))

    
def dist(x1,y1,x2,y2):
    return( (x2-x1)**2 + (y2-y1)**2  )**.5
    
def matrixMult(m1,m2):
    out = zeros([m1.shape[1],m2.shape[1]], float32)
    for i in range(0,m1.shape[1]):
        for j in range(0,m2.shape[0]):
            for k in range(0,m2.shape[1]):               
                out[i][k] += m1[i][j]* m2[j][k]
    return out
    
if __name__ == "__main__":
    for i in [45]:#,60,90,120,180,360]:
        print(i,'::')
        main(i)



