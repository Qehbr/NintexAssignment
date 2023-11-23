# **Color Detection and Analysis App**
**Color Detection and Analysis - practical assignment for Nintex RPA.**

The application allows users to perform color detection and analysis on images using HSV values.

## Author
Yuriy Rusanov
GitHub: [https://github.com/Qehbr](https://github.com/Qehbr)

## Overview

The Color Detection and Analysis App is designed to analyze images and highlight colors within a specified range using HSV values. The application also calculates the percentage coverage of the highlighted colors.

## Usage:
1. Run `color_detection_and_analysis-cli.py`
2. Choose the desired HSV range by using **min-max spinboxes**. Valid range: (H: 0-179, S: 0-255, V: 0-255).
3. Upload the image by using "**Upload Image**" button.
4. Highlight and calculate area of pixels in the given range by "**Detect Colors**" button


## Files:
### color_detection_and_analysis.py
*  This file contains the implementation of the Color Detection and Analysis App.
*  It includes functions for uploading images, displaying them on the canvas, and detecting colors based HSV ranges specified by user.

## Assumptions and Decisions:
* **HSV Range Validation**: The application validates HSV ranges specified by user and ensures it falls within the valid range: (H: 0-179, S: 0-255, V: 0-255). (Users will be alerted if an invalid range is provided)
* **Image File Types**: The application supports image files with extensions ".png," ".jpg," and ".jpeg." Other file types are not considered valid image files.
* **Highlighting Style**: The highlighting of colors uses a red-color mask over the detected colors. The intensity of the highlighting is controlled by an alpha value. Not highlighted parts of the image become less visible (0.9)
* **UI**: The application uses Tkinter for the UI.

