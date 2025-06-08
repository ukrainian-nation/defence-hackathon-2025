import math
import serial
import struct


class RotateModule:
    """
    Handles rotation of a 2-axis device via motors.
    Useful for camera/gimbal tracking based on image position.
    """

    def __init__(self):
        """
        Initializes serial connection and motor parameters.
        """
        try:
            self.ser = serial.Serial('/dev/tty.usbserial-XXXX', 115200, timeout=0.1)  # Change this to your macOS port
        except serial.SerialException as e:
            print(f"Serial port error: {e}")
            self.ser = None

        self.ticks_per_rev = 90
        self.deg_per_tick = 360.0 / self.ticks_per_rev
        self.Kp = 2.0
        self.Ki = 0.01
        self.Kd = 0.05
        self.x_motor = 0
        self.y_motor = 0

    def normalize_angle(self, angle):
        """Wraps angle to 0–360."""
        return angle % 360

    @staticmethod
    def angle_difference(target_angle, current_angle):
        """Returns shortest angle difference in range -180 to 180."""
        diff = (target_angle - current_angle + 180) % 360 - 180
        return diff

    def good_angle(self):
        """Check if angles are within allowed range."""
        if self.x_motor > 180 or self.x_motor < -180:
            print("X motor angle out of range. Resetting to safe position.")
            return False
        if self.y_motor > 45 or self.y_motor < -90:
            print("Y motor angle out of range. Resetting to safe position.")
            return False
        return True

    def setup_basic_position(self):
        """Initialize motors to zero."""
        self.x_motor = 0
        self.y_motor = 0
        print("Motors set to default position (0°, 0°)")

    def tracking(self, drone_x, drone_y, center_x, center_y):
        """Tracks object by calculating required angles and rotating motors."""
        angle_x, angle_y = self.calculate_rotation_angles(drone_x, drone_y, center_x, center_y)
        print(f"Tracking: rotating to ({angle_x:.2f}°, {angle_y:.2f}°)")
        self.rotate_x(angle_x)
        self.rotate_y(angle_y)

    def difference_between_drone_and_center(self, drone_x, drone_y, center_x, center_y):
        """Returns pixel difference between drone and center."""
        return drone_x - center_x, drone_y - center_y

    def calculate_rotation_angles(self, drone_x, drone_y, center_x, center_y, image_width=640, image_height=640, fov_x=31.05, fov_y=22.1):
        """Converts pixel offset to angular offset based on FoV."""
        diff_x = drone_x - center_x
        diff_y = drone_y - center_y

        deg_per_px_x = fov_x / image_width
        deg_per_px_y = fov_y / image_height

        angle_x = diff_x * deg_per_px_x
        angle_y = diff_y * deg_per_px_y

        return angle_x, angle_y

    def rotate_x(self, angle):
        """Rotates X motor by given angle if safe."""
        self.x_motor += angle
        if not self.good_angle():
            self.x_motor -= angle
            print("X-axis rotation aborted.")
        else:
            print(f"Rotating X-axis by {angle:.2f}°, current X: {self.x_motor:.2f}°")
            # You'd send angle to actual motor here via serial if desired

    def rotate_y(self, angle):
        """Rotates Y motor by given angle if safe."""
        self.y_motor += angle
        if not self.good_angle():
            self.y_motor -= angle
            print("Y-axis rotation aborted.")
        else:
            print(f"Rotating Y-axis by {angle:.2f}°, current Y: {self.y_motor:.2f}°")
            # You'd send angle to actual motor here via serial if desired

    def rotate_motors(self):
        """Placeholder to actually trigger motor commands."""
        if self.ser:
            # Here you’d convert angles to protocol messages, then send
            # Example: self.ser.write(struct.pack('>2f', self.x_motor, self.y_motor))
            print(f"Sending to motors: X={self.x_motor}°, Y={self.y_motor}°")
        else:
            print("Serial not connected. Skipping motor write.")


if __name__ == "__main__":
    rotate_module = RotateModule()
    rotate_module.rotate_x(30)
    rotate_module.rotate_y(45)
    rotate_module.rotate_motors()

    # Test difference and angle calculation
    difference = rotate_module.difference_between_drone_and_center(120, 120, 200, 200)
    print(f"Pixel difference: {difference}")

    angles = rotate_module.calculate_rotation_angles(120, 120, 200, 200)
    print(f"Calculated rotation angles: {angles}")

    # Optional tracking example
    rotate_module.tracking(120, 120, 200, 200)
