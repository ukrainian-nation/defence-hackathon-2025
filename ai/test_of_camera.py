import cv2
import subprocess
import numpy as np
import urllib.request
import time

# Forward phone port to localhost
subprocess.run(["adb", "forward", "tcp:8080", "tcp:8080"])

url = "http://127.0.0.1:8080/shot.jpg"  # Now accessible locally

while True:
    try:
        # Fetch frame
        img_resp = urllib.request.urlopen(url, timeout=2)
        img_arr = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        frame = cv2.imdecode(img_arr, -1)

        # Display
        cv2.imshow("USB-C Camera", frame)
        if cv2.waitKey(1) == ord('q'):
            break

    except Exception as e:
        print(f"Error: {e} - Reconnecting...")
        subprocess.run(["adb", "forward", "--remove-all"])  # Reset
        subprocess.run(["adb", "forward", "tcp:8080", "tcp:8080"])
        time.sleep(1)

cv2.destroyAllWindows()
