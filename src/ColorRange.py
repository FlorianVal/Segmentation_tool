from tkinter import *
from types import MethodType
import cv2
import numpy as np

class ColorRange:
    def __init__(self, root, frame_list, image_processor):
        self.root = root
        self.image_processor = image_processor
        self.is_color_range_buttons = False
        self.frame_list = frame_list

        self.image_processor.lower_R = IntVar(self.root, 255)
        self.image_processor.lower_G = IntVar(self.root, 255)
        self.image_processor.lower_B = IntVar(self.root, 255)
        self.image_processor.upper_R = IntVar(self.root, 255)
        self.image_processor.upper_G = IntVar(self.root, 255)
        self.image_processor.upper_B = IntVar(self.root, 255)

        self.image_processor.change_color_range_state = MethodType(change_color_range_state, self.image_processor)
        self.image_processor.do_color_range_transform = MethodType(do_color_range_transform, self.image_processor)

        self.color_range_buttons = []
        self.color_range_buttons.append(Scale(self.frame_list[1], from_=0, to=255, orient=HORIZONTAL, label="Lower R",
                                        variable=self.image_processor.lower_R, command=self.image_processor.process_output))
        self.color_range_buttons.append(Scale(self.frame_list[1], from_=0, to=255, orient=HORIZONTAL, label="Lower G",
                                        variable=self.image_processor.lower_G, command=self.image_processor.process_output))
        self.color_range_buttons.append(Scale(self.frame_list[1], from_=0, to=255, orient=HORIZONTAL, label="Lower B",
                                        variable=self.image_processor.lower_B, command=self.image_processor.process_output))

        self.color_range_buttons.append(Scale(self.frame_list[1], from_=0, to=255, orient=HORIZONTAL, label="upper R",
                                        variable=self.image_processor.upper_R, command=self.image_processor.process_output))
        self.color_range_buttons.append(Scale(self.frame_list[1], from_=0, to=255, orient=HORIZONTAL, label="upper G",
                                        variable=self.image_processor.upper_G, command=self.image_processor.process_output))
        self.color_range_buttons.append(Scale(self.frame_list[1], from_=0, to=255, orient=HORIZONTAL, label="upper B",
                                        variable=self.image_processor.upper_B, command=self.image_processor.process_output))


    def add_main_button(self):
        check_color_range_intvar = IntVar()
        check_color_range_button = Checkbutton(self.frame_list[0], text="Color range", command=self.show_color_range_options, variable=check_color_range_intvar)
        check_color_range_button.pack(side="top", fill="both", padx="10", pady="10")

    def show_color_range_options(self):
        if self.is_color_range_buttons:
            self.is_color_range_buttons = False
            for button in self.color_range_buttons:
                button.pack_forget()
        else:
            self.is_color_range_buttons = True
            for button in self.color_range_buttons:
                button.pack(side="top", fill="both", padx="10", pady="10")
        self.image_processor.change_color_range_state()
        self.image_processor.process_output()


# Methods to add to image processing
# add color_range transform to transformation to do list
def change_color_range_state(self):
    if self.do_color_range_transform not in self.transformation_to_do:
        self.transformation_to_do.append(self.do_color_range_transform)
    else:
        for index, transfo in enumerate(self.transformation_to_do):
            if transfo == self.do_color_range_transform:
                del self.transformation_to_do[index]


def do_color_range_transform(self):
    lower = np.array([self.lower_R.get(), self.lower_G.get(), self.lower_B.get()], dtype=np.uint8)
    upper = np.array([self.upper_R.get(), self.upper_G.get(), self.upper_B.get()], dtype=np.uint8)
    self.output_cv = cv2.inRange(self.output_cv, lower, upper)
