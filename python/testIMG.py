#https://robotclass.ru/tutorials/opencv-detect-rectangle-angle/
#https://datahacker.rs/012-blending-and-pasting-images-using-opencv/
#https://docs.opencv.org/3.4/d4/d15/group__videoio__flags__base.html
import numpy as np
import cv2 as cv
import math

color_blue = (255,0,0)
color_yellow = (0,255,255)

testFiles = ['turtle03', 'turtle04', 'turtle05', 'turtle06']
def findRectangle( imgfile ):
    hsv_min = np.array((0, 101, 69), np.uint8)
    hsv_max = np.array((7, 253, 220), np.uint8)
    fn = './imgTurtle/'+imgfile+'.jpg'
    img = cv.imread(fn)

    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    thresh = cv.inRange(hsv, hsv_min, hsv_max)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        rect = cv.minAreaRect(cnt)
        box = cv.boxPoints(rect)
        area = int(rect[1][0] * rect[1][1])
        if area > 21500:
            box = np.int64(box)
            x = int(rect[0][0])
            y = int(rect[0][1])
            center = ( x, y)
            cv.circle(img, center, 5, color_yellow, 2)
            cv.drawContours(img, [box], 0, (255, 0, 0), 2)

            print(y)
            if (x> 600):
                flarr = 'mvRT'
            elif (x < 100):
                flarr = 'mvLF'
            else:
                print("yy")
                if (y<100):
                    flarr = 'mvFW'
                elif (y>400):
                    flarr = 'mvBW'
                else:
                    flarr = 'mvSTOP'
            imgArrow = cv.imread('./imgTurtle/move/'+flarr+'.jpg')

            img1 = cv.resize(img, (800, 600))
            img2 = cv.resize(imgArrow, (800, 600))
            imgRes = cv.addWeighted(img1, 0.5, img2, 0.5, 0.0)
            edge1 = np.int64((box[1][0] - box[0][0], box[1][1] - box[0][1]))
            edge2 = np.int64((box[2][0] - box[1][0], box[2][1] - box[1][1]))

            usedEdge = edge1
            if cv.norm(edge2) > cv.norm(edge1):
                usedEdge = edge2
            reference = (1, 0)  # vector horizont

            angle = 180.0 / math.pi * math.acos(
                (reference[0] * usedEdge[0] + reference[1] * usedEdge[1]) / (cv.norm(reference) * cv.norm(usedEdge)))
    cv.imshow('direction', imgRes)
#def findRectangle

def findRectangle1( img ):
    hsv_min = np.array(( 36,  85, 115), np.uint8)
    hsv_max = np.array((135, 255, 255), np.uint8)
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    thresh = cv.inRange(hsv, hsv_min, hsv_max)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    if ( len(contours) > 4 ):
        pass
#        return
    for cnt in contours:
        rect = cv.minAreaRect(cnt)
        box = cv.boxPoints(rect)
        area = int(rect[1][0] * rect[1][1])
        if area > 250 and area < 45000:
            box = np.int64(box)
            x = int(rect[0][0])
            y = int(rect[0][1])
            center = ( x, y)
            cv.circle(img, center, 5, color_yellow, 2)
            cv.drawContours(img, [box], 0, (255, 0, 0), 2)

            print("-----------------")
            print(x)
            print(y)
            if (x> 400):
                flarr = 'mvRT'
            elif (x < 200):
                flarr = 'mvLF'
            else:
                if (y< 90):
                    flarr = 'mvFW'
                elif (y>300):
                    flarr = 'mvBW'
                else:
                    flarr = 'mvSTOP'
            imgArrow = cv.imread('./imgTurtle/move/'+flarr+'.jpg')

            img1 = cv.resize(img, (800, 600))
            img2 = cv.resize(imgArrow, (800, 600))
            global imgRes
            imgRes = cv.addWeighted(img1, 0.5, img2, 0.5, 0.0)
            edge1 = np.int64((box[1][0] - box[0][0], box[1][1] - box[0][1]))
            edge2 = np.int64((box[2][0] - box[1][0], box[2][1] - box[1][1]))

            usedEdge = edge1
            if cv.norm(edge2) > cv.norm(edge1):
                usedEdge = edge2
            reference = (1, 0)  # vector horizont

            angle = 180.0 / math.pi * math.acos(
                (reference[0] * usedEdge[0] + reference[1] * usedEdge[1]) / (cv.norm(reference) * cv.norm(usedEdge)))
            win_ctrl = 'direction'
            w = 640
            h = 480
            cv.imshow(win_ctrl, cv.resize(imgRes, (w, h)))
            cv.resizeWindow(win_ctrl, w, h)
            cv.moveWindow(win_ctrl, 340, 0)
        else: # if area >
            win_epmty = 'empty'
            cv.imshow(win_epmty, cv.resize(img, (320, 240)))
            cv.resizeWindow(win_epmty, 320, 240)
            cv.moveWindow(win_epmty, 0, 0)
#            print("empty")
#            print(area)
#def findRectangle1

if __name__ == '__main__':
#    for testimg in testFiles:
#        print(testimg)
#        findRectangle(testimg)
#        cv.waitKey()
    cap = cv.VideoCapture("http://192.168.100.7:8080/video")
    cap.set(cv.CAP_PROP_FPS,3)
    if cap.isOpened():
        while cap.isOpened():
            ret, frame = cap.read()
            if frame is None:
                break
            if ret:
                image = cv.flip(frame, 0)
#                cv.imshow('direction', frame)
                findRectangle1(image)
            key = cv.waitKey(30)
            if key & 0xFF == ord('q') or key == 27:
                break
        cap.release()
        cv.destroyAllWindows()
    else:
        print("Cannot open camera")
