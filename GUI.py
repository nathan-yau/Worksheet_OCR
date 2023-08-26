import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from PIL import Image, ImageTk
import numpy as np
import pandas as pd
import cv2
import supporting_functions
import camera_control
import worksheet_ocr
import answer_projection


class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.user_name = None
        self.font_style = "Yu Gothic UI Semibold"
        self.resizable(False, False)
        self.title("Math Homework v1.0")
        self.icon = ImageTk.PhotoImage(Image.open("icon.png"))
        self.iconphoto(False, self.icon)

        # Create Menu
        self.menu_bar = tk.Menu(self)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="LogFile", command=self.closing_event)
        self.file_menu.add_command(label="Close", command=self.closing_event)
        self.about_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(menu=self.file_menu, label="File")
        self.menu_bar.add_cascade(menu=self.about_menu, label="About")
        self.config(menu=self.menu_bar)

        # Top Frame container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        self.frames = {}
        for F in (StartPage, OptionPage, MathPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Clock Frame
        self.clock_frame = tk.Frame(self, bd=1, relief='sunken')
        self.clock_frame.pack(side="bottom", fill="both", expand=True)

        # Widgets for clock frame
        self.date = tk.Label(self.clock_frame, text=datetime.now().strftime("%d %B %Y"))
        self.date.pack(side='left', padx=10)
        self.clock = tk.Label(self.clock_frame, text=datetime.now().strftime("%H:%M:%S"))
        self.clock.pack(side='right', padx=20)
        self.update_time()

        self.protocol("WM_DELETE_WINDOW", self.closing_event)

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if page_name == "OptionPage":
            frame.update_user_name()
        elif page_name == "MathPage":
            frame.update_user_name()
            frame.after(200, frame.math_grading)

    def closing_event(self):
        if messagebox.askyesno(title="Confirm?", message="Do you confirm to quit?"):
            quit()
        if self.user_name is not None:
            supporting_functions.log_writer([self.user_name, "Logout", " "])

    def update_time(self):
        self.date.config(text=datetime.now().strftime("%d %B %Y"))
        self.clock.config(text=datetime.now().strftime("%H:%M:%S"))
        self.clock_frame.after(200, self.update_time)


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Create Picture
        self.img = ImageTk.PhotoImage(Image.open("cover_image.png").resize((600, 456)))
        self.panel = tk.Label(self, image=self.img)
        self.panel.grid(row=0, columnspan=3, sticky='we', padx=10, pady=10)

        # Create Label
        self.name_label = tk.Label(self, text="Your Name: ", font=(controller.font_style, 12))
        self.name_label.grid(row=1, column=0, sticky='we', padx=10, pady=10)

        # Create User Input Field
        self.entry = tk.Entry(self, font=(controller.font_style, 12))
        self.entry.bind("<KeyPress>", self.shortcut)
        self.entry.grid(row=1, column=1, sticky='we', padx=10, pady=10)
        self.entry.focus_set()

        # Create Button for input
        self.button = tk.Button(self, text="Enter", font=(controller.font_style, 10), command=self.get_user_name,
                                height=1, width=10)
        self.button.grid(row=1, column=2, sticky='we', padx=10, pady=10)

        # Create copyright label
        self.copyright_label = tk.Label(self, text="All rights reserved ©", font=(controller.font_style, 8))
        self.copyright_label.grid(row=2, column=2, columnspan=2, sticky='we')

    def get_user_name(self):
        name = self.entry.get()
        if len(name) == 0:
            messagebox.showinfo(title="Warning!", message="Please enter your name to continue!")
        else:
            self.controller.user_name = name.title()
            supporting_functions.log_writer([name.title(), "Login", " "])
            self.controller.show_frame("OptionPage")

    def shortcut(self, event):
        if event.keysym == "Return":
            self.get_user_name()


class OptionPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.user_frame = tk.Frame(self)
        self.user_frame.grid(row=0, column=0, sticky='we')
        self.user_frame.columnconfigure(1, weight=1)

        self.context_frame = tk.Frame(self)
        self.context_frame.grid(row=1, column=0, sticky='we')
        self.context_frame.columnconfigure(0, weight=1)
        self.context_frame.rowconfigure(1, weight=1)

        self.name_label = tk.Label(self.user_frame, text="Current User: ", font=(controller.font_style, 12))
        self.name_label.grid(row=0, column=0, sticky='w', padx=10)
        self.name = tk.Label(self.user_frame, text=controller.user_name, font=(controller.font_style, 12))
        self.name.grid(row=0, column=1, sticky='e', padx=10)
        self.button = tk.Button(self.context_frame, text="Grading Math Worksheets", font=(controller.font_style, 12),
                                command=lambda: controller.show_frame("MathPage"))
        self.button.grid(row=0, column=0, pady=20)
        self.button = tk.Button(self.context_frame, text="Quit the program", font=(controller.font_style, 12),
                                command=self.quit_program)
        self.button.grid(row=1, column=0, pady=20)

    def update_user_name(self):
        self.name.config(text=self.controller.user_name)

    def quit_program(self):
        if messagebox.askyesno(title="Confirm?", message="Do you confirm to quit?"):
            supporting_functions.log_writer([self.controller.user_name, "Logout", " "])
            quit()


class MathPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.user_frame = tk.Frame(self)
        self.user_frame.grid(row=0, column=0, sticky='we')
        self.user_frame.columnconfigure(1, weight=1)

        self.context_frame = tk.Frame(self)
        self.context_frame.grid(row=1, column=0, sticky='we')
        self.context_frame.columnconfigure(0, weight=1)
        self.context_frame.rowconfigure(2, weight=1)

        self.name_label = tk.Label(self.user_frame, text="Current User: ", font=(controller.font_style, 12))
        self.name_label.grid(row=0, column=0, sticky='w', padx=10)
        self.name = tk.Label(self.user_frame, text=controller.user_name, font=(controller.font_style, 12))
        self.name.grid(row=0, column=1, sticky='e', padx=10)

        self.instruction_title = tk.Label(self.context_frame,
                                          text="Image Capture Instruction:",
                                          font=(self.controller.font_style, 12))
        self.instruction_title.grid(row=0, column=0, sticky='w', padx=10)

        self.instruction_label_one = tk.Label(self.context_frame,
                                          text="⚫ Ensure that the worksheet is in the designated area.",
                                          font=(self.controller.font_style, 12))
        self.instruction_label_one.grid(row=1, column=0, sticky='w', padx=10)

        self.instruction_label_two = tk.Label(self.context_frame,
                                          text="⚫ Press SPACE on the scanner window "
                                               "to capture the worksheet or ESC to exit.",
                                          font=(self.controller.font_style, 12))

        self.instruction_label_two.grid(row=2, column=0, sticky='w', padx=10)

        self.manuel_entry = tk.Entry(self.context_frame, font=(controller.font_style, 12))

        self.exit_button = tk.Button(self.context_frame, text="Previous Page",
                                     font=(self.controller.font_style, 10))
        self.exit_button.grid(row=3, column=0, sticky='e', padx=10, pady=20)

    def update_user_name(self):
        self.name.config(text=self.controller.user_name)

    def math_grading(self):
        username = self.controller.user_name
        default_parameters, blank_image = default_files_setup()
        supporting_functions.log_writer([username, "Start Grading Math", " "])
        cam, win_name, rotate = camera_control.setup_cam(username)
        while True:
            project_image, frame, img_name = \
                camera_control.capturing_image(cam, win_name, rotate, username, blank_image)
            if img_name != "":
                edge_coordinates = worksheet_ocr.detect_edge(username, img_name, frame)
                sheet_number = worksheet_ocr.detect_sheet_number(username, img_name, default_parameters, project_image,
                                                                 frame, edge_coordinates, self.instruction_title,
                                                                 self.manuel_entry, self.instruction_label_two,
                                                                 self.instruction_label_one)
                project_image = answer_projection.define_range(default_parameters, sheet_number, edge_coordinates,
                                                               project_image)
                self.instruction_title.config(text="Answers have been projected. "
                                                   "Please select the below options to continue.")
                self.instruction_label_one.config(text="1. Manual amend the sheet number")
                self.instruction_label_two.config(text="2. Hide the answers")
                break
                # print("3. Process to the next page")
                # print("4. Quit")
            else:
                self.instruction_title.config(text="Document Scanner terminated:")
                self.instruction_label_one.config(text="⚫ Return to the previous page by clicking on the button.")
                self.instruction_label_two.config(text="⚫ Exit by closing the program.")
                break


def default_files_setup():
    empty_image = np.zeros((1280, 920, 3), np.uint8)
    cv2.imwrite('./log_files/{}'.format('target.png'), empty_image)
    df = pd.read_csv("./log_files/table.csv", dtype=str)
    supporting_functions.log_writer(["", "Default Loaded", " "])
    return df, empty_image


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
