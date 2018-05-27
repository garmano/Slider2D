# Slider2D
Slider 2D is intended for making experiments with phidelta diagrams. It can be used to visualize different phidelta diagrams, depending on the class ratio of the dataset at hand (class ratio = ratio between negative and positive samples).

Before running the slider, please make sure that two lists or two vectors (called phi and delta) are available. These data can be manually generated or downloaded from a test file. See the main of Slider2D.py for more information.

Any test file should be in csv format (you may choose the separator, however). At present, each line of the file must contain a couple of phidelta values or a couple of specificity and sensitivity values. The function load, provided in the main of Slider2D, can load both kinds of data (see also the function ss2phidelta, which takes care of data conversion). A test file containing 100 randomly generated samples is also available (see test.csv).

This software is in alpha-release and runs under Python 2.7.

For any further information please feel free to contact me.

    Giuliano Armano (email: armano@diee.unica.it).
    
PS Information about phidelta diagrams can be found here: https://www.sciencedirect.com/science/article/pii/S0020025515005241/pdfft?md5=15bb3eee1dd193293804576fb058b196&pid=1-s2.0-S0020025515005241-main.pdf
