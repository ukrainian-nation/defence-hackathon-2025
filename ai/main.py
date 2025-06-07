from camera import CameraModule
from rotation import RotateModule



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
        # drone_is_detected = False

        # # start tracking if drone is detected
        # if drone_is_detected:
        #     self.tracking(drone_x, drone_y, center_x, center_y)
        # else:
        #     self.rotate_x(90)  # Rotate x-axis by 90 degrees
        #     self.rotate_motors()
        
        if frame is not None:         
            frame = camera.interface(frame)
            
            camera.display_frame(frame)
            
                