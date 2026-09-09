import time

from simulation.physics import PhysicsWorld
from simulation.drone import Drone
from simulation.environment import Environment
from control.motor_mixer import MotorMixer


def main():

    print("Starting drone simulation...")

    # ---------------------------------------------
    # CREATE PHYSICS WORLD
    # ---------------------------------------------

    physics = PhysicsWorld()

    # ---------------------------------------------
    # CREATE DRONE
    # ---------------------------------------------

    drone = Drone()

    # ---------------------------------------------
    # CREATE ENVIRONMENT
    # ---------------------------------------------

    environment = Environment()

    # Test obstacle
    environment.add_static_obstacle(
        position=[3, 0, 0.5],
        size=[0.5, 0.5, 0.5]
    )

    # ---------------------------------------------
    # CREATE MOTOR MIXER
    # ---------------------------------------------

    mixer = MotorMixer(
        max_thrust=5.0
    )

    # ---------------------------------------------
    # DRONE PARAMETERS
    # ---------------------------------------------

    mass = drone.mass
    gravity = 9.81

    # Required thrust for hovering
    hover_thrust = mass * gravity

    print("Mass:", mass, "kg")
    print("Gravity:", gravity, "m/s^2")
    print("Required hover thrust:", hover_thrust, "N")

    # ---------------------------------------------
    # CALCULATE MOTOR THRUST
    # ---------------------------------------------

    motor_1, motor_2, motor_3, motor_4 = mixer.calculate_motor_thrust(
        total_thrust=hover_thrust,
        roll_correction=0.0,
        pitch_correction=0.0,
        yaw_correction=0.0
    )

    print("Motor 1 thrust:", motor_1, "N")
    print("Motor 2 thrust:", motor_2, "N")
    print("Motor 3 thrust:", motor_3, "N")
    print("Motor 4 thrust:", motor_4, "N")

    # ---------------------------------------------
    # APPLY MOTOR THRUST
    # ---------------------------------------------

    drone.apply_motor_forces(
        motor_1,
        motor_2,
        motor_3,
        motor_4
    )

    print("Simulation is running...")

    # ---------------------------------------------
    # SIMULATION LOOP
    # ---------------------------------------------

    for step in range(1200):

        physics.step()

        # Re-apply motor thrust every simulation step
        drone.apply_motor_forces(
            motor_1,
            motor_2,
            motor_3,
            motor_4
        )

        # Print position once every second
        if step % 240 == 0:

            position = drone.get_position()

            print(
                "Time:",
                round(step / 240, 2),
                "seconds",
                "Drone position:",
                position
            )

        time.sleep(physics.time_step)

    print("Simulation finished.")

    physics.close()


if __name__ == "__main__":
    main()