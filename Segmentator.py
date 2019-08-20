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

        self.next_button_coord_row = []
        self.next_button_coord_row.append(1)
        self.next_button_coord_row.append(1)
        self.next_button_coord_row.append(1)

        panelA = None
        panelB = None

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.left_frame = Frame(self.root, bg='cyan')
        self.right_frame = Frame(self.root, width=250)

        self.image_select_button = Button(self.root, text="Select an image", command=self.select_image)
        self.image_select_button.grid(row=0, column=0, sticky="nesw")

        self.image_processing_methods = []
        self.image_processing_methods.append(Canny.Canny(self.root, self.image_processor, self))
        self.image_processing_methods.append(MorphTransform.MorphTransform(self.root, self.image_processor, self))

        self.root.mainloop()

    def select_image(self):
        # path = filedialog.askopenfilename()
        # DEBUG
        path = "/workspace/workspace/hammer.jpg"
        if len(path) > 0:
            self.image_processor.set_image(path)

    def add_image_process_button(self):
        # called when an image is selected to display buttons
        for processor in self.image_processing_methods:
            # column 0 for main buttons
            processor.add_main_button(self.next_button_coord_row[0], 0)
            # TODO blinde if x > grid size
            self.next_button_coord_row[0] += 1

    def grid_configure(self):
        self.root.geometry("800x600")
        self.right_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(1, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)

        for x in range(10):
            self.left_frame.grid_columnconfigure(x, weight=1)
        for y in range(10):
            self.left_frame.grid_rowconfigure(y, weight=1)

    def display_images(self):
        if self.panelA is None or self.panelB is None:
            self.right_frame.grid(column=1, sticky="e")
            self.left_frame.grid(column=0)

            self.panelA = Label(self.right_frame, image=self.image_processor.image_to_display)
            self.panelA.image = self.image_processor.image_to_display
            self.panelA.grid(row=0, column=0, sticky="ne")

            self.panelB = Label(self.right_frame, image=self.image_processor.output_to_display)
            self.panelB.image = self.image_processor.output_to_display
            self.panelB.grid(row=1, column=0, sticky="se")

            self.image_select_button.grid(self.left_frame, row=0, column=2, sticky="nsew")
            self.grid_configure()
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

        self.image_to_display = ImageTk.PhotoImage(Image.fromarray(image_cv_tmp).resize((250, 250)))
        self.output_to_display = ImageTk.PhotoImage(Image.fromarray(self.output_cv).resize((250, 250)))
        self.main_window.display_images()

    def __del__(self):
        print("Destroying image processing")


if __name__ == '__main__':
    MainWindow()
