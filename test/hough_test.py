import cv2 as cv
import math
import numpy as np
import fire
import os
import random as rng


def make_contour_circle(image):
    _, contours, _ = cv.findContours(image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    if len(contours) < 10:
        # Find the rotated rectangles and ellipses for each contour
        for i, c in enumerate(contours):
            (x, y), radius = cv.minEnclosingCircle(c)
            center = (int(x), int(y))
            radius = int(radius)
            cv.circle(image, center, radius, (255, 255, 255), -1)


class ClassImage:
    def __init__(self, img: np.ndarray, window_name: str = "image"):
        self.result = img
        self.result_canny = img
        self.result_color = img
        self.result_circle = img
        self.img = img
        self.thr = 0
        self.min_length = 0
        self.max_distance = 0
        self.param1_circle = 50
        self.param2_circle = 30
        self.min_radius = 0
        self.max_radius = 0
        self.min_dist = 1
        self.dp = 20
        self.Canny_threshold1 = 300
        self.Canny_threshold2 = 500
        self.Canny_aperture_size = 5
        self.Canny_gradient = 0
        self.Color = [120, 120, 120]
        self.Color_width = 10
        self.window_name = window_name
        self.result = self.update(self.img)
        self.result_canny = self.update_canny(self.img)
        self.result_color = self.update_color(self.img)
        self.result_circle = self.update_circle(self.img)

    def set_color(self, color):
        self.Color = color

    def get_img(self):
        return self.img

    def get_result_hough(self):
        return self.result

    def get_result_color(self):
        return self.result_color

    def get_result_circle(self):
        return self.result_circle

    def get_result_canny(self):
        return self.result_canny

    def set_thr(self, thr):
        self.thr = thr
        self.result = self.update(self.img)

    def set_min(self, min_length):
        self.min_length = min_length
        self.result = self.update(self.img)

    def set_max_distance(self, max_distance):
        self.max_distance = max_distance
        self.result = self.update(self.img)

    def set_color_width(self, color_width):
        self.Color_width = color_width
        self.update_color(self.img)

    def update_color(self, img):
        lower = np.array([x - self.Color_width for x in self.Color])
        upper = np.array([x + self.Color_width for x in self.Color])
        mask = cv.inRange(img, lower, upper)
        kernel = np.ones((4, 4), np.uint8)
        mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)
        make_contour_circle(mask)
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
        # make_contour_circle(mask)
        result = cv.bitwise_and(img, img, mask=mask)
        # result = mask
        # result, contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        self.result_color = result
        cv.imshow(self.window_name, self.result_color)
        return result

    def update(self, img):
        dst = cv.Canny(img, self.Canny_threshold1, self.Canny_threshold2, None, self.Canny_aperture_size)
        result = np.ndarray.copy(img)
        lines = cv.HoughLinesP(dst, 1, np.pi / 180, self.thr, None, self.min_length, self.max_distance)
        if lines is not None:
            for i in range(0, len(lines)):
                line = lines[i][0]
                # angle = math.atan2(line[3] - line[1], line[2] - line[0]) * 180 / math.pi
                # if angle > 85 or angle < -85:
                cv.line(result, (line[0], line[1]), (line[2], line[3]), (0, 0, 255), 3, cv.LINE_AA)
                continue
        else:
            print("No lines found")
        self.result = result
        cv.imshow(self.window_name, self.result)
        return result

    def update_canny(self, img):
        result = cv.Canny(img, self.Canny_threshold1, self.Canny_threshold2, None, self.Canny_aperture_size,
                          self.Canny_gradient)
        self.result_canny = result
        cv.imshow(self.window_name, self.result_canny)

        return result

    def set_param1(self, arg):
        self.param1_circle = arg
        self.update_circle(self.img)

    def set_param2(self, arg):
        self.param2_circle = arg
        self.update_circle(self.img)

    def set_min_dist(self, arg):
        self.min_dist = arg
        self.update_circle(self.img)

    def set_min_radius(self, arg):
        self.min_radius = arg
        self.update_circle(self.img)

    def set_max_radius(self, arg):
        self.max_radius = arg
        self.update_circle(self.img)

    def set_dp(self, arg):
        self.dp = arg
        self.update_circle(self.img)

    def update_circle(self, img):
        mask = np.ones((np.shape(img)[0], np.shape(img)[1]), np.uint8)
        img1 = cv.medianBlur(img, 5)
        cimg = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)

        circles = cv.HoughCircles(cimg, cv.HOUGH_GRADIENT, self.min_dist, self.dp,
                                  param1=self.param1_circle, param2=self.param2_circle, minRadius=self.min_radius, maxRadius=self.max_radius)
        try:

            if len(circles) < 10:
                circles = np.uint16(np.around(circles))
                for i in circles[0, :]:
                    # draw the outer circle
                    cv.circle(mask, (i[0], i[1]), i[2], (0, 0, 0), 2)
                    # draw the center of the circle
                    cv.circle(mask, (i[0], i[1]), 2, (0, 0, 0), 3)

            result = cv.bitwise_and(img, img, mask=mask)

        except AttributeError or TypeError:
            print("no circle ", circles)
        self.result_circle = result
        cv.imshow(self.window_name, result)

        return result

    def set_canny1(self, canny1):
        self.Canny_threshold1 = canny1
        self.result_canny = self.update_canny(self.img)

    def set_canny2(self, canny2):
        self.Canny_threshold2 = canny2
        self.result_canny = self.update_canny(self.img)

    def set_canny3(self, canny3):
        if canny3 == 0:
            canny3 = 3
        if canny3 == 1:
            canny3 = 5
        if canny3 == 2:
            canny3 = 7
        self.Canny_aperture_size = canny3
        self.result_canny = self.update_canny(self.img)

    def set_canny_gradient(self, gradient):
        self.Canny_gradient = gradient
        self.result_canny = self.update_canny(self.img)


class EventHandler:
    def __init__(self, ClassImage):
        self.classimg = ClassImage

    def pick_color(self, event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDOWN:
            self.classimg.Color = self.classimg.img[y, x]
            self.classimg.update_color(self.classimg.img)


class Window:
    def __init__(self, img, windown_name, type, image_name):
        self.image = ClassImage(img, windown_name)
        self.window_name = windown_name
        self.type = type
        self.image_name = image_name
        event_handler = EventHandler(self.image)
        if type == "circle_hough":
            cv.imshow(windown_name, self.image.result_circle)
            cv.createTrackbar("param1", windown_name, self.image.param1_circle, 600, self.image.set_param1)
            cv.createTrackbar("param2", windown_name, self.image.param2_circle, 600, self.image.set_param2)
            cv.createTrackbar("min radius", windown_name, self.image.min_radius, 600, self.image.set_min_radius)
            cv.createTrackbar("max radius", windown_name, self.image.max_radius, 600, self.image.set_max_radius)
            cv.createTrackbar("min dist", windown_name, self.image.min_dist, 600, self.image.set_min_dist)
            cv.createTrackbar("dp", windown_name, self.image.dp, 600, self.image.set_dp)
            self.update_function = self.image.update_circle
            self.result = self.image.get_result_circle

        if type == "hough":
            cv.imshow(windown_name, self.image.result)
            cv.createTrackbar("Threshold", windown_name, self.image.thr, 600, self.image.set_thr)
            cv.createTrackbar("min length", windown_name, self.image.min_length, max(self.image.img.shape[0], self.image.img.shape[1]), self.image.set_min)
            cv.createTrackbar("max dist", windown_name, self.image.max_distance, max(self.image.img.shape[0], self.image.img.shape[1]),
                              self.image.set_max_distance)
            self.update_function = self.image.update
            self.result = self.image.get_result_hough

        if type == "color":
            cv.imshow(windown_name, self.image.result_color)
            cv.setMouseCallback(self.window_name, event_handler.pick_color)
            cv.createTrackbar("color Width", windown_name, self.image.Color_width, 255, self.image.set_color_width)
            self.update_function = self.image.update_color
            self.result = self.image.get_result_color

        if type == "canny":
            cv.imshow(windown_name, self.image.result_canny)
            cv.createTrackbar("1", windown_name, self.image.Canny_threshold1, 10000, self.image.set_canny1)
            cv.createTrackbar("2", windown_name, self.image.Canny_threshold2, 10000, self.image.set_canny2)
            cv.createTrackbar("3", windown_name, self.image.Canny_aperture_size, 2, self.image.set_canny3)
            cv.createTrackbar("gradient", windown_name, self.image.Canny_gradient, 1, self.image.set_canny_gradient)
            self.update_function = self.image.update_canny()
            self.result = self.image.get_result_canny

    def set_img(self, image, image_name):
        self.image.img = image
        self.image_name = image_name
        self.update_function(image)

    def get_mask(self):
        return self.result()


def main(path_to_img="/home/florian/Pictures/20180918_141930.jpg"):
    files = []
    image_size = (800, 600)
    file_index = 0
    if os.path.isfile(path_to_img):
        im = cv.imread(path_to_img)
    else:
        for r, d, f in os.walk(path_to_img):
            f.sort()
            for file in f:
                if '.jpg' or '.png' in file:
                    files.append(os.path.join(r, file))
        im = cv.imread(files[0])
    im = cv.resize(im, image_size)
    windows = []
    windows.append(Window(im, "Color", "color", files[0].split("/")[-1]))
    # windows.append(Window(im, "Circle Hough", "circle_hough"))
    while True:
        key = cv.waitKey(1) & 0xFF
        if key == ord("c"):
            break
        try:
            if key == ord("n"):
                file_index += 1
                im = cv.imread(files[file_index])
                im = cv.resize(im, image_size)
                for window in windows:
                    window.set_img(im, files[file_index].split("/")[-1])
            if key == ord("b"):
                file_index -= 1
                im = cv.imread(files[file_index])
                im = cv.resize(im, image_size)
                for window in windows:
                    window.set_img(im, files[file_index].split("/")[-1])
        except IndexError:
            print("no more images")
            file_index = 0
    cv.destroyAllWindows()


if __name__ == '__main__':
    fire.Fire(main)
