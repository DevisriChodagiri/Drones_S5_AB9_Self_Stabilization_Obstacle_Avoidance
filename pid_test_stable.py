import time
import numpy as np
import pybullet as p

from gym_pybullet_drones.envs.CtrlAviary import CtrlAviary
from gym_pybullet_drones.control.DSLPIDControl import DSLPIDControl
from gym_pybullet_drones.utils.enums import DroneModel, Physics


# ============================================================
# CONFIGURATION
# ============================================================

DRONE_MODEL = DroneModel.CF2X
PHYSICS = Physics.PYB

NUM_DRONES = 1

PYB_FREQ = 240
CTRL_FREQ = 48

INIT_XYZ = np.array([
    [0.0, 0.0, 0.1]
])

INIT_RPY = np.array([
    [0.0, 0.0, 0.0]
])

TARGET_POS = np.array([
    0.0,
    0.0,
    1.0
])

TARGET_RPY = np.array([
    0.0,
    0.0,
    0.0
])

TARGET_VEL = np.array([
    0.0,
    0.0,
    0.0
])

TARGET_RPY_RATES = np.array([
    0.0,
    0.0,
    0.0
])

SIM_TIME = 8.0

GUI = True
RECORD = False


# ============================================================
# CREATE ENVIRONMENT
# ============================================================

env = CtrlAviary(
    drone_model=DRONE_MODEL,
    num_drones=NUM_DRONES,
    initial_xyzs=INIT_XYZ,
    initial_rpys=INIT_RPY,
    physics=PHYSICS,
    pyb_freq=PYB_FREQ,
    ctrl_freq=CTRL_FREQ,
    gui=GUI,
    record=RECORD
)


# ============================================================
# CREATE DSL PID CONTROLLER
# ============================================================

controller = DSLPIDControl(
    drone_model=DRONE_MODEL
)


# ============================================================
# RESET
# ============================================================

obs, info = env.reset(seed=42)


print()
print("======================================")
print("PID STABILIZATION TEST")
print("======================================")
print()

print("Target Position:")
print(
    f"X={TARGET_POS[0]:+.2f} "
    f"Y={TARGET_POS[1]:+.2f} "
    f"Z={TARGET_POS[2]:+.2f}"
)

print()


# ============================================================
# SIMULATION
# ============================================================

step = 0
last_print_time = -1.0

try:

    while True:

        # ----------------------------------------------------
        # SIMULATION TIME
        # ----------------------------------------------------

        current_time = step / CTRL_FREQ

        if current_time >= SIM_TIME:
            break


        # ----------------------------------------------------
        # CURRENT STATE
        # ----------------------------------------------------

        state = obs[0]

        current_pos = state[0:3]

        current_quat = state[3:7]

        current_vel = state[10:13]

        current_ang_vel = state[13:16]


        # ----------------------------------------------------
        # DSL PID CONTROLLER
        # ----------------------------------------------------

        rpm, pos_error, yaw_error = (
            controller.computeControlFromState(
                control_timestep=1.0 / CTRL_FREQ,

                state=state,

                target_pos=TARGET_POS,

                target_rpy=TARGET_RPY,

                target_vel=TARGET_VEL,

                target_rpy_rates=TARGET_RPY_RATES
            )
        )


        # ----------------------------------------------------
        # CONVERT TO NUMPY ARRAY
        # ----------------------------------------------------

        rpm = np.asarray(
            rpm,
            dtype=float
        )


        # ----------------------------------------------------
        # SAFETY LIMIT
        #
        # CtrlAviary itself will clip RPM to MAX_RPM.
        # We therefore DO NOT use controller.MAX_RPM.
        # ----------------------------------------------------

        rpm = np.maximum(
            rpm,
            0.0
        )


        # ----------------------------------------------------
        # SEND RPM COMMAND
        # ----------------------------------------------------

        action = np.array([
            rpm
        ])


        obs, reward, terminated, truncated, info = env.step(
            action
        )


        # ----------------------------------------------------
        # CURRENT ORIENTATION
        # ----------------------------------------------------

        current_rpy = p.getEulerFromQuaternion(
            current_quat
        )

        roll = np.degrees(
            current_rpy[0]
        )

        pitch = np.degrees(
            current_rpy[1]
        )

        yaw = np.degrees(
            current_rpy[2]
        )


        # ----------------------------------------------------
        # SPEED
        # ----------------------------------------------------

        speed = np.linalg.norm(
            current_vel
        )


        # ----------------------------------------------------
        # PRINT EVERY 0.5 SECOND
        # ----------------------------------------------------

        if (
            last_print_time < 0
            or current_time - last_print_time >= 0.5
        ):

            print(
                f"Time={current_time:.2f}s | "
                f"X={current_pos[0]:+.3f} | "
                f"Y={current_pos[1]:+.3f} | "
                f"Z={current_pos[2]:+.3f} | "
                f"Speed={speed:.3f} | "
                f"Roll={roll:+.2f}° | "
                f"Pitch={pitch:+.2f}° | "
                f"Yaw={yaw:+.2f}°"
            )

            print(
                "Motor RPM: "
                f"{np.round(rpm, 2)} | "
                f"Min={np.min(rpm):.2f} | "
                f"Max={np.max(rpm):.2f}"
            )

            print(
                f"Position Error: "
                f"X={pos_error[0]:+.3f} "
                f"Y={pos_error[1]:+.3f} "
                f"Z={pos_error[2]:+.3f}"
            )

            print(
                f"Yaw Error={np.degrees(yaw_error):+.2f}°"
            )

            print()

            last_print_time = current_time


        # ----------------------------------------------------
        # SAFETY CHECK
        # ----------------------------------------------------

        if (
            abs(roll) > 45.0
            or
            abs(pitch) > 45.0
        ):

            print()
            print("Drone became unstable.")

            print(
                f"Roll={roll:+.2f}°"
            )

            print(
                f"Pitch={pitch:+.2f}°"
            )

            print(
                f"Yaw={yaw:+.2f}°"
            )

            break


        # ----------------------------------------------------
        # GROUND CHECK
        # ----------------------------------------------------

        if current_pos[2] < 0.05:

            print()
            print("Drone reached ground.")

            break


        # ----------------------------------------------------
        # ENVIRONMENT TERMINATION
        # ----------------------------------------------------

        if terminated or truncated:

            print()
            print("Simulation terminated.")

            break


        step += 1


finally:

    # ========================================================
    # CLOSE ENVIRONMENT
    # ========================================================

    env.close()


# ============================================================
# FINISHED
# ============================================================

print()
print("======================================")
print("PID STABILIZATION TEST COMPLETED")
print("======================================")