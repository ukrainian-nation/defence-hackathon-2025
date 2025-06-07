import math
import serial

class RotateModule:
    """
    RotateModule is a class that handles the rotation of a robot or device.
    We have 2 motors that can rotate the device in x and y directions.
    The rotation angle is specified in degrees.
    The class provides methods to rotate the device and scan the surroundings.
    """
    
    def __init__(self):
        """
        We have 390 degrees rotation
        """
        self.x_motor = 0  # Placeholder for x-axis motor control
        self.y_motor = 0  # Placeholder for y-axis motor control
        pass
    
    def setup_basic_position(self):
        """
        Set the initial position of the motors to 0 degrees.
        This is the default position for the device.
        """
        return 

    def tracking(self, drone_x, drone_y, center_x, center_y):
        pass

    def difference_between_drone_and_center(self, drone_x, drone_y, center_x, center_y):
        """
        Calculate the difference between the drone's position and the center position.
        This is used to determine how much to rotate the drone to face the center.
        Returns a tuple of (diff_x, diff_y).
        """
        diff_x =  drone_x - center_x
        diff_y =  drone_y - center_y
        return diff_x, diff_y

    def calculate_rotation_angles(self, drone_x, drone_y, center_x, center_y):
        """
        Calculate the angles required to rotate the motors to align the drone with the center.
        Returns a tuple of (angle_x, angle_y) in degrees.
        """
        diff_x, diff_y = self.difference_between_drone_and_center(drone_x, drone_y, center_x, center_y)
        
        # Assuming the screen coordinates are in pixels and the rotation angles are proportional
        # to the difference in position, we calculate the angles using simple trigonometry.
        
        angle_x = math.degrees(math.atan2(diff_x, center_x))  # Rotation angle for x-axis
        angle_y = math.degrees(math.atan2(diff_y, center_y))  # Rotation angle for y-axis
        
        return angle_x, angle_y
    
    def rotate_x(self, angle):
        """
        Rotate the device around the x-axis by the specified angle.
        The angle is in degrees.
        """
        self.x_motor += angle
        print(f"Rotating X-axis by {angle} degrees. Current angle: {self.rotate_x} degrees.")
        
    def rotate_y(self, angle):
        """
        Rotate the device around the y-axis by the specified angle.
        The angle is in degrees.
        """
        self.y_motor += angle
        print(f"Rotating Y-axis by {angle} degrees. Current angle: {self.rotate_y} degrees.")
        
    def rotate_motors(self):
        """
        We can't rotate motors due to the 
        """
        pass
        
if __name__ == "__main__":
    rotate_module = RotateModule()
    rotate_module.rotate_x(30)
    rotate_module.rotate_y(45)
    rotate_module.rotate_motors()
    print("Rotation complete.", rotate_module.x_motor, rotate_module.y_motor)
    difference = rotate_module.difference_between_drone_and_center(120, 120, 200, 200) # screen 400x400 px and drone center is 120, 120
    print(f"Difference between drone and center: {difference}")
    angles = rotate_module.calculate_rotation_angles(120, 120, 200, 200)
    print(f"Calculated rotation angles: {angles}")