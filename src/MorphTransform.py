from tkinter import *
from types import MethodType
import cv2
import numpy as np


class MorphTransform:
    def __init__(self, root, frame_list, image_processor):
        self.frame_list = frame_list
        self.root = root
        self.image_processor = image_processor
        self.is_morph_transform_buttons = False
        self.transformation_name_list = ["Erosion", "Dilation", "Opening", "Closing"]
        self.morph_function = [do_erosion, do_dilation, do_opening, do_closing]
        self.image_processor.morph_kernel = np.ones((5, 5), np.uint8)
        self.image_processor.iteration_number = IntVar(self.root, 1)
        self.morph_scale_sub_button = Scale(self.frame_list[2], from_=0, to=50, orient=HORIZONTAL, label="Iteration",
                                            variable=self.image_processor.iteration_number, command=self.image_processor.process_output)

        self.image_processor.add_morph = MethodType(add_morph, self.image_processor)
        self.image_processor.del_morph = MethodType(del_morph, self.image_processor)
        self.image_processor.do_erosion = MethodType(do_erosion, self.image_processor)
        self.image_processor.do_dilation = MethodType(do_dilation, self.image_processor)
        self.image_processor.do_closing = MethodType(do_closing, self.image_processor)
        self.image_processor.do_opening = MethodType(do_opening, self.image_processor)

        self.morph_function = [self.image_processor.do_erosion, self.image_processor.do_dilation, self.image_processor.do_opening, self.image_processor.do_closing]

        self.morph_check_buttons = []
        self.morph_check_intvar = []

        for i, name in enumerate(self.transformation_name_list):
            self.morph_check_intvar.append(IntVar())
            if name == "Erosion" or name == "Dilation":
                self.morph_check_buttons.append(
                    Checkbutton(self.frame_list[1], text=name, command=self.show_morph_sub_options, variable=self.morph_check_intvar[i]))
            else:
                self.morph_check_buttons.append(Checkbutton(self.frame_list[1], text=name, command=self.add_to_transformation, variable=self.morph_check_intvar[i]))

    def add_main_button(self):
        check_morph_intvar = IntVar()
        check_morph_button = Checkbutton(self.frame_list[0], text="Morphological Transform", command=self.show_morph_options, variable=check_morph_intvar)
        check_morph_button.pack(side="top", fill="both", padx="10", pady="10")

    def show_morph_options(self):
        # show / hide options
        if self.is_morph_transform_buttons:
            self.is_morph_transform_buttons = False
            for button in self.morph_check_buttons:
                button.pack_forget()
        else:
            self.is_morph_transform_buttons = True
            for button in self.morph_check_buttons:
                button.pack(side="top", fill="both", padx="10", pady="10")

    def show_morph_sub_options(self):
        # show only if reosion or dilation is on
        if self.morph_check_intvar[0].get() == 0 and self.morph_check_intvar[1].get() == 0:
            self.morph_scale_sub_button.pack_forget()
        else:
            self.morph_scale_sub_button.pack(side="top", fill="both", padx="10", pady="10")
        self.add_to_transformation()

    def add_to_transformation(self):
        for i in range(len(self.morph_function)):
            if self.morph_check_intvar[i].get() != 0:
                self.image_processor.add_morph(self.morph_function[i])
            else:
                self.image_processor.del_morph(self.morph_function[i])
        self.image_processor.process_output()


def add_morph(self, transformation):
    if transformation not in self.transformation_to_do:
        self.transformation_to_do.append(transformation)


def del_morph(self, transformation):
    for i, transfo_to_do in enumerate(self.transformation_to_do):
        if transfo_to_do == transformation:
            del self.transformation_to_do[i]


def do_erosion(self):
    self.output_cv = cv2.erode(self.output_cv, self.morph_kernel, iterations=self.iteration_number.get())


def do_dilation(self):
    self.output_cv = cv2.dilate(self.output_cv, self.morph_kernel, iterations=self.iteration_number.get())


def do_opening(self):
    self.output_cv = cv2.morphologyEx(self.output_cv, cv2.MORPH_OPEN, self.morph_kernel)


def do_closing(self):
    self.output_cv = cv2.morphologyEx(self.output_cv, cv2.MORPH_CLOSE, self.morph_kernel)
