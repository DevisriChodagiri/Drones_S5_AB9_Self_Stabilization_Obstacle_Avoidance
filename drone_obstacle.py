import time
import math
import numpy as np
import pybullet as p

from gym_pybullet_drones.envs.CtrlAviary import CtrlAviary
from gym_pybullet_drones.control.DSLPIDControl import DSLPIDControl
from gym_pybullet_drones.utils.enums import DroneModel, Physics

from ml_model import predict_safety


# ============================================================
# CONFIGURATION
# ============================================================

DRONE_MODEL = DroneModel.CF2X
PHYSICS = Physics.PYB

NUM_DRONES = 1

INITIAL_XYZ = np.array([
    [0.0, 0.0, 1.0]
])

INITIAL_RPYS = np.array([
    [0.0, 0.0, 0.0]
])

TARGET_HEIGHT = 1.0

# Obstacle position
OBSTACLE_X = 3.0
OBSTACLE_Y = 0.0
OBSTACLE_Z = 0.5

# Obstacle dimensions
OBSTACLE_HALF_X = 0.3
OBSTACLE_HALF_Y = 0.5
OBSTACLE_HALF_Z = 0.5

# Ultrasonic safety distance
SAFETY_DISTANCE = 0.8

# Distance at which avoidance starts
AVOID_DISTANCE = 1.2

# Forward movement
FORWARD_STEP = 0.04

# Side movement during avoidance
SIDE_STEP = 0.04

# Maximum allowed roll/pitch before declaring instability
MAX_ATTITUDE = 45.0

# Simulation time
SIMULATION_TIME = 15.0

# Display frequency
PRINT_EVERY = 0.5


# ============================================================
# ULTRASONIC SENSOR
# ============================================================

def get_distance_to_obstacle(drone_position):
    """
    Simulated ultrasonic sensor.

    Measures distance from the drone to the front face
    of the obstacle along the +X direction.
    """

    drone_x = drone_position[0]
    drone_y = drone_position[1]

    # Only consider the obstacle if it is roughly in front
    # of the drone.
    if abs(drone_y - OBSTACLE_Y) > (
        OBSTACLE_HALF_Y + 0.15
    ):
        return 10.0

    obstacle_front = OBSTACLE_X - OBSTACLE_HALF_X

    distance = obstacle_front - drone_x

    return max(distance, 0.0)


# ============================================================
# ANGLE WRAPPING
# ============================================================

def wrap_angle(angle):
    """
    Converts angle to [-pi, pi].
    """

    return (angle + np.pi) % (2 * np.pi) - np.pi


# ============================================================
# MAIN PROGRAM
# ============================================================

print()
print("======================================")
print("PID + ULTRASONIC OBSTACLE AVOIDANCE")
print("======================================")
print()

print(
    "Target Position: "
    f"X=+0.00 Y=+0.00 Z={TARGET_HEIGHT:+.2f}"
)

print(
    "Obstacle Position: "
    f"X={OBSTACLE_X:+.2f} "
    f"Y={OBSTACLE_Y:+.2f}"
)

print(
    f"Safety Distance = {SAFETY_DISTANCE:.2f} m"
)

print(
    f"Avoidance Distance = {AVOID_DISTANCE:.2f} m"
)

print()


# ============================================================
# CREATE ENVIRONMENT
# ============================================================

env = None

try:

    env = CtrlAviary(
        drone_model=DRONE_MODEL,
        num_drones=NUM_DRONES,
        initial_xyzs=INITIAL_XYZ,
        initial_rpys=INITIAL_RPYS,
        physics=PHYSICS,
        pyb_freq=240,
        ctrl_freq=48,
        gui=True,
        record=False,
        obstacles=False,
        user_debug_gui=False
    )


    # ========================================================
    # CREATE OBSTACLE
    # ========================================================

    obstacle_collision = p.createCollisionShape(
        p.GEOM_BOX,
        halfExtents=[
            OBSTACLE_HALF_X,
            OBSTACLE_HALF_Y,
            OBSTACLE_HALF_Z
        ],
        physicsClientId=env.CLIENT
    )

    obstacle_visual = p.createVisualShape(
        p.GEOM_BOX,
        halfExtents=[
            OBSTACLE_HALF_X,
            OBSTACLE_HALF_Y,
            OBSTACLE_HALF_Z
        ],
        rgbaColor=[1, 0, 0, 1],
        physicsClientId=env.CLIENT
    )

    obstacle_id = p.createMultiBody(
        baseMass=0,
        baseCollisionShapeIndex=obstacle_collision,
        baseVisualShapeIndex=obstacle_visual,
        basePosition=[
            OBSTACLE_X,
            OBSTACLE_Y,
            OBSTACLE_Z
        ],
        physicsClientId=env.CLIENT
    )

    print("Red obstacle created.")
    print()


    # ========================================================
    # CREATE PID CONTROLLER
    # ========================================================

    controller = DSLPIDControl(
        drone_model=DRONE_MODEL
    )

    print("DSLPID controller created.")
    print()


    # ========================================================
    # RESET ENVIRONMENT
    # ========================================================

    obs, info = env.reset(
        seed=42
    )

    print("Drone initialized.")
    print()


    # ========================================================
    # TARGET STATE
    # ========================================================

    target_pos = np.array([
        0.0,
        0.0,
        TARGET_HEIGHT
    ])

    target_rpy = np.array([
        0.0,
        0.0,
        0.0
    ])

    target_vel = np.zeros(3)

    target_rpy_rates = np.zeros(3)


    # ========================================================
    # SIMULATION VARIABLES
    # ========================================================

    start_time = time.time()

    last_print_time = -PRINT_EVERY

    avoidance_mode = False

    avoidance_direction = 1.0

    passed_obstacle = False

    stable_count = 0


    # ========================================================
    # MAIN LOOP
    # ========================================================

    while True:

        current_time = time.time() - start_time

        if current_time >= SIMULATION_TIME:
            break


        # ----------------------------------------------------
        # GET DRONE STATE
        # ----------------------------------------------------

        state = env._getDroneStateVector(0)

        current_pos = np.array(
            state[0:3]
        )

        current_quat = np.array(
            state[3:7]
        )

        current_vel = np.array(
            state[10:13]
        )

        current_ang_vel = np.array(
            state[13:16]
        )


        # ----------------------------------------------------
        # GET EULER ANGLES
        # ----------------------------------------------------

        current_rpy = np.array(
            p.getEulerFromQuaternion(
                current_quat
            )
        )

        roll = math.degrees(
            current_rpy[0]
        )

        pitch = math.degrees(
            current_rpy[1]
        )

        yaw = math.degrees(
            current_rpy[2]
        )


        # ----------------------------------------------------
        # SPEED
        # ----------------------------------------------------

        speed = float(
            np.linalg.norm(
                current_vel
            )
        )


        # ----------------------------------------------------
        # ULTRASONIC SENSOR
        # ----------------------------------------------------

        distance = get_distance_to_obstacle(
            current_pos
        )


        # ----------------------------------------------------
        # OBSTACLE AVOIDANCE
        # ----------------------------------------------------

        if not avoidance_mode and distance <= AVOID_DISTANCE:

            avoidance_mode = True

            # Choose a side depending on current Y.
            if current_pos[1] >= 0:
                avoidance_direction = -1.0
            else:
                avoidance_direction = 1.0

            print()
            print("======================================")
            print("OBSTACLE DETECTED")
            print(
                f"Distance = {distance:.3f} m"
            )
            print(
                "Starting obstacle avoidance..."
            )
            print("======================================")
            print()


        # ----------------------------------------------------
        # NORMAL FORWARD FLIGHT
        # ----------------------------------------------------

        if not avoidance_mode:

            target_pos[0] += FORWARD_STEP

            target_pos[1] = 0.0

            target_pos[2] = TARGET_HEIGHT


        # ----------------------------------------------------
        # OBSTACLE AVOIDANCE MODE
        # ----------------------------------------------------

        else:

            # Move sideways around obstacle.
            target_pos[1] += (
                avoidance_direction *
                SIDE_STEP
            )

            target_pos[2] = TARGET_HEIGHT

            # Continue moving forward slowly.
            target_pos[0] += (
                FORWARD_STEP * 0.5
            )


        # ----------------------------------------------------
        # AFTER PASSING OBSTACLE
        # ----------------------------------------------------

        if (
            avoidance_mode
            and current_pos[0] >
            OBSTACLE_X + OBSTACLE_HALF_X + 0.8
        ):

            if not passed_obstacle:

                passed_obstacle = True

                avoidance_mode = False

                print()
                print(
                    "Obstacle successfully passed."
                )
                print(
                    "Returning toward center path."
                )
                print()


            # Slowly return to Y = 0.
            target_pos[1] *= 0.95

            if abs(target_pos[1]) < 0.02:
                target_pos[1] = 0.0


        # ----------------------------------------------------
        # PID CONTROLLER
        # ----------------------------------------------------

        control_timestep = 1.0 / env.CTRL_FREQ

        rpm, pos_error, yaw_error = (
            controller.computeControl(
                control_timestep=control_timestep,
                cur_pos=current_pos,
                cur_quat=current_quat,
                cur_vel=current_vel,
                cur_ang_vel=current_ang_vel,
                target_pos=target_pos,
                target_rpy=target_rpy,
                target_vel=target_vel,
                target_rpy_rates=target_rpy_rates
            )
        )


        # ----------------------------------------------------
        # SAFETY RPM LIMIT
        # ----------------------------------------------------

        rpm = np.asarray(
            rpm,
            dtype=float
        )

        rpm = np.clip(
            rpm,
            9440.3,
            20000.0
        )


        # ----------------------------------------------------
        # SEND MOTOR COMMAND
        # ----------------------------------------------------

        obs, reward, terminated, truncated, info = (
            env.step(rpm.reshape(1, 4))
        )


        # ----------------------------------------------------
        # ML SAFETY PREDICTION
        # ----------------------------------------------------

        try:

            prediction, probability = (
                predict_safety(
                    distance,
                    speed,
                    roll,
                    pitch
                )
            )

            if prediction == 1:
                safety_result = "SAFE"
            else:
                safety_result = "UNSAFE"

        except Exception:

            safety_result = "ML ERROR"

            probability = None


        # ----------------------------------------------------
        # STABILITY CHECK
        # ----------------------------------------------------

        if (
            abs(roll) < MAX_ATTITUDE
            and abs(pitch) < MAX_ATTITUDE
        ):

            stable_count += 1

        else:

            print()
            print(
                "WARNING: Drone attitude is unstable!"
            )

            print(
                f"Roll={roll:+.2f}°"
            )

            print(
                f"Pitch={pitch:+.2f}°"
            )


        # ----------------------------------------------------
        # PRINT STATUS
        # ----------------------------------------------------

        if (
            current_time - last_print_time
            >= PRINT_EVERY
        ):

            last_print_time = current_time

            print(
                f"Time={current_time:.2f}s | "
                f"X={current_pos[0]:+.3f} | "
                f"Y={current_pos[1]:+.3f} | "
                f"Z={current_pos[2]:+.3f} | "
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
                "| Min=",
                round(float(np.min(rpm)), 2),
                "| Max=",
                round(float(np.max(rpm)), 2)
            )

            print(
                f"Distance={distance:.3f} m | "
                f"ML={safety_result}"
            )

            print(
                f"Target: "
                f"X={target_pos[0]:+.2f} "
                f"Y={target_pos[1]:+.2f} "
                f"Z={target_pos[2]:+.2f}"
            )

            if avoidance_mode:
                print(
                    "MODE: OBSTACLE AVOIDANCE"
                )
            else:
                print(
                    "MODE: NORMAL FLIGHT"
                )

            print()


        # ----------------------------------------------------
        # TERMINATION CHECK
        # ----------------------------------------------------

        if terminated or truncated:
            print(
                "Environment terminated."
            )
            break


        # ----------------------------------------------------
        # ADDITIONAL PYBULLET TIME
        # ----------------------------------------------------

        time.sleep(0.005)


except KeyboardInterrupt:

    print()
    print(
        "Simulation stopped by user."
    )


except Exception as e:

    print()
    print(
        "ERROR:"
    )

    print(
        type(e).__name__,
        ":",
        e
    )


finally:

    if env is not None:

        env.close()

    print()
    print("======================================")
    print("PID + OBSTACLE TEST COMPLETED")
    print("======================================")