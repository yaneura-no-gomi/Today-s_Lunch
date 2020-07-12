from PIL import Image
import cv2
import numpy as np
from pprint import pprint


class ImageCroper:
    def __init__(self, img_path):
        self.img_path = img_path
        self.img = cv2.imread(img_path)

    def extract_lines(self):

        # Grayscale Conversion & Negative Positive Conversion
        img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        ret, img_thresh = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)
        img = cv2.bitwise_not(img_thresh)

        # Lines Detection by Hough Conversion
        lines = cv2.HoughLinesP(
            img, rho=1, theta=np.pi / 360, threshold=80, minLineLength=250, maxLineGap=5
        )

        self.lines = [line[0] for line in lines]

    def check_lines(self):
        for line in self.lines:
            x1, y1, x2, y2 = line
            # 赤線を引く
            red_line_img = cv2.line(self.img, (x1, y1), (x2, y2), (0, 0, 255), 3)
            cv2.imwrite("check_lines.png", red_line_img)

    def eliminate_close_element(self, l):
        rm = []
        for i in range(len(l)):
            if l[i] not in rm:
                for j in range(i + 1, len(l)):
                    if l[j] not in rm and (l[i] - l[j]) ** 2 < 4:
                        rm.append(l[j])

        removed_l = [e for e in l if e not in rm]

        return removed_l

    def crop_by_frame(self):
        """
        Find the coordinates of the required intersection points
        """

        # Find the coordinates of the required intersection points
        vertical = []
        horizontal = []
        for line in self.lines:
            if line[0] == line[2]:
                # vertical line
                vertical.append(line[0])

            elif line[1] == line[3]:
                # horizontal line
                horizontal.append(line[1])

        # Close elements are eliminated
        vertical = self.eliminate_close_element(sorted(vertical))
        horizontal = self.eliminate_close_element(sorted(horizontal))

        pprint(vertical)
        pprint(horizontal)

        # Croping 
        croped_imgs = dict()
        for i, day in enumerate(["mon", "tue", "wed", "thu", "fri", "sat"]):
            _ = self.img[:, vertical[i] : vertical[i + 1]]
            cv2.imwrite("result/" + day + ".png", _)
            croped_imgs[day] = self.img[:, vertical[i] : vertical[i + 1]]

        for k, v in croped_imgs.items():
            _ = []
            for i in range(len(horizontal) - 1):
                if i!=0:
                    _.append(v[horizontal[i] : horizontal[i + 1], :])
            v = _

        return croped_imgs


def main():

    img_path = "2.jpg"
    croper = ImageCroper(img_path)
    croper.extract_lines()
    # croper.check_lines()
    croper.crop_by_frame()


if __name__ == "__main__":
    main()