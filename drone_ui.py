import threading
import tello
import cv2
import time
import platform
from PIL import Image


class DroneUI:
    def __init__(self, tello):
        self.tello = tello
        #self.thread = None
        #self.stopEvent = None  

        #self.stopEvent = threading.Event()
        #self.thread = threading.Thread(target=self.videoLoop, args=())
        #self.thread.start()

        while True:                
                time.sleep(0.5)
                system = platform.system()

            # read the frame for GUI show
                self.frame = self.tello.read()
                if self.frame is None or self.frame.size == 0:
                    continue

                print self.frame
                #cv2.imshow('Image', self.frame)
                image = Image.fromarray(self.frame)
                cv2.imshow('Image', self.frame)
                                                          

    def videoLoop(self):
        """
        The mainloop thread of Tkinter 
        Raises:
            RuntimeError: To get around a RunTime error that Tkinter throws due to threading.
        """
        try:
            # start the thread that get GUI image and drwa skeleton 
            #self.sending_command_thread.start()
            while not self.stopEvent.is_set():                
                system = platform.system()

            # read the frame for GUI show
                self.frame = self.tello.read()
                if self.frame is None or self.frame.size == 0:
                    continue

                print self.frame
                #cv2.imshow('ImageWindow', self.frame)
                ##image = Image.fromarray(self.frame)
                                                          
        except RuntimeError, e:
            print("[INFO] caught a RuntimeError")

    def _sendingCommand(self):
        """
        start a while loop that sends 'command' to tello every 5 second
        """    

        while True:
            self.tello.send_command('command')        
            time.sleep(5)


    def on_keypress_enter(self, event):
        if self.frame is not None:
            self.registerFace()
        self.tmp_f.focus_set()

    def onClose(self):
        """
        set the stop event, cleanup the camera, and allow the rest of
        
        the quit process to continue
        """
        print("[INFO] closing...")
        self.stopEvent.set()
        del self.tello
        self.root.quit()

