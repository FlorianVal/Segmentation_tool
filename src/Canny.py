from tkinter import *
from types import MethodType
import cv2


class Canny:
    def __init__(self, root, image_processor):
        self.root = root
        self.image_processor = image_processor
        self.is_canny_buttons = False

        self.image_processor.Canny_threshold1 = IntVar(self.root, 200)
        self.image_processor.Canny_threshold2 = IntVar(self.root, 200)
        self.image_processor.Canny_aperture_size = IntVar(self.root, 5)
        self.image_processor.Canny_gradient = IntVar(self.root, 200)

        self.image_processor.change_canny_state = MethodType(change_canny_state, self.image_processor)
        self.image_processor.do_canny_transform = MethodType(do_canny_transform, self.image_processor)

        self.canny_buttons = []
        self.canny_buttons.append(Scale(self.root, from_=0, to=1000, orient=HORIZONTAL, label="Thresold 1",
                                        variable=self.image_processor.Canny_threshold1, command=self.image_processor.process_output))

        self.canny_buttons.append(Scale(self.root, from_=0, to=1000, orient=HORIZONTAL, label="Thresold 2",
                                        variable=self.image_processor.Canny_threshold2, command=self.image_processor.process_output))

        self.canny_buttons.append(Scale(self.root, from_=3, to=7, orient=HORIZONTAL, label="Aperture size",
                                        variable=self.image_processor.Canny_aperture_size, command=self.image_processor.process_output))

        self.canny_buttons.append(Scale(self.root, from_=0, to=200, orient=HORIZONTAL, label="gradient",
                                        variable=self.image_processor.Canny_gradient, command=self.image_processor.process_output))

    def add_main_button(self):
        check_canny_button = Checkbutton(self.root, text="Canny Transform", command=self.show_canny_options)
        check_canny_button.pack(side="bottom", fill="both", padx="10", pady="10")

    def show_canny_options(self):
        if self.is_canny_buttons:
            self.is_canny_buttons = False
            for button in self.canny_buttons:
                button.pack_forget()
        else:
            self.is_canny_buttons = True
            for button in self.canny_buttons:
                button.pack()
        self.image_processor.change_canny_state()
        self.image_processor.process_output()


# Methods to add to image processing
def change_canny_state(self):
    if self.do_canny_transform not in self.transformation_to_do:
        self.transformation_to_do.append(self.do_canny_transform)
    else:
        for index, transfo in enumerate(self.transformation_to_do):
            if transfo == self.do_canny_transform:
                del self.transformation_to_do[index]


def do_canny_transform(self):
    self.output_cv = cv2.Canny(self.image_cv, self.Canny_threshold1.get(), self.Canny_threshold2.get(), None,
                               self.Canny_aperture_size.get(), self.Canny_gradient.get())
