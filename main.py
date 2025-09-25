#------------------------------------------------------------------------------
# CS7367 MACHINE VISION
# FINAL PROJECT
# Trevor Zimmerman
# 12/2/24
#
# This project utilizes Roboflow to detect USD coins from a cell phone camera 
# and calculates the total value of the coins in the image frame.
#
# An Android cell phone with the app IP Webcam is necessary to run this script.
# The script provides more specific steps when it runs and opens the camera 
# setup screen. The photo resolution of the camera used to make this project is
# 1920x1080. Using a phone with a different resolution may cause scaling issues
# to all the annotations on the output window.
#
# The dataset and model created for this project can be found here:
# https://universe.roboflow.com/s1-sowiy/coins-l4wkp
# A few datasets and models are located here, version 7 is what is used in this
# project.
#------------------------------------------------------------------------------
import package.roboflow_coins as rc

def main():
    coinProject = rc.RoboflowCoins()
    coinProject.detect()

if __name__ == '__main__':
    main()  