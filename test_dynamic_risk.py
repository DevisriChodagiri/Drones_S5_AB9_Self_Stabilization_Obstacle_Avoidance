import sys
import os
import pybullet as p

# -----------------------------------------
# ADD PROJECT ROOT TO PYTHON PATH
# -----------------------------------------

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from simulation.physics import PhysicsWorld
from simulation.drone import Drone
from simulation.environment import Environment
from sensors.distance_sensor import DistanceSensor
from navigation.risk_estimator import RiskEstimator


def main():

    print("Starting dynamic risk integration test...")

    # -----------------------------------------
    # 1. CREATE PHYSICS WORLD
    # -----------------------------------------

    physics = PhysicsWorld()

    # -----------------------------------------
    # 2. CREATE DRONE
    # -----------------------------------------

    drone = Drone()

    # -----------------------------------------
    # 3. CREATE ENVIRONMENT
    # -----------------------------------------

    environment = Environment()

    # -----------------------------------------
    # 4. CREATE MOVING OBSTACLE
    # -----------------------------------------

    obstacle_position = [5.0, 0.0, 1.0]

    obstacle_id = environment.add_static_obstacle(
        position=obstacle_position,
        size=[0.2, 0.2, 0.2]
    )

    # -----------------------------------------
    # 5. CREATE DISTANCE SENSOR
    # -----------------------------------------

    sensor = DistanceSensor(
        drone_id=drone.drone_id,
        max_distance=10.0
    )

    # -----------------------------------------
    # 6. CREATE RISK ESTIMATOR
    # -----------------------------------------

    risk_estimator = RiskEstimator(
        warning_ttc=5.0,
        danger_ttc=2.0,
        danger_distance=0.8
    )

    # -----------------------------------------
    # 7. MOVEMENT PARAMETERS
    # -----------------------------------------

    velocity = -0.5

    acceleration = -0.2

    dt = 0.1

    # -----------------------------------------
    # 8. GET INITIAL DISTANCE
    # -----------------------------------------

    previous_distance = (
        sensor.get_distance_to_obstacle(
            obstacle_id
        )
    )

    # -----------------------------------------
    # 9. DISPLAY HEADER
    # -----------------------------------------

    print(
        "\nTime\tDistance\tClosing\tTTC\tRisk"
    )

    print(
        "------------------------------------------------"
    )

    # -----------------------------------------
    # 10. SIMULATION LOOP
    # -----------------------------------------

    for step in range(40):

        time = step * dt

        # -------------------------------------
        # GET CURRENT OBSTACLE POSITION
        # -------------------------------------

        obstacle_position, orientation = (
            p.getBasePositionAndOrientation(
                obstacle_id
            )
        )

        current_x = obstacle_position[0]

        # -------------------------------------
        # UPDATE VELOCITY
        #
        # v = v + a * dt
        # -------------------------------------

        velocity = (
            velocity +
            acceleration * dt
        )

        # -------------------------------------
        # UPDATE POSITION
        #
        # x = x + v * dt
        # -------------------------------------

        new_x = (
            current_x +
            velocity * dt
        )

        # -------------------------------------
        # MOVE OBSTACLE
        # -------------------------------------

        p.resetBasePositionAndOrientation(
            obstacle_id,
            [new_x, 0.0, 1.0],
            orientation
        )

        # -------------------------------------
        # MEASURE DISTANCE
        # -------------------------------------

        current_distance = (
            sensor.get_distance_to_obstacle(
                obstacle_id
            )
        )

        # -------------------------------------
        # CALCULATE CLOSING SPEED
        #
        # Vc = (Dprevious - Dcurrent) / dt
        # -------------------------------------

        closing_speed = (
            previous_distance -
            current_distance
        ) / dt

        # -------------------------------------
        # CALCULATE TTC
        #
        # TTC = D / Vc
        # -------------------------------------

        if closing_speed > 0:

            ttc = (
                current_distance /
                closing_speed
            )

        else:

            ttc = float("inf")

        # -------------------------------------
        # CALCULATE RISK
        # -------------------------------------

        risk = risk_estimator.calculate_risk(
            distance=current_distance,
            closing_speed=closing_speed,
            ttc=ttc
        )

        # -------------------------------------
        # DISPLAY RESULTS
        # -------------------------------------

        print(
            f"{time:.1f}\t"
            f"{current_distance:.2f}\t\t"
            f"{closing_speed:.2f}\t"
            f"{ttc:.2f}\t"
            f"{risk}"
        )

        # -------------------------------------
        # UPDATE PREVIOUS DISTANCE
        # -------------------------------------

        previous_distance = current_distance

        # -------------------------------------
        # STEP PHYSICS
        # -------------------------------------

        physics.step()

    # -----------------------------------------
    # 11. CLOSE SIMULATION
    # -----------------------------------------

    physics.close()

    print(
        "\nDynamic risk integration test completed."
    )


if __name__ == "__main__":
    main()