#------------------------------------------------------------------------------
# This class takes an image from an Android cell phone video, identifies the 
# coins in the image(quarter, dime, nickel, penny), calculates the total value 
# of the coins, draws boxes and labels the coins, and shows all this 
# information in a GUI. The image updates the GUI about every 0.5 s. The GUI 
# allows a user to save the image as a jpg or record the GUI window and 
# create/save an mp4.
#------------------------------------------------------------------------------
from inference import get_model
import supervision as sv
import requests 
import cv2 
import numpy as np 
import datetime
import package.camera_setup as cs
import os

class RoboflowCoins():
#------------------------------------------------------------------------------
# This is the class constructor. It calls the CameraSetup class to set up the 
# Android phone camera, gets the model created with Roboflow and initializes
# other various variables necessary to run the script.
# The Roboflow model used in this project can be found here:
# https://universe.roboflow.com/s1-sowiy/coins-l4wkp/model/7
#------------------------------------------------------------------------------
    def __init__(self):
        self.camera = cs.CameraSetup()
        self.url = self.camera.ipv4string
        self.model = get_model(model_id="coins-l4wkp/7", 
                               api_key="")
        self.f = 1  
        self.r = 0
        self.rS = -1
        self.p = 0
        self.q = 1
        self.font = cv2.FONT_HERSHEY_PLAIN
        self.org1 = (100, 85)
        self.org2 = (700, 85)
        self.L = 60
        self.w = 0
        self.buttonS1 = "EXIT PROGRAM: 'Esc' OR MIDDLE CLICK"
        self.buttonS2 = "RECORD MP4: 'r' OR RIGHT CLICK"
        self.buttonS3 = "SAVE JPG: 's' OR LEFT CLICK"
        self.buttonS4 = "PICTURE SAVED"
        self.buttonS5 = ["RECORDING","RECORDING.","RECORDING..","RECORDING..."]
        os.makedirs('./pictures', exist_ok=True)
        os.makedirs('./videos', exist_ok=True)
        self.fontScale = 6
        self.fontScale1 = 3
        self.color1 = (0, 0, 0)
        self.color2 = (0, 0, 255)
        self.thickness = 12
        self.thickness1 = 5
        self.Esc = False
        self.lc = 0
        self.mc = 0
        self.rc = 0

#------------------------------------------------------------------------------
# This is the main loop that runs after the camera has been set up, it does not 
# stop until the user presses the esc key or the center mouse button. The loop
# follows this order:
# Get the image from the cell phone
# Run inference on the image/calculate the value of the coins
# Draw boxes around each coin based on the inference results
# Add all the text on the user display screen
# Show the image with the boxes and text
# Check if the user wants to take a picture or stop/start recording or quit
#------------------------------------------------------------------------------
    def detect(self):    
        # While loop to continuously fetching data from the URL 
        while self.Esc == False: 
            RoboflowCoins.getImage(self)
            RoboflowCoins.getTotal(self)
            RoboflowCoins.drawBoxes(self)
            RoboflowCoins.addText(self)
            RoboflowCoins.showImage(self)
            RoboflowCoins.userInput(self)
        cv2.destroyAllWindows() 

#------------------------------------------------------------------------------
# This function gets the image from the cell phone. The first lines up to the 
# if statement were found here:
# geeksforgeeks.org/connect-your-android-phone-camera-to-opencv-python/
# This site also helped with connecting the phone to this script.
# The if statement only runs once. It gets the image pixel size and creates an
# aspect ratio used later to display the video.
#------------------------------------------------------------------------------
    def getImage(self):
        self.img_resp = requests.get(self.url) 
        self.img_arr = np.array(bytearray(self.img_resp.content), 
                                dtype=np.uint8) 
        self.img = cv2.imdecode(self.img_arr, -1) 
        if self.f == 1:
            self.aspect_ratio = self.img.shape[1] / self.img.shape[0]
            self.width = 500
            self.height = int(self.width / self.aspect_ratio)
            self.f = 0

#------------------------------------------------------------------------------
# This function runs inference on the image through Roboflow's self-hosted 
# inference. The results are used to calculate the total amount of coins and 
# their total value.
#------------------------------------------------------------------------------
    def getTotal(self):
        self.results = self.model.infer(self.img)[0]    
        count = len(self.results.predictions)
        total = 0.0
        for i in range(0,count):
            if self.results.predictions[i].class_name == 'Penny':
                total += 0.01
            elif self.results.predictions[i].class_name == 'Nickel':
                total += 0.05
            elif self.results.predictions[i].class_name == 'Dime':
                total += 0.1
            elif self.results.predictions[i].class_name == 'Quarter':
                total += 0.25
            else:
                total += 0.0
        self.totalS = "%0.2f" % total
        self.totalS = '$' + self.totalS        

#------------------------------------------------------------------------------
# This function adds the boxes around each coin in the image. This site helped
# write this function:
# inference.roboflow.com/quickstart/run_a_model/#visualize-results
# The comments in the function are from this site. The only parts altered are
# the parameters inside the parenthesis for the first 3 variables.
# The if statement at the end only runs once. It sets the origins of the text
# based on the image size.
#------------------------------------------------------------------------------
    def drawBoxes(self):
        # load the results into the supervision Detections api
        detections = sv.Detections.from_inference(self.results)
        # create supervision annotators
        bounding_box_annotator = sv.BoxAnnotator(thickness=10)
        label_annotator = sv.LabelAnnotator(text_scale=0.8, text_thickness=2)
        # annotate the image with our inference results
        self.annotated_image = bounding_box_annotator.annotate(
                            scene=self.img, detections=detections)
        self.annotated_image = label_annotator.annotate(
                            scene=self.annotated_image, detections=detections)
        if self.w == 0:
            self.org3 = (100, self.annotated_image.shape[0]-self.L)
            self.org4 = (100, self.annotated_image.shape[0]-2*self.L)
            self.org5 = (100, self.annotated_image.shape[0]-3*self.L)
            self.org6 = (100, self.annotated_image.shape[0]-4*self.L)
            self.w = 1

#------------------------------------------------------------------------------
# This function adds all the text to the image. The 2nd self.annotated_image
# is the calculated total as a string (totalS). The if statements at the end
# are to let the user know a picture was taken or if the screen is being 
# recorded. The logic was necessary because the text placement depends on the
# user's input. The logic is slightly complicated because the user can start
# recording and while recording take a picture. The recording text turns off
# for about 1 sec to display the picture text and then the recording text turns 
# back on when the picture text goes off.
# p is if a picture was taken
# q was needed because picture and recording strings were displayed on top of 
#   each other for 1 cycle
# r is if a recording was turned on
# rS is for the recording strings to cycle through: RECORDING, RECORDING.,
#   RECORDING.. RECORDING...
#------------------------------------------------------------------------------
    def addText(self):
        self.annotated_image = cv2.putText(self.annotated_image, 'TOTAL: ', 
                                           self.org1, self.font, 
                                           self.fontScale, self.color1, 
                                           self.thickness, cv2.LINE_AA)
        self.annotated_image = cv2.putText(self.annotated_image, self.totalS, 
                                           self.org2, self.font, 
                                           self.fontScale, self.color2, 
                                           self.thickness, cv2.LINE_AA)
        self.annotated_image = cv2.putText(self.annotated_image, self.buttonS1, 
                                           self.org3, self.font, 
                                           self.fontScale1, self.color1, 
                                           self.thickness1, cv2.LINE_AA)
        self.annotated_image = cv2.putText(self.annotated_image, self.buttonS2,
                                            self.org4, self.font, 
                                            self.fontScale1, self.color1, 
                                            self.thickness1, cv2.LINE_AA)
        self.annotated_image = cv2.putText(self.annotated_image, self.buttonS3,
                                            self.org5, self.font, 
                                            self.fontScale1, self.color1, 
                                            self.thickness1, cv2.LINE_AA)
        if self.p != 0:
            self.annotated_image = cv2.putText(self.annotated_image, 
                                               self.buttonS4, self.org6, 
                                               self.font, self.fontScale, 
                                               self.color2, self.thickness, 
                                               cv2.LINE_AA)
            self.p += 1
            if self.p == 4:
                self.p = 0
                self.q = 0
        if self.r != 0:
            self.rS += 1
            if self.rS == 4:
                self.rS = 0
            if self.p == 0 and self.q != 0:   
                self.annotated_image = cv2.putText(self.annotated_image, 
                                                   self.buttonS5[self.rS], 
                                                   self.org6, self.font, 
                                                   self.fontScale, self.color2, 
                                                   self.thickness, cv2.LINE_AA)
            elif self.q == 0:
                self.q = 1

#------------------------------------------------------------------------------
# This function resizes the image and displays it. If recording is on, the 
# current frame is written to an mp4.
#------------------------------------------------------------------------------
    def showImage(self):
        resized_image = cv2.resize(self.annotated_image, (self.width, 
                                                          self.height))
        cv2.imshow("Android Camera", resized_image) 
        if self.r == 1:
            self.out.write(self.annotated_image)

#------------------------------------------------------------------------------
# This script handles all the user input.
# To exit the program: key 27 or self.mc ('Esc' key or mouse middle click) 
# To save an image: key 115 or self.lc ('s' key or mouse left click)
# To start or stop recording: key 114 or self.rc ('r' key or mouse right click)
# The last if statement is if the user quits during a recording. In this case,
# the video is released before the script ends.
#------------------------------------------------------------------------------
    def userInput(self):
        cv2.setMouseCallback('Android Camera', self.mouseClick) 
        key = cv2.waitKey(500)
        if key == 27 or self.mc == 1: # exit on ESC
            self.Esc = True
        if key == 115 or self.lc == 1: # save image with s key
            filename = ('./pictures/total-{date:%Y%m%d%H%M%S}.jpg'.format(
                                                date=datetime.datetime.now()))
            cv2.imwrite(filename, self.annotated_image)
            print('Image saved as: ' + filename)
            self.p = 1
            self.lc = 0
        if key == 114 or self.rc == 1: # start/stop record with r key
            if self.r == 0:
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                self.mp4name = ('./videos/total{date:%Y%m%d%H%M%S}.mp4'.format(
                                                date=datetime.datetime.now()))
                self.out = cv2.VideoWriter(self.mp4name, fourcc, 2.0, (
                                                self.annotated_image.shape[1],
                                                self.annotated_image.shape[0]))
                self.r = 1
                self.rS = -1
                print('Recording..')
            else:
                self.r = 0
                print('Recording Stopped, MP4 saved as: ' + self.mp4name)
                self.out.release()
            self.rc = 0
        if self.Esc == True and self.r == 1:
            self.r = 0
            print('Recording Stopped, MP4 saved as: ' + self.mp4name)
            self.out.release()

#------------------------------------------------------------------------------
# This is the mouse callback function, it directly relates to the function
# above, userInput.
#------------------------------------------------------------------------------
    def mouseClick(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.lc = 1
        if event == cv2.EVENT_RBUTTONDOWN:
            self.rc = 1
        if event == cv2.EVENT_MBUTTONDOWN:
            self.mc = 1