import numpy as np


class EventHandler:
    def __init__(self, main_window):
        self.main_window = main_window
        self.fill_click = False
        self.fill_points = []

    def click_fill_event(self):
        if self.fill_click:
            self.fill_click = False
            self.main_window.image_processing_methods[2].color_buttons[1].config(relief="raised")
        else:
            self.fill_click = True
            self.main_window.image_processing_methods[2].color_buttons[1].config(relief="sunken")

    def click_event(self, event):
        if self.fill_click:
            print(np.shape(self.main_window.image_processor.output_cv))
            print(event.x, event.y)
            if event.x < np.shape(self.main_window.image_processor.output_cv)[1] and event.y < np.shape(self.main_window.image_processor.output_cv)[0]:
                self.fill_points.append((event.x, event.y))
                print(event)
                print(self.fill_points)
                self.main_window.image_processor.process_output()

    def clean(self):
        self.fill_points = []
        self.main_window.image_processor.process_output()
