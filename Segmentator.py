from tkinter import *
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import cv2
import numpy as np
import imutils


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

        self.root.mainloop()

    def select_image(self):
        path = filedialog.askopenfilename()
        if len(path) > 0:
            self.image_processor.set_image(path)

    def add_image_process_button(self):
        check_canny_button = Checkbutton(self.root, text="Canny Transform", command=self.add_canny_buttons)
        check_canny_button.pack(side="bottom", fill="both", padx="10", pady="10")

    def add_canny_buttons(self):
        canny_buttons = []
        # TODO test canny scale with variable
        # TODO need to call a function to update output not just changing a variable
        canny_buttons.append(Scale(self.root, from_=0, to=200, orient=HORIZONTAL, label="Thresold 1", variable=self.image_processor.Canny_threshold1))
        canny_buttons.append(Scale(self.root, from_=0, to=200, orient=HORIZONTAL, label="Thresold 2", variable=self.image_processor.Canny_threshold2))
        canny_buttons.append(Scale(self.root, from_=3, to=7, orient=HORIZONTAL, label="Aperture size", variable=self.image_processor.Canny_aperture_size))
        canny_buttons.append(Scale(self.root, from_=0, to=200, orient=HORIZONTAL, label="gradient", variable=self.image_processor.Canny_gradient))
        for button in canny_buttons:
            button.pack()
        self.image_processor.change_canny_state()
        self.image_processor.process_output()

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
        self.Canny_threshold1 = IntVar(self.main_window.root, 200)
        self.Canny_threshold2 = IntVar(self.main_window.root, 200)
        self.Canny_aperture_size = IntVar(self.main_window.root, 5)
        self.Canny_gradient = IntVar(self.main_window.root, 200)

    def set_image(self, path_to_image):
        self.image_cv = cv2.imread(path_to_image)
        self.resize_image()
        self.process_output()

    def change_canny_state(self):
        if self.do_canny_transform not in self.transformation_to_do:
            self.transformation_to_do.append(self.do_canny_transform)
        else:
            for index, transfo in enumerate(self.transformation_to_do):
                if transfo == self.do_canny_transform:
                    del self.transformation_to_do[index]

    def do_canny_transform(self):
        self.output_cv = cv2.Canny(self.image_cv, self.Canny_threshold1.get(), self.Canny_threshold2.get(), None, self.Canny_aperture_size.get(), self.Canny_gradient.get())

    def resize_image(self):
        if np.shape(self.image_cv)[0] > 800:
            self.image_cv = imutils.resize(self.image_cv, width=800)
        if np.shape(self.image_cv)[1] > 600:
            self.image_cv = imutils.resize(self.image_cv, height=600)

    def process_output(self):
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
