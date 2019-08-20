import cv2
import tkinter as tk
from threading import Thread
import time
##
##Not working
##

class Menu(Thread):
    def __init__(self, ImageResult):
        Thread.__init__(self)
        self.window_name = "Segmentator"
        self.window = None
        self.hough_button = None
        self.result_window = ImageResult
        self.canny_transform = None

    def build_window(self):
        self.window = tk.Tk()
        self.window.title(self.window_name)
        self.canny_transform = tk.BooleanVar()
        self.hough_button = tk.Checkbutton(self.window, variable=self.canny_transform, text="Canny Transform", command=self.canny_button_pressed)
        self.hough_button.pack()

    def canny_button_pressed(self):
        if self.canny_transform.get():
            self.result_window.set_canny()

    def run(self):
        self.build_window()
        self.window.mainloop()
        # Close image window if menu closed
        self.result_window.exit = True

    def __del__(self):
        self.window.quit()
        print("Menu Destructor called")


class ImageResult(Thread):
    def __init__(self, path_to_image="20180918_141930.jpg"):
        Thread.__init__(self)
        self.window_name = "Segmentato"
        self.base_image = cv2.resize(cv2.imread(path_to_image), (800, 600))
        self.result = self.base_image
        self.use_hough = False
        self.exit = False

    def set_canny(self):
        if not self.use_hough:
            print('ok')
            self.use_hough = True
        else:
            self.use_hough = False

    def show(self):
        cv2.imshow(self.window_name, self.result)

    def run(self):
        while 1:
            self.show()
            k = cv2.waitKey(1)
            if self.exit:
                break

    def __del__(self):
        cv2.destroyAllWindows()
        print("ImageResult Destructor called")


def main():
    image_res = ImageResult()
    ui = Menu(image_res)
    image_res.start()
    ui.start()
    print("ui run")
    ui.join()
    image_res.join()


if __name__ == '__main__':
    main()
