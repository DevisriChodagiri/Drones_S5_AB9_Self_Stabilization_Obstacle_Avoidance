
import sys
import os
import math

# ============================================================
# ADD PROJECT ROOT
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.insert(0, PROJECT_ROOT)


# ============================================================
# IMPORTS
# ============================================================

import pybullet as p

from simulation.physics import PhysicsWorld
from simulation.drone import Drone
from sensors.imu import IMU
from control.pid_controller import PIDController
from control.motor_mixer import MotorMixer


# ============================================================
# LIMIT FUNCTION
# ============================================================

def limit_value(value, minimum, maximum):

    if value < minimum:
        return minimum

    if value > maximum:
        return maximum

    return value


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 70)
    print("          PYBULLET PID SELF-STABILIZATION TEST")
    print("=" * 70)
    print("     Roll + Pitch Mathematical PID Controller")
    print("=" * 70)
    print()

    # --------------------------------------------------------
    # CREATE PHYSICS WORLD
    # --------------------------------------------------------

    world = PhysicsWorld()

    # --------------------------------------------------------
    # CREATE DRONE
    # --------------------------------------------------------

    drone = Drone()

    # --------------------------------------------------------
    # CREATE IMU
    # --------------------------------------------------------

    imu = IMU(drone.drone_id)

    # --------------------------------------------------------
    # PID CONTROLLERS
    # --------------------------------------------------------

    roll_pid = PIDController(
        kp=0.8,
        ki=0.1,
        kd=0.05
    )

    pitch_pid = PIDController(
        kp=0.8,
        ki=0.1,
        kd=0.05
    )

    # --------------------------------------------------------
    # MOTOR MIXER
    # --------------------------------------------------------

    mixer = MotorMixer(
        max_thrust=5.0
    )

    # --------------------------------------------------------
    # SIMULATION PARAMETERS
    # --------------------------------------------------------

    dt = 1.0 / 240.0

    simulation_time = 5.0

    desired_roll = 0.0

    desired_pitch = 0.0

    mass = drone.mass

    gravity = 9.81

    # Hover thrust required to balance gravity
    hover_thrust = mass * gravity

    # --------------------------------------------------------
    # INITIAL DISTURBANCE
    # --------------------------------------------------------
    #
    # We intentionally tilt the drone.
    #
    # Roll  = +10 degrees
    # Pitch = +8 degrees
    #
    # PID must bring both values back toward zero.
    # --------------------------------------------------------

    initial_roll = math.radians(10.0)

    initial_pitch = math.radians(8.0)

    initial_yaw = 0.0

    initial_orientation = p.getQuaternionFromEuler(
        [
            initial_roll,
            initial_pitch,
            initial_yaw
        ]
    )

    p.resetBasePositionAndOrientation(
        drone.drone_id,
        [0.0, 0.0, 1.0],
        initial_orientation
    )

    # Start with zero velocity
    p.resetBaseVelocity(
        drone.drone_id,
        linearVelocity=[0.0, 0.0, 0.0],
        angularVelocity=[0.0, 0.0, 0.0]
    )

    # --------------------------------------------------------
    # PRINT INITIAL CONDITIONS
    # --------------------------------------------------------

    print("Initial Roll  :", 10.0, "degrees")
    print("Initial Pitch :", 8.0, "degrees")

    print("Desired Roll  :", desired_roll, "degrees")
    print("Desired Pitch :", desired_pitch, "degrees")

    print("Kp =", roll_pid.kp)
    print("Ki =", roll_pid.ki)
    print("Kd =", roll_pid.kd)

    print()
    print("-" * 110)

    print(
        "Time | Roll | Pitch | "
        "RollErr | RollP | RollI | RollD | "
        "PitchErr | PitchP | PitchI | PitchD | "
        "M1 | M2 | M3 | M4"
    )

    print("-" * 110)

    # --------------------------------------------------------
    # SIMULATION LOOP
    # --------------------------------------------------------

    total_steps = int(
        simulation_time / dt
    )

    for step in range(total_steps):

        current_time = step * dt

        # ====================================================
        # READ IMU
        # ====================================================

        actual_roll, actual_pitch, actual_yaw = (
            imu.get_orientation()
        )

        # ====================================================
        # ROLL PID
        # ====================================================

        roll_output, roll_p, roll_i, roll_d = (
            roll_pid.calculate(
                desired_roll,
                actual_roll,
                dt
            )
        )

        # ====================================================
        # PITCH PID
        # ====================================================

        pitch_output, pitch_p, pitch_i, pitch_d = (
            pitch_pid.calculate(
                desired_pitch,
                actual_pitch,
                dt
            )
        )

        # ====================================================
        # LIMIT PID OUTPUT
        # ====================================================

        roll_output = limit_value(
            roll_output,
            -20.0,
            20.0
        )

        pitch_output = limit_value(
            pitch_output,
            -20.0,
            20.0
        )

        # ====================================================
        # CONVERT PID OUTPUT TO MOTOR CORRECTION
        # ====================================================

        roll_correction = roll_output * 0.05

        pitch_correction = pitch_output * 0.05

        yaw_correction = 0.0

        # ====================================================
        # MOTOR MIXING
        # ====================================================

        motor_1, motor_2, motor_3, motor_4 = (
            mixer.calculate_motor_thrust(
                hover_thrust,
                roll_correction,
                pitch_correction,
                yaw_correction
            )
        )

        # ====================================================
        # APPLY MOTOR FORCES
        # ====================================================

        drone.apply_motor_forces(
            motor_1,
            motor_2,
            motor_3,
            motor_4
        )

        # ====================================================
        # PRINT RESULTS EVERY 0.1 SECOND
        # ====================================================

        if step % 24 == 0:

            roll_error = (
                desired_roll - actual_roll
            )

            pitch_error = (
                desired_pitch - actual_pitch
            )

            print(
                f"{current_time:4.2f} | "
                f"{actual_roll:6.2f} | "
                f"{actual_pitch:6.2f} | "
                f"{roll_error:7.2f} | "
                f"{roll_p:6.2f} | "
                f"{roll_i:6.2f} | "
                f"{roll_d:7.2f} | "
                f"{pitch_error:8.2f} | "
                f"{pitch_p:7.2f} | "
                f"{pitch_i:7.2f} | "
                f"{pitch_d:7.2f} | "
                f"{motor_1:4.2f} | "
                f"{motor_2:4.2f} | "
                f"{motor_3:4.2f} | "
                f"{motor_4:4.2f}"
            )

        # ====================================================
        # STEP PYBULLET
        # ====================================================

        world.step()

    # ========================================================
    # FINAL ATTITUDE
    # ========================================================

    final_roll, final_pitch, final_yaw = (
        imu.get_orientation()
    )

    print()
    print("=" * 70)
    print("             PID TEST COMPLETED")
    print("=" * 70)

    print(
        f"Initial Roll  : {10.0:.2f} degrees"
    )

    print(
        f"Final Roll    : {final_roll:.2f} degrees"
    )

    print(
        f"Initial Pitch : {8.0:.2f} degrees"
    )

    print(
        f"Final Pitch   : {final_pitch:.2f} degrees"
    )

    print()

    if abs(final_roll) < 2.0:
        print("Roll stabilization: SUCCESS")
    else:
        print("Roll stabilization: NEEDS TUNING")

    if abs(final_pitch) < 2.0:
        print("Pitch stabilization: SUCCESS")
    else:
        print("Pitch stabilization: NEEDS TUNING")

    print("=" * 70)

    # ========================================================
    # CLOSE SIMULATION
    # ========================================================

    world.close()


# ============================================================
# START PROGRAM
# ============================================================

if __name__ == "__main__":
    main()

