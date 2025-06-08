import time
import struct
import serial

ser = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=0.1)
hoverboard_CI = 0

TICKS_PER_REV = 90
DEG_PER_TICK = 360.0 / TICKS_PER_REV

# PID параметры (можно настраивать)
Kp = 2.0
Ki = 0.01
Kd = 0.05

# Переменные интеграла и дифференциала для каждого колеса
integral_left = 0
last_error_left = 0

integral_right = 0
last_error_right = 0

# Получаем абсолютное положение колёс в тиках (int32)
def get_position_ticks():
    global hoverboard_CI
    SOM = 4
    CI = (hoverboard_CI + 1) % 256
    hoverboard_CI = CI
    cmd = ord('W')
    code = 0x0C  # код позиции
    length = 0

    packet_wo_cs = struct.pack('<BBB B B', SOM, CI, length, cmd, code)
    CS = 0
    for b in packet_wo_cs[1:]:
        CS = (CS - b) % 256

    packet = packet_wo_cs + struct.pack('B', CS)
    ser.write(packet)

    response = ser.read(14)
    if len(response) != 14:
        return None, None

    try:
        _, _, _, _, r_code, p1, p2, cs = struct.unpack('<BBB B B ii B', response)
        if r_code != 0x0C:
            return None, None
        return p1, p2
    except:
        return None, None

def set_pwm(pwm_left, pwm_right):
    global hoverboard_CI
    SOM = 4
    CI = (hoverboard_CI + 1) % 256
    hoverboard_CI = CI
    cmd = ord('r')
    code = 0x0E
    length = 1 + 1 + 4 + 4

    packet_wo_cs = struct.pack('<BBB B B ii', SOM, CI, length, cmd, code, pwm_left, pwm_right)
    CS = 0
    for b in packet_wo_cs[1:]:
        CS = (CS - b) % 256
    packet = packet_wo_cs + struct.pack('B', CS)
    ser.write(packet)

def normalize_angle_deg(angle):
    """Нормализует угол в диапазон [0, 360)"""
    return angle % 360

def angle_difference(target, current):
    """Минимальная разница между углами в градусах [-180, 180]"""
    diff = (target - current + 180) % 360 - 180
    return diff

def rotate_wheels_to_angles(target_left_deg, target_right_deg, timeout=10, precision=1.0):
    global integral_left, last_error_left, integral_right, last_error_right

    integral_left = 0
    last_error_left = 0
    integral_right = 0
    last_error_right = 0

    start_time = time.time()

    while True:
        pos_left_ticks, pos_right_ticks = get_position_ticks()
        if pos_left_ticks is None or pos_right_ticks is None:
            print("Ошибка чтения позиций")
            continue

        current_left_deg = pos_left_ticks * DEG_PER_TICK
        current_right_deg = pos_right_ticks * DEG_PER_TICK

        # Разница между целевым и текущим углом
        error_left = angle_difference(target_left_deg, current_left_deg)
        error_right = angle_difference(target_right_deg, current_right_deg)

        # Проверяем достижение цели с нужной точностью
        if abs(error_left) < precision and abs(error_right) < precision:
            break

        now = time.time()
        dt = 0.05  # фиксируем dt для упрощения, можно улучшить измерением времени

        # PID для левого колеса
        integral_left += error_left * dt
        derivative_left = (error_left - last_error_left) / dt
        last_error_left = error_left

        pwm_left = int(Kp * error_left + Ki * integral_left + Kd * derivative_left)
        pwm_left = max(min(pwm_left, 1000), -1000)

        # PID для правого колеса
        integral_right += error_right * dt
        derivative_right = (error_right - last_error_right) / dt
        last_error_right = error_right

        pwm_right = int(Kp * error_right + Ki * integral_right + Kd * derivative_right)
        pwm_right = max(min(pwm_right, 1000), -1000)

        print(f"Левое колесо: {current_left_deg:.2f}° → {target_left_deg}°, PWM: {pwm_left}")
        print(f"Правое колесо: {current_right_deg:.2f}° → {target_right_deg}°, PWM: {pwm_right}")

        set_pwm(pwm_left, pwm_right)
        time.sleep(dt)

        if time.time() - start_time > timeout:
            print("Таймаут!")
            break

    set_pwm(0, 0)
    print("✅ Колёса достигли заданных углов")

# Пример запуска:
rotate_wheels_to_angles(720, 360, precision=0.5)  # Левое колесо 2 оборота, правое 1 оборот с точностью 0.5 градуса
