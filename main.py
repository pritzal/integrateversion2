import cv2
from PIL import Image

from utils import get_limits


class ObjectDetector:
    def __init__(self, color):
        self.color = color
        self.cap = cv2.VideoCapture(0)

    def detect(self):
        ret, frame = self.cap.read()

        hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lowerLimit, upperLimit = get_limits(color=self.color)

        mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)

        mask_ = Image.fromarray(mask)

        bbox = mask_.getbbox()

        if bbox is not None:
            x1, y1, x2, y2 = bbox

            frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 5)

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.cap.release()
            cv2.destroyAllWindows()
            return False

        return True


class DimensionExtractor:
    def __init__(self):
        self.webcam = True
        self.path = '1.jpg'
        self.cap = cv2.VideoCapture(0)
        self.cap.set(10, 160)
        self.cap.set(3, 1920)
        self.cap.set(4, 1080)
        self.scale = 3
        self.wP = 210 * self.scale
        self.hP = 297 * self.scale

    def extract(self):
        if self.webcam:
            success, img = self.cap.read()
        else:
            img = cv2.imread(self.path)

        imgContours, conts = utlis.getContours(img, minArea=50000, filter=4)
        if len(conts) != 0:
            biggest = conts[0][2]
            # print(biggest)
            imgWarp = utlis.warpImg(img, biggest, self.wP, self.hP)
            imgContours2, conts2 = utlis.getContours(imgWarp,
                                                     minArea=2000, filter=4,
                                                     cThr=[50, 50], draw=False)
            if len(conts) != 0:
                for obj in conts2:
                    cv2.polylines(imgContours2, [obj[2]], True, (0, 255, 0), 2)
                    nPoints = utlis.reorder(obj[2])
                    nW = round((utlis.findDis(nPoints[0][0] // self.scale, nPoints[1][0][0] // self.scale) / 10), 1)
                    nH = round((utlis.findDis(nPoints[0][0] // self.scale, nPoints[2][0][0] // self.scale) / 10), 1)
                    cv2.arrowedLine(imgContours2, (nPoints[0][0][0], nPoints[0][0][1]),
                                    (nPoints[1][0][0], nPoints[1][0][1]),
                                    (255, 0, 255), 3, 8, 0, 0.05)
                    cv2.arrowedLine(imgContours2, (nPoints[0][0][0], nPoints[0][0][1]),
                                    (nPoints[2][0][0], nPoints[2][0][1]),
                                    (255, 0, 255), 3, 8, 0,)

