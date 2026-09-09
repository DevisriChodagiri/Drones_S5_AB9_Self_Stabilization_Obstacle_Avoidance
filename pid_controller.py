class PIDController:

    def __init__(self, kp, ki, kd):
        # PID constants
        self.kp = kp
        self.ki = ki
        self.kd = kd

        # Previous error is needed for D term
        self.previous_error = 0.0

        # Accumulated error is needed for I term
        self.integral_error = 0.0

    def calculate(self, desired_value, actual_value, dt):

        # --------------------------------
        # 1. ERROR
        # --------------------------------
        error = desired_value - actual_value

        # --------------------------------
        # 2. PROPORTIONAL TERM
        # P = Kp * error
        # --------------------------------
        proportional = self.kp * error

        # --------------------------------
        # 3. INTEGRAL TERM
        # I = Ki * sum(error * dt)
        # --------------------------------
        self.integral_error = (
            self.integral_error + error * dt
        )

        integral = self.ki * self.integral_error

        # --------------------------------
        # 4. DERIVATIVE TERM
        # D = Kd * (error - previous_error) / dt
        # --------------------------------
        derivative_error = (
            (error - self.previous_error) / dt
        )

        derivative = self.kd * derivative_error

        # --------------------------------
        # 5. TOTAL PID OUTPUT
        # --------------------------------
        output = (
            proportional
            + integral
            + derivative
        )

        # Store current error for next calculation
        self.previous_error = error

        return output, proportional, integral, derivative

    def reset(self):

        self.previous_error = 0.0
        self.integral_error = 0.0