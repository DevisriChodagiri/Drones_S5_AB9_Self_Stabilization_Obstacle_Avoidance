
import sys
import os
import math
import pickle
import pandas as pd
import pybullet as p


# =========================================================
# PROJECT ROOT
# =========================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# =========================================================
# IMPORT PROJECT MODULES
# =========================================================

from simulation.physics import PhysicsWorld
from simulation.drone import Drone

from sensors.imu import IMU

from control.attitude_controller import AttitudeController
from control.motor_mixer import MotorMixer

from navigation.decision_controller import DecisionController


# =========================================================
# DISTANCE CALCULATION
# =========================================================

def calculate_distance(
    drone_position,
    obstacle_position
):

    dx = obstacle_position[0] - drone_position[0]
    dy = obstacle_position[1] - drone_position[1]
    dz = obstacle_position[2] - drone_position[2]

    distance = math.sqrt(
        dx * dx +
        dy * dy +
        dz * dz
    )

    return distance


# =========================================================
# CLOSING SPEED
# =========================================================

def calculate_closing_speed(
    previous_distance,
    current_distance,
    dt
):

    if dt <= 0:
        return 0.0

    closing_speed = (
        previous_distance
        - current_distance
    ) / dt

    if closing_speed < 0:
        closing_speed = 0.0

    return closing_speed


# =========================================================
# TIME TO COLLISION
# =========================================================

def calculate_ttc(
    distance,
    closing_speed
):

    if closing_speed <= 0.01:
        return 20.0

    ttc = distance / closing_speed

    if ttc > 20.0:
        ttc = 20.0

    return ttc


# =========================================================
# LATERAL SEPARATION
# =========================================================

def calculate_lateral_separation(
    drone_position,
    obstacle_position
):

    return abs(
        drone_position[1]
        - obstacle_position[1]
    )


# =========================================================
# LIMIT VALUE
# =========================================================

def limit_value(
    value,
    minimum,
    maximum
):

    if value < minimum:
        return minimum

    if value > maximum:
        return maximum

    return value


# =========================================================
# CREATE DYNAMIC OBSTACLE
# =========================================================

def create_dynamic_obstacle():

    obstacle_shape = p.createCollisionShape(
        p.GEOM_BOX,
        halfExtents=[
            0.30,
            0.30,
            0.50
        ]
    )

    obstacle_id = p.createMultiBody(
        baseMass=0,
        baseCollisionShapeIndex=obstacle_shape,
        basePosition=[
            6.0,
            0.0,
            1.0
        ]
    )

    return obstacle_id


# =========================================================
# MAIN
# =========================================================

def main():

    print()
    print("================================================")
    print("       FULL DRONE SYSTEM INTEGRATION V3")
    print("================================================")
    print(" PID + ML + DYNAMIC OBSTACLE AVOIDANCE")
    print("================================================")
    print()


    # =====================================================
    # PHYSICS
    # =====================================================

    world = PhysicsWorld()


    # =====================================================
    # DRONE
    # =====================================================

    drone = Drone()


    # =====================================================
    # IMU
    # =====================================================

    imu = IMU(
        drone.drone_id
    )


    # =====================================================
    # PID CONTROLLER
    # =====================================================

    attitude_controller = (
        AttitudeController()
    )


    # =====================================================
    # MOTOR MIXER
    # =====================================================

    motor_mixer = MotorMixer(
        max_thrust=5.0
    )


    # =====================================================
    # DECISION CONTROLLER
    # =====================================================

    decision_controller = (
        DecisionController()
    )


    # =====================================================
    # LOAD ML MODEL
    # =====================================================

    model_path = os.path.join(
        PROJECT_ROOT,
        "results",
        "risk_model.pkl"
    )

    scaler_path = os.path.join(
        PROJECT_ROOT,
        "results",
        "scaler.pkl"
    )


    with open(
        model_path,
        "rb"
    ) as file:

        model = pickle.load(file)


    with open(
        scaler_path,
        "rb"
    ) as file:

        scaler = pickle.load(file)


    print("ML model loaded successfully.")
    print("Scaler loaded successfully.")
    print()


    # =====================================================
    # DYNAMIC OBSTACLE
    # =====================================================

    obstacle_id = (
        create_dynamic_obstacle()
    )

    obstacle_speed = 0.50


    # =====================================================
    # PHYSICS
    # =====================================================

    dt = 1.0 / 240.0

    mass = drone.mass

    gravity = 9.81

    hover_thrust = (
        mass * gravity
    )


    # =====================================================
    # SAFE ATTITUDE COMMANDS
    # =====================================================

    # We intentionally use very small attitude
    # references during this integration test.

    FORWARD_PITCH = -1.0

    SLOW_PITCH = -0.5

    AVOIDANCE_ROLL = 5.0


    # =====================================================
    # SAFETY LIMITS
    # =====================================================

    MAX_COMMAND_ROLL = 5.0

    MAX_COMMAND_PITCH = 1.0

    MAX_SAFE_ROLL = 20.0

    MAX_SAFE_PITCH = 20.0


    # =====================================================
    # OBSTACLE CLEARANCE
    # =====================================================

    CLEARANCE_REQUIRED = 1.0


    # =====================================================
    # SIMULATION
    # =====================================================

    simulation_time = 12.0

    total_steps = int(
        simulation_time / dt
    )


    # =====================================================
    # INITIAL DRONE POSITION
    # =====================================================

    initial_position = [
        0.0,
        0.0,
        1.0
    ]


    # =====================================================
    # INITIAL DISTURBANCE
    # =====================================================

    initial_orientation = (
        p.getQuaternionFromEuler(
            [
                math.radians(5.0),
                math.radians(3.0),
                0.0
            ]
        )
    )


    p.resetBasePositionAndOrientation(
        drone.drone_id,
        initial_position,
        initial_orientation
    )


    # =====================================================
    # INITIAL VALUES
    # =====================================================

    previous_distance = 6.0

    avoidance_active = False

    avoidance_completed = False

    emergency_recovery = False


    # =====================================================
    # LOG
    # =====================================================

    log_data = []


    # =====================================================
    # SIMULATION LOOP
    # =====================================================

    for step in range(
        total_steps
    ):

        current_time = (
            step * dt
        )


        # =================================================
        # DYNAMIC OBSTACLE MOTION
        # =================================================

        p.resetBaseVelocity(

            obstacle_id,

            linearVelocity=[
                -obstacle_speed,
                0.0,
                0.0
            ],

            angularVelocity=[
                0.0,
                0.0,
                0.0
            ]
        )


        # =================================================
        # GET DRONE POSITION
        # =================================================

        drone_position = (
            drone.get_position()
        )


        # =================================================
        # GET OBSTACLE POSITION
        # =================================================

        obstacle_position, _ = (
            p.getBasePositionAndOrientation(
                obstacle_id
            )
        )


        # =================================================
        # DISTANCE
        # =================================================

        distance = (
            calculate_distance(
                drone_position,
                obstacle_position
            )
        )


        # =================================================
        # CLOSING SPEED
        # =================================================

        closing_speed = (
            calculate_closing_speed(
                previous_distance,
                distance,
                dt
            )
        )


        # =================================================
        # TTC
        # =================================================

        ttc = (
            calculate_ttc(
                distance,
                closing_speed
            )
        )


        # =================================================
        # IMU
        # =================================================

        (
            roll,
            pitch,
            yaw
        ) = imu.get_orientation()


        # =================================================
        # ML INPUT
        # =================================================

        features = pd.DataFrame(

            [[
                distance,
                closing_speed,
                ttc,
                roll,
                pitch
            ]],

            columns=[
                "Distance",
                "ClosingSpeed",
                "TTC",
                "Roll",
                "Pitch"
            ]
        )


        # =================================================
        # SCALE
        # =================================================

        scaled_features = (
            scaler.transform(
                features
            )
        )


        # =================================================
        # ML PREDICTION
        # =================================================

        prediction = (
            model.predict(
                scaled_features
            )[0]
        )

        risk = str(
            prediction
        )


        # =================================================
        # DECISION
        # =================================================

        action = (
            decision_controller.decide(
                risk,
                distance,
                closing_speed,
                ttc
            )
        )


        # =================================================
        # DEFAULT ATTITUDE
        # =================================================

        desired_roll = 0.0

        desired_pitch = FORWARD_PITCH


        # =================================================
        # CONTINUE
        # =================================================

        if action == "CONTINUE":

            desired_roll = 0.0

            desired_pitch = FORWARD_PITCH


        # =================================================
        # SLOW DOWN
        # =================================================

        elif action == "SLOW_DOWN":

            desired_roll = 0.0

            desired_pitch = SLOW_PITCH


        # =================================================
        # AVOID
        # =================================================

        elif action == "AVOID":

            avoidance_active = True


        # =================================================
        # LATERAL SEPARATION
        # =================================================

        lateral_separation = (
            calculate_lateral_separation(
                drone_position,
                obstacle_position
            )
        )


        # =================================================
        # ACTIVE AVOIDANCE
        # =================================================

        if avoidance_active:

            desired_roll = AVOIDANCE_ROLL

            desired_pitch = 0.0


            # ---------------------------------------------
            # CHECK CLEARANCE
            # ---------------------------------------------

            if (
                lateral_separation
                >= CLEARANCE_REQUIRED
            ):

                avoidance_active = False

                avoidance_completed = True


                # Stop sideways movement command

                desired_roll = 0.0

                desired_pitch = 0.0


        # =================================================
        # ATTITUDE SAFETY CHECK
        # =================================================

        if (
            abs(roll) > MAX_SAFE_ROLL
            or
            abs(pitch) > MAX_SAFE_PITCH
        ):

            emergency_recovery = True

            desired_roll = 0.0

            desired_pitch = 0.0

            action = "RECOVER"


        # =================================================
        # LIMIT COMMAND
        # =================================================

        desired_roll = limit_value(
            desired_roll,
            -MAX_COMMAND_ROLL,
            MAX_COMMAND_ROLL
        )


        desired_pitch = limit_value(
            desired_pitch,
            -MAX_COMMAND_PITCH,
            MAX_COMMAND_PITCH
        )


        # =================================================
        # PID
        # =================================================

        (
            roll_output,
            roll_p,
            roll_i,
            roll_d,

            pitch_output,
            pitch_p,
            pitch_i,
            pitch_d

        ) = (
            attitude_controller
            .calculate_corrections(

                desired_roll,
                roll,

                desired_pitch,
                pitch,

                dt
            )
        )


        # =================================================
        # THRUST
        # =================================================

        roll_rad = math.radians(
            roll
        )

        pitch_rad = math.radians(
            pitch
        )


        denominator = (
            math.cos(roll_rad)
            *
            math.cos(pitch_rad)
        )


        if denominator < 0.8:

            denominator = 0.8


        total_thrust = (
            hover_thrust
            / denominator
        )


        # =================================================
        # LIMIT TOTAL THRUST
        # =================================================

        if total_thrust > 14.0:

            total_thrust = 14.0


        # =================================================
        # PID CORRECTIONS
        # =================================================

        roll_correction = (
            roll_output * 0.02
        )

        pitch_correction = (
            pitch_output * 0.02
        )


        # =================================================
        # MOTOR MIXER
        # =================================================

        (
            motor_1,
            motor_2,
            motor_3,
            motor_4

        ) = motor_mixer.calculate_motor_thrust(

            total_thrust,

            roll_correction,

            pitch_correction,

            0.0
        )


        # =================================================
        # APPLY MOTOR FORCES
        # =================================================

        drone.apply_motor_forces(

            motor_1,
            motor_2,
            motor_3,
            motor_4
        )


        # =================================================
        # STEP PHYSICS
        # =================================================

        world.step()


        # =================================================
        # SAVE DATA
        # =================================================

        log_data.append(

            [

                current_time,

                drone_position[0],

                drone_position[1],

                drone_position[2],

                distance,

                closing_speed,

                ttc,

                roll,

                pitch,

                desired_roll,

                desired_pitch,

                roll_p,

                roll_i,

                roll_d,

                pitch_p,

                pitch_i,

                pitch_d,

                risk,

                action,

                lateral_separation,

                motor_1,

                motor_2,

                motor_3,

                motor_4
            ]
        )


        # =================================================
        # DISPLAY
        # =================================================

        if step % 120 == 0:

            print(

                f"{current_time:5.2f}s | "

                f"D={distance:5.2f}m | "

                f"Close={closing_speed:5.2f} | "

                f"TTC={ttc:5.2f}s | "

                f"Roll={roll:6.2f} | "

                f"Pitch={pitch:6.2f} | "

                f"DR={desired_roll:5.2f} | "

                f"DP={desired_pitch:5.2f} | "

                f"Risk={risk:8s} | "

                f"Action={action:10s} | "

                f"Ysep={lateral_separation:5.2f}"
            )


        # =================================================
        # UPDATE DISTANCE
        # =================================================

        previous_distance = distance


    # =====================================================
    # DATAFRAME
    # =====================================================

    columns = [

        "Time",

        "DroneX",

        "DroneY",

        "DroneZ",

        "Distance",

        "ClosingSpeed",

        "TTC",

        "Roll",

        "Pitch",

        "DesiredRoll",

        "DesiredPitch",

        "RollP",

        "RollI",

        "RollD",

        "PitchP",

        "PitchI",

        "PitchD",

        "Risk",

        "Action",

        "LateralSeparation",

        "Motor1",

        "Motor2",

        "Motor3",

        "Motor4"
    ]


    dataframe = pd.DataFrame(

        log_data,

        columns=columns
    )


    # =====================================================
    # SAVE
    # =====================================================

    results_path = os.path.join(

        PROJECT_ROOT,

        "results",

        "full_integration_results.csv"
    )


    dataframe.to_csv(

        results_path,

        index=False
    )


    # =====================================================
    # FINAL REPORT
    # =====================================================

    print()
    print("================================================")
    print("       FULL INTEGRATION TEST COMPLETED")
    print("================================================")

    print()

    print(
        "Results saved to:"
    )

    print(
        results_path
    )

    print()

    print(
        "Avoidance completed:",
        avoidance_completed
    )

    print(
        "Emergency recovery:",
        emergency_recovery
    )

    print()

    print(
        "Final Roll:",
        round(roll, 2),
        "degrees"
    )

    print(
        "Final Pitch:",
        round(pitch, 2),
        "degrees"
    )

    print()

    print("================================================")


    # =====================================================
    # CLOSE
    # =====================================================

    world.close()


# =========================================================
# START
# =========================================================

if __name__ == "__main__":

    main()

