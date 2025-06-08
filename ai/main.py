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
        
        # get frame and process it
        (frame, result) = camera.process() # frame and (x1, y1, x2, y2)

        # get Angle to rotate
        if result is not None:
            (rotate_x, rotate_y) = rotation.calculate_rotation_angles(
                drone_x=abs(result[0]-result[2])/2+result[0], 
                drone_y=abs(result[1]-result[3])/2+result[1], 
                center_x=320, 
                center_y=320
            )
            print(f"Rotate X: {rotate_x}, Rotate Y: {rotate_y}")

        # if frame is not None:   
        if result is None:
            frame = camera.interface(frame)
        else:
            frame = camera.interface(frame, drone_x=abs(result[0]-result[2])/2+result[0], drone_y=abs(result[1]-result[3])/2+result[1])
        
        
        camera.display_frame(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    