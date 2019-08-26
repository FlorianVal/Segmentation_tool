from tkinter import *
from types import MethodType
import cv2


class ColorTools:
    def __init__(self, root, frame_list, image_processor, event_handler):
        self.frame_list = frame_list
        self.event_handler = event_handler
        self.root = root
        self.image_processor = image_processor

        self.image_processor.add_fill = MethodType(add_fill, self.image_processor)
        self.image_processor.do_fill = MethodType(do_fill, self.image_processor)

        self.is_options_shown = False
        self.fill_is_clicked = False

        check_fill_intvar = IntVar(self.root, 1)

        self.color_buttons = []
        self.color_buttons.append(Checkbutton(self.frame_list[1], text="Color fill", command=self.image_processor.add_fill, variable=check_fill_intvar))
        self.color_buttons.append(Button(self.frame_list[1], text="Add points", command=self.event_handler.click_fill_event))
        self.color_buttons.append(Button(self.frame_list[1], text="Clean points", command=self.event_handler.clean))

    def add_main_button(self):
        check_color_intvar = IntVar()
        check_color_button = Checkbutton(self.frame_list[0], text="Color Tools", command=self.show_options_buttons, variable=check_color_intvar)
        check_color_button.pack(side="top", fill="both", padx="10", pady="10")

    def show_options_buttons(self):
        if self.is_options_shown:
            self.is_options_shown = False
            for button in self.color_buttons:
                button.pack_forget()
        else:
            self.is_options_shown = True
            for button in self.color_buttons:
                button.pack(side="top", fill="both", padx="10", pady="10")


def add_fill(self):
    if self.do_fill not in self.transformation_to_do:
        self.transformation_to_do.append(self.do_fill)
    else:
        for i, transfo_to_do in enumerate(self.transformation_to_do):
            if transfo_to_do == self.do_fill:
                del self.transformation_to_do[i]
    self.process_output()


def do_fill(self):
    for point in self.event_handler.fill_points:
        cv2.floodFill(self.output_cv, None, point, 255)
