from tkinter import *
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import cv2
import numpy as np
import imutils
from src import *

class MainWindow:
    def __init__(self):
        self.root = Tk()
        self.panelA = None
        self.panelB = None
        self.image_processor = ImageProcessing(self)

        panelA = None
        panelB = None

        image_select_button = Button(self.root, text="Select an image", command=self.select_image)
        image_select_button.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

        self.image_processing_methods = []
        self.image_processing_methods.append(Canny.Canny(self.root, self.image_processor))
        self.image_processing_methods.append(MorphTransform.MorphTransform(self.root, self.image_processor))

        self.root.mainloop()

    def select_image(self):
        path = filedialog.askopenfilename()
        if len(path) > 0:
            self.image_processor.set_image(path)

    def add_image_process_button(self):
        # called when an image is selected to display buttons
        for processor in self.image_processing_methods:
            processor.add_main_button()

    def display_images(self):
        if self.panelA is None or self.panelB is None:
            self.panelA = Label(image=self.image_processor.image_to_display)
            self.panelA.image = self.image_processor.image_to_display
            self.panelA.pack(side="left", padx=10, pady=10)

            self.panelB = Label(image=self.image_processor.output_to_display)
            self.panelB.image = self.image_processor.output_to_display
            self.panelB.pack(side="right", padx=10, pady=10)

            self.add_image_process_button()
        else:
            # TODO when changing image fix window size
            # update the pannels
            self.panelA.configure(image=self.image_processor.image_to_display)
            self.panelB.configure(image=self.image_processor.output_to_display)
            self.panelA.image = self.image_processor.image_to_display
            self.panelB.image = self.image_processor.output_to_display

    def __del__(self):
        print("Destroying window")


class ImageProcessing:
    def __init__(self, MainWindow):
        self.main_window = MainWindow

        self.image_cv = None
        self.image_to_display = None
        self.output_cv = None
        self.output_to_display = None

        self.transformation_to_do = []

    def set_image(self, path_to_image):
        self.image_cv = cv2.imread(path_to_image)
        self.resize_image()
        self.process_output()

    def resize_image(self):
        if np.shape(self.image_cv)[0] > 800:
            self.image_cv = imutils.resize(self.image_cv, width=800)
        if np.shape(self.image_cv)[1] > 600:
            self.image_cv = imutils.resize(self.image_cv, height=600)

    def process_output(self, args=None):
        self.output_cv = self.image_cv
        if len(self.transformation_to_do) > 0:
            for transformation in self.transformation_to_do:
                transformation()
        self.convert_images()

    def convert_images(self):
        image_cv_tmp = cv2.cvtColor(self.image_cv, cv2.COLOR_BGR2RGB)
        # self.output_cv = cv2.cvtColor(self.output_cv, cv2.COLOR_BGR2RGB)

        self.image_to_display = ImageTk.PhotoImage(Image.fromarray(image_cv_tmp))
        self.output_to_display = ImageTk.PhotoImage(Image.fromarray(self.output_cv))
        self.main_window.display_images()

    def __del__(self):
        print("Destroying image processing")


if __name__ == '__main__':
    MainWindow()
