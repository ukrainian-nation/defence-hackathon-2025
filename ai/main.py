from camera import CameraModule
from rotation import RotateModule
import time
import cv2
import struct

if __name__=="__main__":
    camera = CameraModule()
    rotation = RotateModule()
    
    while True:
        """
        Scaning of the positions while cyclus.
        When detects starting a traking of the object,
        4 rotates by x-axis and 2 y-axis rotate on 1 rotate of x-axis.
        Default position is x: 0, y: 0.
        x: 90 -> y: 45, -45 -> 
        x: 90 -> y: 45, -45 -> 
        x: 90 -> y: 45, -45 -> 
        x: 90 -> y: 45, -45
        """
        
        # get frame
        frame = camera.process()
        
        # send frame to ai
        
        # #detect drone

        # if frame is not None:   
        frame = camera.interface(frame)
        
        
        camera.display_frame(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    