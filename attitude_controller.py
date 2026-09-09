from control.pid_controller import PIDController


class AttitudeController:

    def __init__(self):

        # ---------------------------------
        # ROLL PID
        # ---------------------------------

        self.roll_pid = PIDController(
            kp=0.8,
            ki=0.1,
            kd=0.05
        )

        # ---------------------------------
        # PITCH PID
        # ---------------------------------

        self.pitch_pid = PIDController(
            kp=0.8,
            ki=0.1,
            kd=0.05
        )

    def calculate_corrections(
        self,
        desired_roll,
        actual_roll,
        desired_pitch,
        actual_pitch,
        dt
    ):

        # ---------------------------------
        # ROLL PID
        # ---------------------------------

        roll_output, roll_p, roll_i, roll_d = (
            self.roll_pid.calculate(
                desired_roll,
                actual_roll,
                dt
            )
        )

        # ---------------------------------
        # PITCH PID
        # ---------------------------------

        pitch_output, pitch_p, pitch_i, pitch_d = (
            self.pitch_pid.calculate(
                desired_pitch,
                actual_pitch,
                dt
            )
        )

        return (
            roll_output,
            pitch_output,
            roll_p,
            roll_i,
            roll_d,
            pitch_p,
            pitch_i,
            pitch_d
        )