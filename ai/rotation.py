import math


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
        self.x_motor = None  # Placeholder for x-axis motor control
        self.y_motor = None  # Placeholder for y-axis motor control
        pass
    
    def scan(self):
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
        pass

        def difference_between_drone_and_center(self, drone_x, drone_y, center_x, center_y):
            """
            Calculate the difference between the drone's position and the center position.
            This is used to determine how much to rotate the drone to face the center.
            Returns a tuple of (diff_x, diff_y).
            """
            diff_x = center_x - drone_x
            diff_y = center_y - drone_y
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
        self.x_angle += angle
        print(f"Rotating X-axis by {angle} degrees. Current angle: {self.x_angle} degrees.")
        
    def rotate_y(self, angle):
        """
        Rotate the device around the y-axis by the specified angle.
        The angle is in degrees.
        """
        self.y_angle += angle
        print(f"Rotating Y-axis by {angle} degrees. Current angle: {self.y_angle} degrees.")
        
    def rotate_motors(self):
        pass
        