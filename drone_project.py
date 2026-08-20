import time
import math
import numpy as np
import pybullet as p

from gym_pybullet_drones.envs.CtrlAviary import CtrlAviary
from gym_pybullet_drones.control.DSLPIDControl import DSLPIDControl
from gym_pybullet_drones.utils.enums import DroneModel, Physics

from ml_model import predict_safety


# ============================================================
# AUTONOMOUS SELF-STABILIZING DRONE
# PID + ULTRASONIC + LOGISTIC REGRESSION
# STABLE DEMONSTRATION VERSION
# ============================================================

print()
print("======================================")
print("AUTONOMOUS DRONE PROJECT")
print("PID + ULTRASONIC + LOGISTIC REGRESSION")
print("STABLE DEMONSTRATION")
print("======================================")
print()


# ============================================================
# CONFIGURATION
# ============================================================

DRONE_MODEL = DroneModel.CF2X

SIMULATION_FREQ = 240
CONTROL_FREQ = 48

DURATION_SEC = 60.0

GUI = True


# ============================================================
# INITIAL POSITION
# ============================================================

INITIAL_XYZ = np.array([
    [0.0, 0.0, 1.0]
])

INITIAL_RPYS = np.array([
    [0.0, 0.0, 0.0]
])


# ============================================================
# TARGET
# ============================================================

TARGET_Z = 1.0
FINAL_X = 7.0


# ============================================================
# VERY SLOW FLIGHT
# ============================================================

FORWARD_SPEED = 0.03
SIDE_SPEED = 0.02

POSITION_STEP = 0.015


# ============================================================
# OBSTACLE
# ============================================================

OBSTACLE_X = 5.0

BRAKE_DISTANCE = 1.5

AVOID_DISTANCE = 0.50

PASS_DISTANCE = 0.80


# ============================================================
# SAFETY
# ============================================================

# Keep these conservative.
WARNING_ANGLE = 10.0
EMERGENCY_ANGLE = 30.0


# ============================================================
# ENVIRONMENT
# ============================================================

env = CtrlAviary(
    drone_model=DRONE_MODEL,
    num_drones=1,
    initial_xyzs=INITIAL_XYZ,
    initial_rpys=INITIAL_RPYS,
    physics=Physics.PYB,
    pyb_freq=SIMULATION_FREQ,
    ctrl_freq=CONTROL_FREQ,
    gui=GUI,
    record=False,
    obstacles=False,
    user_debug_gui=False
)


# ============================================================
# PID CONTROLLER
# ============================================================

controller = DSLPIDControl(
    drone_model=DRONE_MODEL
)


# ============================================================
# RESET
# ============================================================

obs, info = env.reset(seed=42)


# ============================================================
# TARGET VARIABLES
# ============================================================

target_pos = np.array(
    [0.0, 0.0, TARGET_Z],
    dtype=float
)

target_rpy = np.array(
    [0.0, 0.0, 0.0],
    dtype=float
)

target_vel = np.zeros(3)

target_rpy_rates = np.zeros(3)


# ============================================================
# MODES
# ============================================================

MODE_HOVER = "HOVER"
MODE_FORWARD = "FORWARD"
MODE_BRAKE = "BRAKE"
MODE_AVOID = "AVOID"
MODE_PASS = "PASS"
MODE_RETURN = "RETURN"
MODE_FINISH = "FINISH"

mode = MODE_HOVER


# ============================================================
# VARIABLES
# ============================================================

avoid_target_y = 0.0

avoid_side = -1.0

brake_start_time = None


# ============================================================
# ULTRASONIC SENSOR MODEL
# ============================================================

def ultrasonic_distance(x):

    distance = OBSTACLE_X - x

    if distance < 0:

        distance = 0.0

    return distance


# ============================================================
# GET DRONE STATE
# ============================================================

def get_state():

    state = env._getDroneStateVector(0)

    pos = np.array(
        state[0:3],
        dtype=float
    )

    quat = np.array(
        state[3:7],
        dtype=float
    )

    vel = np.array(
        state[10:13],
        dtype=float
    )

    ang_vel = np.array(
        state[13:16],
        dtype=float
    )

    return pos, quat, vel, ang_vel


# ============================================================
# GET ATTITUDE
# ============================================================

def get_angles(quat):

    roll, pitch, yaw = p.getEulerFromQuaternion(quat)

    return (
        math.degrees(roll),
        math.degrees(pitch),
        math.degrees(yaw)
    )


# ============================================================
# PID CONTROL
# ============================================================

def pid_control(
    pos,
    quat,
    vel,
    ang_vel
):

    rpm, pos_error, yaw_error = controller.computeControl(
        control_timestep=1.0 / CONTROL_FREQ,

        cur_pos=pos,

        cur_quat=quat,

        cur_vel=vel,

        cur_ang_vel=ang_vel,

        target_pos=target_pos,

        target_rpy=target_rpy,

        target_vel=target_vel,

        target_rpy_rates=target_rpy_rates
    )

    rpm = np.asarray(
        rpm,
        dtype=float
    )

    # Do NOT force an artificial 12000-16000 RPM range.
    #
    # The PID controller already calculates the required
    # motor RPM.

    rpm = np.clip(
        rpm,
        9440.3,
        18000.0
    )

    return rpm, pos_error, yaw_error


# ============================================================
# START MESSAGE
# ============================================================

print("Obstacle:")
print(
    f"X=+{OBSTACLE_X:.2f} m"
)

print()

print("Final target:")
print(
    f"X=+{FINAL_X:.2f} "
    f"Y=+0.00 "
    f"Z=+{TARGET_Z:.2f}"
)

print()

print("Starting stable hover...")
print()


# ============================================================
# TIMING
# ============================================================

start_time = time.time()

last_print = 0.0

counter = 0

control_interval = int(
    SIMULATION_FREQ / CONTROL_FREQ
)


# ============================================================
# INITIAL MOTOR COMMAND
# ============================================================

action = np.array(
    [[14468.43, 14468.43, 14468.43, 14468.43]],
    dtype=float
)


# ============================================================
# MAIN LOOP
# ============================================================

try:

    while True:

        elapsed = time.time() - start_time


        # ----------------------------------------------------
        # TIME LIMIT
        # ----------------------------------------------------

        if elapsed >= DURATION_SEC:

            print()
            print("Simulation completed.")

            break


        # ----------------------------------------------------
        # STATE
        # ----------------------------------------------------

        pos, quat, vel, ang_vel = get_state()

        x = float(pos[0])
        y = float(pos[1])
        z = float(pos[2])


        # ----------------------------------------------------
        # ATTITUDE
        # ----------------------------------------------------

        roll, pitch, yaw = get_angles(quat)


        # ----------------------------------------------------
        # SPEED
        # ----------------------------------------------------

        speed = float(
            np.linalg.norm(vel)
        )


        # ----------------------------------------------------
        # ULTRASONIC
        # ----------------------------------------------------

        distance = ultrasonic_distance(x)


        # ----------------------------------------------------
        # MACHINE LEARNING
        # ----------------------------------------------------

        try:

            prediction, probability = predict_safety(
                distance * 100.0,
                speed,
                roll,
                pitch
            )

            if prediction == 1:

                ml_result = "SAFE"

            else:

                ml_result = "UNSAFE"

        except Exception:

            ml_result = "ERROR"


        # ====================================================
        # CONTROL UPDATE
        # ====================================================

        if counter % control_interval == 0:


            # =================================================
            # HOVER
            # =================================================

            if mode == MODE_HOVER:

                target_pos[:] = [
                    0.0,
                    0.0,
                    TARGET_Z
                ]

                target_vel[:] = 0.0

                target_rpy[:] = 0.0


                if elapsed >= 5.0:

                    mode = MODE_FORWARD

                    print()
                    print("======================================")
                    print("STABLE HOVER ACHIEVED")
                    print("STARTING SLOW FORWARD FLIGHT")
                    print("======================================")
                    print()


            # =================================================
            # FORWARD
            # =================================================

            elif mode == MODE_FORWARD:

                target_rpy[:] = 0.0

                target_vel[:] = 0.0


                # Move the target forward by only a tiny amount.

                next_x = min(
                    x + POSITION_STEP,
                    FINAL_X
                )

                target_pos[:] = [
                    next_x,
                    0.0,
                    TARGET_Z
                ]


                # Very small forward velocity.

                target_vel[0] = FORWARD_SPEED


                # -------------------------------------------------
                # OBSTACLE DETECTION
                # -------------------------------------------------

                if distance <= BRAKE_DISTANCE:

                    mode = MODE_BRAKE

                    brake_start_time = elapsed

                    target_pos[:] = [
                        x,
                        y,
                        TARGET_Z
                    ]

                    target_vel[:] = 0.0

                    print()
                    print("======================================")
                    print("ULTRASONIC OBSTACLE DETECTED")
                    print(
                        f"Distance = {distance:.2f} m"
                    )
                    print("BRAKING")
                    print("======================================")
                    print()


                # -------------------------------------------------
                # FINAL TARGET
                # -------------------------------------------------

                if x >= FINAL_X - 0.10:

                    mode = MODE_FINISH

                    target_pos[:] = [
                        FINAL_X,
                        0.0,
                        TARGET_Z
                    ]

                    target_vel[:] = 0.0

                    print()
                    print("======================================")
                    print("FINAL TARGET REACHED")
                    print("======================================")
                    print()


            # =================================================
            # BRAKE
            # =================================================

            elif mode == MODE_BRAKE:

                target_pos[:] = [
                    x,
                    y,
                    TARGET_Z
                ]

                target_vel[:] = 0.0

                target_rpy[:] = 0.0


                # Wait until the drone becomes stable.

                stable = (
                    abs(roll) < WARNING_ANGLE
                    and
                    abs(pitch) < WARNING_ANGLE
                    and
                    speed < 0.10
                )


                if (
                    brake_start_time is not None
                    and
                    elapsed - brake_start_time >= 2.0
                    and
                    stable
                ):

                    avoid_target_y = (
                        y + avoid_side * AVOID_DISTANCE
                    )

                    mode = MODE_AVOID

                    print()
                    print("======================================")
                    print("DRONE STABLE")
                    print("STARTING SIDEWAYS AVOIDANCE")
                    print(
                        f"Target Y = {avoid_target_y:+.2f}"
                    )
                    print("======================================")
                    print()


            # =================================================
            # AVOID
            # =================================================

            elif mode == MODE_AVOID:

                target_rpy[:] = 0.0

                target_pos[:] = [
                    x,
                    avoid_target_y,
                    TARGET_Z
                ]

                target_vel[:] = 0.0

                target_vel[1] = (
                    avoid_side * SIDE_SPEED
                )


                # ------------------------------------------------
                # Wait until sideways movement is complete.
                # ------------------------------------------------

                if abs(y - avoid_target_y) < 0.08:

                    target_vel[:] = 0.0

                    mode = MODE_PASS

                    print()
                    print("======================================")
                    print("SIDEWAYS AVOIDANCE COMPLETED")
                    print("PASSING OBSTACLE")
                    print("======================================")
                    print()


            # =================================================
            # PASS OBSTACLE
            # =================================================

            elif mode == MODE_PASS:

                target_rpy[:] = 0.0

                target_pos[:] = [
                    min(
                        x + POSITION_STEP,
                        OBSTACLE_X + PASS_DISTANCE
                    ),
                    avoid_target_y,
                    TARGET_Z
                ]

                target_vel[:] = 0.0

                target_vel[0] = (
                    FORWARD_SPEED * 0.5
                )


                if x >= OBSTACLE_X + PASS_DISTANCE:

                    mode = MODE_RETURN

                    print()
                    print("======================================")
                    print("OBSTACLE PASSED")
                    print("RETURNING TO CENTER")
                    print("======================================")
                    print()


            # =================================================
            # RETURN
            # =================================================

            elif mode == MODE_RETURN:

                target_rpy[:] = 0.0

                target_pos[:] = [
                    min(
                        x + POSITION_STEP,
                        FINAL_X
                    ),
                    0.0,
                    TARGET_Z
                ]

                target_vel[:] = 0.0

                target_vel[0] = (
                    FORWARD_SPEED * 0.5
                )

                target_vel[1] = (
                    -avoid_side * SIDE_SPEED
                )


                if abs(y) < 0.08:

                    target_vel[1] = 0.0

                    mode = MODE_FORWARD

                    print()
                    print("======================================")
                    print("CENTER LINE RESTORED")
                    print("RESUMING FORWARD FLIGHT")
                    print("======================================")
                    print()


            # =================================================
            # FINISH
            # =================================================

            elif mode == MODE_FINISH:

                target_pos[:] = [
                    FINAL_X,
                    0.0,
                    TARGET_Z
                ]

                target_vel[:] = 0.0

                target_rpy[:] = 0.0


            # =================================================
            # ATTITUDE SAFETY
            # =================================================

            attitude_bad = (
                abs(roll) > EMERGENCY_ANGLE
                or
                abs(pitch) > EMERGENCY_ANGLE
            )


            # ------------------------------------------------
            # Emergency condition
            # ------------------------------------------------

            if attitude_bad:

                print()
                print("======================================")
                print("EMERGENCY STOP")
                print("ATTITUDE TOO LARGE")
                print(
                    f"Roll={roll:+.2f}°"
                )
                print(
                    f"Pitch={pitch:+.2f}°"
                )
                print(
                    f"Mode={mode}"
                )
                print("======================================")

                break


            # =================================================
            # HIGH ATTITUDE WARNING
            # =================================================

            if (
                abs(roll) > WARNING_ANGLE
                or
                abs(pitch) > WARNING_ANGLE
            ):

                print()
                print("WARNING: HIGH ATTITUDE")
                print(
                    f"Roll={roll:+.2f}° "
                    f"Pitch={pitch:+.2f}°"
                )
                print("REDUCING HORIZONTAL MOTION")
                print()

                # Immediately remove horizontal velocity.

                target_vel[0] = 0.0
                target_vel[1] = 0.0

                # Hold current position.

                target_pos[0] = x
                target_pos[1] = y
                target_pos[2] = TARGET_Z


            # =================================================
            # PID
            # =================================================

            rpm, pos_error, yaw_error = pid_control(
                pos,
                quat,
                vel,
                ang_vel
            )


            action = rpm.reshape(
                1,
                4
            )


        # ====================================================
        # SIMULATION STEP
        # ====================================================

        obs, reward, terminated, truncated, info = env.step(
            action
        )


        # ====================================================
        # PRINT STATUS
        # ====================================================

        if elapsed - last_print >= 0.5:

            last_print = elapsed

            print(
                f"Time={elapsed:.2f}s | "
                f"X={x:+.3f} | "
                f"Y={y:+.3f} | "
                f"Z={z:+.3f} | "
                f"Speed={speed:.3f}"
            )

            print(
                f"Roll={roll:+.2f}° | "
                f"Pitch={pitch:+.2f}° | "
                f"Yaw={yaw:+.2f}°"
            )

            print(
                "Motor RPM:",
                np.round(rpm, 2),
                "| Min:",
                round(float(np.min(rpm)), 2),
                "| Max:",
                round(float(np.max(rpm)), 2)
            )

            print(
                f"Distance={distance:.3f} m | "
                f"ML={ml_result}"
            )

            print(
                f"Target: "
                f"X={target_pos[0]:+.3f} "
                f"Y={target_pos[1]:+.3f} "
                f"Z={target_pos[2]:+.3f}"
            )

            print(
                f"MODE: {mode}"
            )

            print()


        # ====================================================
        # ENVIRONMENT TERMINATION
        # ====================================================

        if terminated or truncated:

            print()
            print("Environment terminated.")

            break


        counter += 1


except KeyboardInterrupt:

    print()
    print("Simulation stopped by user.")


finally:

    env.close()

    print()
    print("======================================")
    print("PID + ML + OBSTACLE TEST COMPLETED")
    print("======================================")

    print(
        f"Final Mode: {mode}"
    )