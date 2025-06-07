import cv2
import subprocess
import numpy as np
import urllib.request
import time


class CameraModule:
    """
    A class to handle camera operations for a USB-C camera connected via ADB.
    This class provides methods to fetch frames, check if the camera is colorful,
    find contours in the frames, and display the frames.
    The camera is expected to be connected to an Android device and the frames/
    We are trying to find contours in the frames.
    The camera is expected to be connected to an Android device and the frames
    """
    
    def __init__(self):
        self.colorful = False # true is light and false is dark
        self.url = "http://127.0.0.1:8080/shot.jpg"
        subprocess.run(["adb", "forward", "tcp:8080", "tcp:8080"])
    
    def get_frame(self):
        try:
            img_resp = urllib.request.urlopen(self.url, timeout=2)
            img_arr = np.array(bytearray(img_resp.read()), dtype=np.uint8)
            frame = cv2.imdecode(img_arr, -1)
            return frame
        except Exception as e:
            print(f"Error fetching frame: {e}")
            return None
    
    def display_frame(self, frame):
        if frame is not None:
            cv2.imshow("USB-C Camera", frame)
        else:
            return None
        
        
    def check_colorful(self):
        frame = self.get_frame()
        if frame is not None:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            brightness = np.mean(hsv[:, :, 2])  # Calculate the average brightness from the V channel
            self.colorful = brightness > 100  # Threshold to determine if it's light or dark
            print(f"Colorful: {self.colorful}, Brightness: {brightness}")
        else:
            print("Unable to fetch frame for color check.")
    
    def find_conturs(self, frame):
        if not self.colorful:
            frame = cv2.convertScaleAbs(frame, alpha=1.2, beta=30)  # Increase contrast and brightness
            
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 50, 150)
        contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours
    
    
    def test_processing(self):
        while True:
            self.check_colorful()
            frame = self.get_frame()
            if frame is not None:
                contours = self.find_conturs(frame)
                for contour in contours:
                    cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
                self.display_frame(frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                return None     
        cv2.destroyAllWindows()
           
            

if __name__ == "__main__":
    camera = CameraModule()
    camera.test_processing()