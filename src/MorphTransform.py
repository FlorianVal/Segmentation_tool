from tkinter import *
from types import MethodType
import cv2
import numpy as np


class MorphTransform:
    def __init__(self, root, image_processor):
        self.root = root
        self.image_processor = image_processor
        self.is_morph_transform_buttons = False

        self.image_processor.morph_kernel = np.ones((5, 5), np.uint8)
        self.image_processor.iteration_number = IntVar(self.root, 1)

        self.morph_check_buttons = []
        self.morph_check_buttons.append(Checkbutton(self.root, text="Erosion", command=self.image_processor.process_output))

    def add_main_button(self):
        check_morph_button = Checkbutton(self.root, text="Morphological Transform", command=self.show_morph_options)
        check_morph_button.pack(side="bottom", fill="both", padx="10", pady="10")

    def show_morph_options(self):
        if self.is_morph_transform_buttons:
            self.is_morph_transform_buttons = False
            for button in self.morph_check_buttons:
                button.pack_forget()
        else:
            self.is_morph_transform_buttons = True
            for button in self.morph_check_buttons:
                button.pack(side="bottom", fill="both", padx="10", pady="10")
