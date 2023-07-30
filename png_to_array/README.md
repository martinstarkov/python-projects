# Description

Turn `.png` files into tilemap data arrays for easy 2D level creation.


# How to use

1. Open a command line.
2. Navigate to this directory using the ```cd``` command.
3. Type ```python3 main.py``` to run the program.
4. Provide the following information to the program: 
    - The file name and location for the generated tilemap data file.
    - The path to a readable `.png` image.
    - The path to a `.xlsm` excel texture dictionary.


## Example image
![exampleImage](https://user-images.githubusercontent.com/5933654/58112556-736cdc80-7bfc-11e9-8af4-5f3211076717.png)

It is important that the hex codes used in the image match the texture dictionary values.


## Example dictionary
![exampleDictionary](https://user-images.githubusercontent.com/5933654/58112555-736cdc80-7bfc-11e9-842d-909c40c64fd2.png)

The crucial part in the texture dictionary is that it contains numbers in the second column and hex codes in the third column, everything else in the image is optional (texture names and rgb values). The number column tells the program to replace the corresponding pixels with those integers. 

The `example_dictionary.xlsm` provided in this repository contains a macro that will color the background of each hex column cells with the appropriate color, make sure to run the macro every time a color is added if you would like the cells to update color (optional).


## Example output file
![exampleSmall](https://user-images.githubusercontent.com/5933654/58112557-736cdc80-7bfc-11e9-9225-4daacf5f23b6.png)


## Example output file (zoomed to see numbers)
![exampleBig](https://user-images.githubusercontent.com/5933654/59223404-827bf480-8bd4-11e9-90e2-79cace288c82.png)

As seen above, the program has converted the image into an array of numbers that can be processed by a game's tilemap processing code. 