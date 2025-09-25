#------------------------------------------------------------------------------
# This class sets up the Android phone camera. The idea for this class came 
# from the Tkinter tutorials, specifically this one: 
# 'Tkinter Entry widget example'
# pythontutorial.net/tkinter/tkinter-entry/
#------------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk

class CameraSetup():

#------------------------------------------------------------------------------
# This is the class constructor that sets up the camera. It calls all the 
# other functions in this class. In general: 
# root: a window is created
# screen: sets window title, size and location
# explanation: a long string label to inform the user how to connect the camera
# ipv4Text: setup IPV4 text entry
# button: Enter button
# mainloop: keeps the window on the screen until enterClicked callback function 
#------------------------------------------------------------------------------
    def __init__(self):
        self.ipv4string = ' '
        self.root = tk.Tk()
        CameraSetup.screen(self)
        CameraSetup.explanation(self)
        CameraSetup.ipv4Text(self)
        CameraSetup.button(self)
        self.root.mainloop()

#------------------------------------------------------------------------------
# This function titles the window, gives it size and centers it in the center 
# of the screen. The comments in the script are from the tkinter tutorial.
#------------------------------------------------------------------------------
    def screen(self):
        self.root.title('Cell Phone Camera Setup')
        window_width = 500
        window_height = 300
        # get the screen dimension
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # find the center point
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        # set the position of the window to the center of the screen
        self.root.geometry(
            f'{window_width}x{window_height}+{center_x}+{center_y}')

#------------------------------------------------------------------------------
# This gives an explanation to the user what to do to set up the camera through
# a label widget.
#------------------------------------------------------------------------------
    def explanation(self):
        ttk.Label(self.root, text="\nIn order to connect your Android cell "
                  "phone, follow the steps below.\n\n1: Download IP Webcam "
                  "Pro on an Android cell phone.\n2: The cell phone and this "
                  "computer must have the same WiFi connection. \n3: Open the "
                  "app, click 'Video preferences', click 'Video orientation' "
                  "and set it to 'Portrait'\n4: Go back to the main page of "
                  "the app and click the last option, 'Start server'. \n5:"
                  " Below, enter in the given IPv4 number given in the app "
                  "camera screen.\n\nE.g.\nhttp://192.168.1.151:8080").pack()

#------------------------------------------------------------------------------
# This function sets up the entry field in the window. 
# ipv4: variable to store user input; initialized with a default value
# ipv4frame: widget, displays a simple rectangle
# ipv4_label: widget, displays text
# ipv4_entry: Entry widget, allows user input, saves input to ipv4 variable 
#------------------------------------------------------------------------------
    def ipv4Text(self):
        self.ipv4 = tk.StringVar(self.root, value='http://192.168.1.151:8080')
        self.ipv4frame = ttk.Frame(self.root)
        self.ipv4frame.pack(padx=10, pady=10, fill='x', expand=True)
        ipv4_label = ttk.Label(self.ipv4frame, text="IPV4:")
        ipv4_label.pack(fill='x', expand=True)
        ipv4_entry = ttk.Entry(self.ipv4frame, textvariable=self.ipv4)
        ipv4_entry.pack(fill='x', expand=True)
        ipv4_entry.focus()

#------------------------------------------------------------------------------
# This sets up the Enter button. The callback function for the button is
# self.enterclicked
#------------------------------------------------------------------------------
    def button(self):
        enter_button = ttk.Button(self.ipv4frame, 
                                  text="Enter", 
                                  command=self.enterClicked)
        enter_button.pack(fill='x', expand=True, pady=10)

#------------------------------------------------------------------------------
# Enter button callback function. When the enter button is clicked, the input
# string from the entry widget is appended with '/shot.jpg'. The IP Camera app
# needs the IPV4 number to end in /shot.jpg to work.
#------------------------------------------------------------------------------
    def enterClicked(self):
        self.ipv4string = f'{self.ipv4.get()}/shot.jpg'
        self.root.destroy()