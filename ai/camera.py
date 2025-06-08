import cv2
import subprocess
import numpy as np
import urllib.request
import time
from ultralytics import YOLO 
import struct


class CameraModule:
    """
    A class to handle camera operations for a USB-C camera connected via ADB.
    This class provides methods to fetch frames, check if the camera is colorful,
    find contours in the frames, and display the frames.
    The camera is expected to be connected to an Android device and the frames/
    We are trying to find contours in the frames.
    The camera is expected to be connected to an Android device and the frames.
    """
    
    def __init__(self):
        self.model = YOLO("../train/weights/best.pt")
        self.termo_vision = False # true is termo vision and false is normal camera
        self.url = input("Write ipwithport default (127.0.0.1:8080): ")
        subprocess.run(["adb", "forward", "tcp:8080", "tcp:8080"])
    
    def get_frame(self):
        try:
            if self.url == "":
                self.url = "127.0.0.1:8080"
                
            # Fetch the image from the camera URL
            img_resp = urllib.request.urlopen("http://" + self.url + "/shot.jpg", timeout=2)
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
   
    def process(self):
        frame = self.get_frame()
        frame = self.crop_frame(frame, 640, 640)
        result = self.model(frame)[0]  # Get first result from YOLO
        
        if result is None or not result.boxes:
            print("No detections found.")
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            return gray
        
        box = result.boxes[0]  # Get bounding boxes from the result
        x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box in pixel format
        confidence = float(box.conf[0])
        class_id = int(box.cls[0])

        # Draw rectangle
        cv2.rectangle(frame, (x1, y1), (x2, y2), color=(0, 255, 0), thickness=2)
        
        # Optionally draw label
        label = f"Dron"
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                0.5, (0, 255, 0), 2)        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        return (gray)

        
    def place_cursor(self, frame):
        cursor_size = int(50/2)
        # cursor looks like a 2 lines in the middle of the screen
        if frame is not None:
            height, width = frame.shape[:2]
            cv2.line(frame, (width // 2, height // 2 - cursor_size), (width // 2, height // 2 + cursor_size), (255, 255, 255), 3)
            cv2.line(frame, (width // 2 - cursor_size, height // 2), (width // 2 + cursor_size, height // 2), (255, 255, 255), 3)
        else:
            print("Unable to fetch frame for cursor placement.")
        return frame
    
    def title_text(self, frame):
        if frame is not None:
            cv2.putText(frame, "Terminator 3000", (15, 60), cv2.FONT_HERSHEY_DUPLEX, 0.83, (255, 255, 255), 2)
            cv2.putText(frame, "Version 1.0.0 (Hackathon edition)", (15, 25), cv2.FONT_HERSHEY_DUPLEX, 0.40, (255, 255, 255), 2)
            self.display_frame(frame)
        else:
            print("Unable to fetch frame for text display.")
            
    def crop_frame(self, frame, width, height):
        """
        Crop the frame to a specified width and height.
        The cropping is done from the center of the frame.
        """
        if frame is not None:
            h, w = frame.shape[:2]
            start_x = (w - width) // 2
            start_y = (h - height) // 2
            cropped_frame = frame[start_y:start_y + height, start_x:start_x + width]
            return cropped_frame
        else:
            print("Unable to fetch frame for cropping.")
            return None
        
    def interface(self, frame):
        self.title_text(frame)    
        frame = self.place_cursor(frame)
        return frame
                
    def test_processing(self):
        while True:
            # Check if the camera is colorful
            frame = self.get_frame()
            frame = self.crop_frame(frame, 640, 640) 
            
            if frame is not None:
                # Convert to grayscale
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Add interface
                self.title_text(gray)    
                gray = self.place_cursor(gray)
                
                # Display the processed frame
                self.display_frame(gray)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                return None     
        cv2.destroyAllWindows()
           
            

if __name__ == "__main__":
    camera = CameraModule()
    camera.test_processing()