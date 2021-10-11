import json
import cv2
import enum
import os
import numpy as np
from PIL import Image
import sys
import tkinter as tk
from pathlib import Path, WindowsPath
from send2trash import send2trash
try:
    import pyheif # only on UNIX
except ImportError:
    pass

class SizeUnit(enum.Enum):
    BYTES = 1
    KB = 2
    MB = 3
    GB = 4

class Picture(object):
    def __init__(self, path, border, image_width):
        self.image_width = image_width
        self.path = path
        self.image = DuplicateViewer.find_image(str(self.path))
        self.refresh()
        self.border = border

    def refresh(self):
        self.original_image = np.copy(self.image)

    def reset(self):
        self.image = np.copy(self.original_image)

    def resize(self, width, height):
        self.image = cv2.resize(self.image, (width, height), interpolation = cv2.INTER_AREA)
        self.refresh()

    def add_border(self):
        shape = self.image.shape
        h, w, channels = shape
        background = np.zeros(shape, dtype=np.uint8)
        bc = (0, 255, 0) # border color
        bt = 20 # border thickess
        cv2.rectangle(background, (0, 0), (w, h), bc, -1)
        # Fill part of background with original image
        background[bt:h - bt, bt:w - bt] = self.image[bt:h - bt, bt:w - bt]
        self.image = background

    def add_centered_text(self, text, y, font_scale):
        font = cv2.FONT_HERSHEY_SIMPLEX
        background_color = (255, 255, 255)
        font_color = (0, 0, 0)
        thickness = 1
        text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)
        text_width, text_height = text_size
        x = int(self.image_width / 2 - text_width / 2)
        cv2.rectangle(self.image, (x, y), (x + text_width, y + text_height), background_color, -1)
        y = int(y + text_height + font_scale - 1)
        cv2.putText(self.image, text, (x, y), font, font_scale, font_color, thickness)
        self.refresh()

class DuplicateViewer(object):
    def __init__(self, duplicate_json_file):
        with open(duplicate_json_file) as file:
            print("Reading duplicate data from json file...")
            self.duplicate_data = json.load(file)
            print("Finished reading json into dictionary")
        root = tk.Tk()
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        self.image_width = int(self.screen_width / 2)
        self.window = "Duplicate Viewer"
        self.display_duplicates()

    @staticmethod
    def find_image(file: str):
        image = None
        path = Path(file)
        file = str(path.absolute)
        suffix = path.suffix.lower()
        try:
            readable = suffix == '.jpg' or suffix == '.png' or suffix == '.bmp' or suffix == '.jpeg'
            if not readable:
                raise Exception
            image = cv2.imread(file)
        except:
            try:
                if 'pyheif' in sys.modules:
                    heif_file = pyheif.read(file)
                    image = Image.frombytes(
                        heif_file.mode, 
                        heif_file.size, 
                        heif_file.data,
                        "raw",
                        heif_file.mode,
                        heif_file.stride,
                    )
                    image = np.array(image)
                elif suffix == '.heif' or suffix == '.heic':
                    pass
                else:
                    raise Exception
            except:
                try:
                    if suffix == '.mov' or suffix == '.mp4' or suffix == '.avi':
                        capture = cv2.VideoCapture(file)
                        success, image = capture.read()
                        capture.release()
                    else:
                        raise Exception
                except:
                    image = None
                    print("Could not recognize file format for: " + file)
        return image

    @staticmethod
    def convert_unit(size, unit):
        if unit == SizeUnit.KB:
            return size / 1024, "KB"
        elif unit == SizeUnit.MB:
            return size / (1024 * 1024), "MB"
        elif unit == SizeUnit.GB:
            return size / (1024 * 1024 * 1024), "GB"
        else:
            return size, "BYTES"

    @staticmethod
    def get_file_size_text(file_path, unit = SizeUnit.MB):
        size = os.path.getsize(file_path)
        converted_size, suffix = DuplicateViewer.convert_unit(size, unit)
        return str(round(converted_size, 2)) + " " + suffix

    def display_duplicates(self):
        self.running = True
        for duplicate in self.duplicate_data:
            if self.running:
                similarity = duplicate["similarity"]
                paths = duplicate["paths"]
                picture1 = Picture(paths[0], True, self.image_width)
                picture2 = Picture(paths[1], False, self.image_width)
                if picture1.image is not None and picture2.image is not None:
                    picture1.resize(picture1.image_width, self.screen_height)
                    picture2.resize(picture1.image_width, self.screen_height)
                    picture1.add_centered_text("Similarity: " + str(similarity), 20, 0.8)
                    picture1.add_centered_text(DuplicateViewer.get_file_size_text(picture1.path), 50, 0.8)
                    picture1.add_centered_text(picture1.path, 70, 1 / 2)
                    picture2.add_centered_text("Similarity: " + str(similarity), 20, 0.8)
                    picture2.add_centered_text(DuplicateViewer.get_file_size_text(picture2.path), 50, 0.8)
                    picture2.add_centered_text(picture2.path, 70, 1 / 2)
                    pictures = [picture1, picture2]
                    cv2.namedWindow(self.window, cv2.WND_PROP_FULLSCREEN)
                    cv2.moveWindow(self.window, 0, 0)
                    cv2.setWindowProperty(self.window, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                    self.update_display(pictures)
                    while cv2.getWindowProperty(self.window, 0) >= 0:
                        k = cv2.waitKey(33)
                        if k == 27: # Esc key to stop
                            self.running = False
                            break
                        elif k == -1: # -1 returned if no key is pressed
                            continue
                        elif k == ord('s'): # Skip duplicate if 's' is pressed
                            break
                        elif k == ord('1'):
                            pictures[0].border = not pictures[0].border
                            self.update_display(pictures)
                        elif k == ord('2'):
                            pictures[1].border = not pictures[1].border
                            self.update_display(pictures)
                        elif k == ord(' '):
                            for picture in pictures:
                                if not picture.border:
                                    if os.path.exists(picture.path):
                                        try:
                                            send2trash(os.path.abspath(picture.path))
                                            print("Deleting: " + picture.path)
                                        except:
                                            print("Failed to delete: " + picture.path)
                                            #shutil.move(os.path.abspath(picture.path), 'D:/Media/test')
                                            #print("Moving: " + picture.path + " to duplicate folder")
                            print("---")
                            break
                else:
                    # Notify the user that an image cannot be displayed
                    print("Skipping: [" + picture1.path + ", " + picture2.path + "]")

    def update_display(self, pictures):
        for picture in pictures:
            if picture.border:
                picture.add_border()
            else:
                picture.reset()
        cv2.imshow(self.window, cv2.hconcat([pictures[0].image, pictures[1].image]))

viewer = DuplicateViewer('heic_duplicates.json')
