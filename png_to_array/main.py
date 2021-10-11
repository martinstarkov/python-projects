import math as m
import os
from pathlib import Path
import cv2
import pyperclip
import xlrd
from PIL import Image

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
HOME_DIR = str(Path.home())

#used for converting numbers into their corresponding hex letter
hexDictionary = {
    10: "A",
    11: "B",
    12: "C",
    13: "D",
    14: "E",
    15: "F",
}

#if a value is above 9, turn it into a hex character
def hexify(number_):
    if number_ > 9:
        return hexDictionary.get(number_)
    else:
        return str(int(number_))

#find the hex value of an individual (r,g,b) value
def makeHex(number_):
    return hexify(m.floor(number_ / 16)) + hexify((number_ / 16 - m.floor(number_ / 16)) * 16)    

#stitch the (r,g,b) hex values into one hex code
def rgbToHex(rgbTuple_):
    return "#{0:2}{1:2}{2:2}".format(makeHex(rgbTuple_[2]), makeHex(rgbTuple_[1]), makeHex(rgbTuple_[0]))

#find and return the number corresponding to the hex code from the excel sheet
def hexToTexture(hexValue_, dictionary_):
    return dictionary_.get(hexValue_, "Unknown Hex Texture: " + hexValue_)

#read the excel sheet and populate the texture dictionary
def setTextureDictionary(excel_):
    dictionary = {}
    workbook = xlrd.open_workbook(excel_)
    sheet = workbook.sheet_by_index(0)
    for i in range(1, sheet.nrows):
        dictionary[sheet.cell_value(i, 2)] = int(sheet.cell_value(i, 1))
    return dictionary

#loop through the pixels of the image and return an array containing the corresponding numbers to each hex code
def generateData(image_, excel_):
    dictionary = setTextureDictionary(excel_)
    print("Texture dictionary processed: " + str(dictionary))
    data = cv2.imread(image_)
    height, width = data.shape[:2]
    pixelMap = []
    for row in range(height):
        pixelMap.append([])
        for column in range(width):
            hexColor = rgbToHex(data[row, column])
            pixelMap[row].append(hexToTexture(hexColor, dictionary))
    return pixelMap

#create / write and clear the data to a file that is readable by the C++ side of my map interpreter 
def writeToFile(path_, data_):
    f = open(path_, "w+")
    for row in range(len(data_)):
        for column in range(len(data_[row])):
            if not column == len(data_[row]) - 1:
                f.write(str(data_[row][column]) + " ")
            else:
                f.write(str(data_[row][column]))
        if not row == len(data_) - 1:
            f.write("\n")
    f.close()

def checkPathValidity(path_, check_):
    if path_ != "":
        #determine if file/folder needs to be readable or writeable
        write_or_read = os.R_OK
        if check_ == "folder":
            write_or_read = os.W_OK
        elif check_ == "image":
            if ".png" not in path_:
                print("Image file path invalid. Please give a valid "".png"" image file path.")
                return ""
        elif check_ == "dictionary":
            if ".xlsm" not in path_:
                print("Excel file path invalid. Please give a valid "".xlsm"" excel file path.")
                return ""
        #check absolute paths
        if not os.access(path_, write_or_read):
            #check Drive:\Users\UserName home directory paths
            if not os.access(HOME_DIR + "\\" + path_, write_or_read):
                #check root directory paths (where the python program is run from)
                if not os.access(ROOT_DIR + "\\" + path_, write_or_read):
                    if check_ == "folder":
                        if "\\" not in path_[:-1] and "." not in path_:
                            #ask the user if they would like to create a new folder using input()[-1] to confirm
                            if input("Would you like to generate a folder called \"" + path_ + "\" in \"" + ROOT_DIR + "\\\"? (y/n): ")[-1] == "y":
                                path_ = ROOT_DIR + "\\" + path_
                                os.mkdir(path_)
                                print("Created \"" + path_ + "\" folder")
                                return path_
                    print("Path invalid.")
                    return ""
                else:
                    path_ = ROOT_DIR + "\\" + path_
            else:
                path_ = HOME_DIR + "\\" + path_
    return path_

def runProgram(file_, folder_, image_, dictionary_):

    if "." in file_ and ".txt" not in file_:
        print("File name invalid. Please do not include file type such as \".docx\" in the end.")
        runProgram(input("Enter a name for the output file: "), "", "", "")
    
    if ".txt" not in file_:
        file_ += ".txt"

    folder_ = checkPathValidity(folder_, "folder")

    if folder_ == "":
        runProgram(file_, input("Enter a location for the output file: "), "", "")

    if "/" in folder_:
        folder_.replace("/", "\\")

    if "desktop" in folder_.lower() and "\\" not in folder_:
        folder_ = HOME_DIR + "\\Desktop\\"

    if folder_[-1] != "\\" and "\\" in  folder_:
        folder_ += "\\"

    image_ = checkPathValidity(image_, "image")

    if image_ == "":
        runProgram(file_, folder_, input("Enter an image file path to read pixel data from: "), "")

    dictionary_ = checkPathValidity(dictionary_, "dictionary")

    if dictionary_ == "":
        runProgram(file_, folder_, image_, input("Enter an excel file path to read color values from: "))

    data = generateData(image_, dictionary_)
    pyperclip.copy(str(data).replace("[", "{").replace("]", "}")) #convert python array to c++ form array with curly brackets
    print("Data copied to clipboard.")
    writeToFile(folder_ + file_, data)
    print("Map file created at \"" + folder_ + file_ + "\"")
    print()
    runProgram(input("Enter a name for the output file: "), "", "", "")

runProgram(input("Enter a name for the output file: "), "", "", "")