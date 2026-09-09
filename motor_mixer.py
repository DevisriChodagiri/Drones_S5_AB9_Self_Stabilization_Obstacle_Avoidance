class MotorMixer:
    """
    Converts total thrust and attitude corrections
    into four individual motor thrust values.

    Motor arrangement:

                FRONT
                  ↑
          M1              M2
             \          /
              \  DRONE /
              /        \
             /          \
          M4              M3
                  ↓
                 BACK
    """

    def __init__(self, max_thrust=5.0):

        # Maximum thrust that one motor can produce
        self.max_thrust = max_thrust

    def calculate_motor_thrust(
        self,
        total_thrust,
        roll_correction,
        pitch_correction,
        yaw_correction
    ):

        # -------------------------------------------------
        # Step 1: Start with equal thrust for all motors
        # -------------------------------------------------

        base_thrust = total_thrust / 4.0

        # -------------------------------------------------
        # Step 2: Roll correction
        # -------------------------------------------------
        # Roll changes the thrust difference between
        # the left and right sides.

        motor_1 = base_thrust - roll_correction
        motor_2 = base_thrust + roll_correction
        motor_3 = base_thrust + roll_correction
        motor_4 = base_thrust - roll_correction

        # -------------------------------------------------
        # Step 3: Pitch correction
        # -------------------------------------------------
        # Pitch changes the thrust difference between
        # the front and back motors.

        motor_1 = motor_1 - pitch_correction
        motor_2 = motor_2 - pitch_correction

        motor_3 = motor_3 + pitch_correction
        motor_4 = motor_4 + pitch_correction

        # -------------------------------------------------
        # Step 4: Yaw correction
        # -------------------------------------------------
        # Yaw is produced by changing the thrust pattern
        # between opposite rotating motors.

        motor_1 = motor_1 + yaw_correction
        motor_2 = motor_2 - yaw_correction
        motor_3 = motor_3 + yaw_correction
        motor_4 = motor_4 - yaw_correction

        # -------------------------------------------------
        # Step 5: Keep motor thrust within physical limits
        # -------------------------------------------------

        motor_1 = self.limit_thrust(motor_1)
        motor_2 = self.limit_thrust(motor_2)
        motor_3 = self.limit_thrust(motor_3)
        motor_4 = self.limit_thrust(motor_4)

        return motor_1, motor_2, motor_3, motor_4

    def limit_thrust(self, thrust):

        if thrust < 0.0:
            return 0.0

        if thrust > self.max_thrust:
            return self.max_thrust

        return thrust