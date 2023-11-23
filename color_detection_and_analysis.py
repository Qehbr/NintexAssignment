import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk
from tkinter import ttk, TclError


class ColorDetectionAnalysisApp:
    """
    A Tkinter application for color detection and analysis using HSV values.
    """

    def __init__(self, master):
        self.master = master
        self.master.title("Color Detection and Analysis")

        # min and max values for HSV values
        self.hue_min_var = tk.DoubleVar()
        self.hue_max_var = tk.DoubleVar(value=179)
        self.saturation_min_var = tk.DoubleVar()
        self.saturation_max_var = tk.DoubleVar(value=255)
        self.value_min_var = tk.DoubleVar()
        self.value_max_var = tk.DoubleVar(value=255)

        # use theme and change font and colors
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', font=('Arial', 12), background='#E6E6FA')
        style.configure('TButton', font=('Arial', 12), padding=5)
        style.configure('TFrame', background='#E6E6FA')

        self.image = None

        # create widgets for the app
        self.create_widgets()

    def create_widgets(self):
        """
        Creates and organizes widgets (spinboxes and buttons) for the application.
        @param self: instance of the class
        @return:
        """

        # create a frame for widgets
        frame = ttk.Frame(self.master, padding="20")
        frame.grid(row=0, column=0, padx=20, pady=20)

        # hue range
        hue_label = ttk.Label(frame, text="Hue Range (0-179)")
        hue_label.grid(row=0, column=0, padx=10, pady=10)
        hue_min_spinbox = tk.Spinbox(frame, from_=0, to=179, textvariable=self.hue_min_var)
        hue_min_spinbox.grid(row=0, column=1, padx=10, pady=10)
        hue_max_spinbox = tk.Spinbox(frame, from_=0, to=179, textvariable=self.hue_max_var)
        hue_max_spinbox.grid(row=0, column=2, padx=10, pady=10)

        # saturation Range
        saturation_label = ttk.Label(frame, text="Saturation Range (0-255)")
        saturation_label.grid(row=1, column=0, padx=10, pady=10)
        saturation_min_spinbox = tk.Spinbox(frame, from_=0, to=255, textvariable=self.saturation_min_var)
        saturation_min_spinbox.grid(row=1, column=1, padx=10, pady=10)
        saturation_max_spinbox = tk.Spinbox(frame, from_=0, to=255, textvariable=self.saturation_max_var)
        saturation_max_spinbox.grid(row=1, column=2, padx=10, pady=10)

        # value Range
        value_label = ttk.Label(frame, text="Value Range (0-255)")
        value_label.grid(row=2, column=0, padx=10, pady=10)
        value_min_spinbox = tk.Spinbox(frame, from_=0, to=255, textvariable=self.value_min_var)
        value_min_spinbox.grid(row=2, column=1, padx=10, pady=10)
        value_max_spinbox = tk.Spinbox(frame, from_=0, to=255, textvariable=self.value_max_var)
        value_max_spinbox.grid(row=2, column=2, padx=10, pady=10)

        # upload image button
        upload_button = ttk.Button(frame, text="Upload Image", command=self.upload_image)
        upload_button.grid(row=3, column=0, columnspan=3, pady=20)

        # detect colors button
        detect_button = ttk.Button(frame, text="Detect Colors", command=self.detect_colors)
        detect_button.grid(row=4, column=0, columnspan=3, pady=20)

        # create canvas for the image (so it will not appear too big)
        self.canvas = tk.Canvas(frame, width=400, height=400)
        self.canvas.grid(row=5, column=0, columnspan=3, pady=10)

        # label for displaying percentage coverage
        self.coverage_label = ttk.Label(frame, text="")
        self.coverage_label.grid(row=6, column=0, columnspan=3, pady=10)

    def upload_image(self):
        """
        Uploads an image file and displays it on the canvas.
        @param self: instance of the class
        @return: None
        """
        # only images can be uploaded
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;")])
        if file_path:
            self.image = cv2.imread(file_path)
            if self.image is not None:
                self.display_image(self.image)
            # if somehow not image has been chosen
            else:
                messagebox.showerror("Error", "Selected file is not a valid image.")
                print("Selected file is not a valid image.")

    def display_image(self, image):
        """
        Displays an image on the canvas, keeping its ratio and adjusting its size.
        @param self: instance of the class
        @param image: OpenCV image to be displayed
        @return: None
        """

        # create image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)

        # fit the image to the canvas and keep image ratio
        original_width, original_height = image.size
        target_width = 400
        target_height = int((target_width / original_width) * original_height)

        # resize image to the size of canvas
        image = image.resize((target_width, target_height), Image.LANCZOS)

        # update canvas
        photo = ImageTk.PhotoImage(image=image)
        self.canvas.config(width=target_width, height=target_height)

        # display image on canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.canvas.image = photo

    def detect_colors(self):
        """
        Detects and highlights colors within a specified range in the uploaded image.
        Calculates the area of highlighted colors and outputs the percentage coverage.
        @param self: instance of the class
        @return: None
        """
        if self.image is not None:
            # validate HSV ranges
            try:
                if not (0 <= self.hue_min_var.get() <= 179 and 0 <= self.hue_max_var.get() <= 179 and
                        0 <= self.saturation_min_var.get() <= 255 and 0 <= self.saturation_max_var.get() <= 255 and
                        0 <= self.value_min_var.get() <= 255 and 0 <= self.value_max_var.get() <= 255):
                    messagebox.showerror("Error", "Invalid HSV range. Please ensure values are within the valid range.")
                    print("Invalid HSV range. Please ensure values are within the valid range.")
                    return
            except TclError:
                messagebox.showerror("Error", "Invalid HSV range. Please ensure values are within the valid range.")
                print("Invalid HSV range. Please ensure values are within the valid range.")
                return

            # set the range corresponding to the user's values
            lower_range = np.array([self.hue_min_var.get(), self.saturation_min_var.get(), self.value_min_var.get()])
            upper_range = np.array([self.hue_max_var.get(), self.saturation_max_var.get(), self.value_max_var.get()])

            # convert the image to HSV values
            hsv_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

            # check for each pixel if it is in the given range
            mask = cv2.inRange(hsv_image, lower_range, upper_range)
            result = cv2.bitwise_and(self.image, self.image, mask=mask)

            # create a red mask for pixels in range
            red_mask = np.zeros_like(result)
            red_mask[mask > 0] = [0, 0, 255]  # set pixels in range to red

            # merge the red mask with original image
            alpha = 0.3  # control highlighting
            highlighted_image = cv2.addWeighted(self.image, 0.9, red_mask, alpha, 0)

            # display a new image on canvas
            self.display_image(highlighted_image)

            # calculate the percentage coverage
            highlighted_area = np.count_nonzero(mask)
            total_area = self.image.shape[0] * self.image.shape[1]
            percentage_coverage = (highlighted_area / total_area) * 100

            # update the label text with the percentage coverage
            self.coverage_label.config(text=f"Percentage Coverage: {percentage_coverage:.2f}%")

            messagebox.showinfo("Success",
                                f"Highlighted area: {highlighted_area} pixels\n"
                                f"Total area: {total_area} pixels\n"
                                f"Percentage coverage: {percentage_coverage:.2f}%")

        # if image has not been chosen
        else:
            print("Please upload an image first.")
            messagebox.showerror("Error", "Please upload an image first.")


if __name__ == "__main__":
    root = tk.Tk()
    app = ColorDetectionAnalysisApp(root)
    root.mainloop()
