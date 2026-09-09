import pybullet as p
import math


class Drone:

    def __init__(self):

        # Physical properties
        self.mass = 1.0

        # Distance from the center of the drone
        # to each motor
        self.arm_length = 0.25

        # Create the drone body
        collision_shape = p.createCollisionShape(
            p.GEOM_BOX,
            halfExtents=[0.25, 0.25, 0.08]
        )

        self.drone_id = p.createMultiBody(
            baseMass=self.mass,
            baseCollisionShapeIndex=collision_shape,
            basePosition=[0, 0, 1]
        )

        # Start with zero velocity
        p.resetBaseVelocity(
            self.drone_id,
            linearVelocity=[0, 0, 0],
            angularVelocity=[0, 0, 0]
        )

    def get_position(self):

        position, orientation = p.getBasePositionAndOrientation(
            self.drone_id
        )

        return position

    def get_orientation(self):

        position, orientation = p.getBasePositionAndOrientation(
            self.drone_id
        )

        return orientation

    def get_velocity(self):

        linear_velocity, angular_velocity = p.getBaseVelocity(
            self.drone_id
        )

        return linear_velocity, angular_velocity

    def apply_motor_forces(
        self,
        motor_1,
        motor_2,
        motor_3,
        motor_4
    ):

        # ---------------------------------------------
        # TOTAL VERTICAL THRUST
        # ---------------------------------------------

        total_thrust = (
            motor_1 +
            motor_2 +
            motor_3 +
            motor_4
        )

        # ---------------------------------------------
        # VERTICAL FORCE
        # ---------------------------------------------

        force = [0, 0, total_thrust]

        p.applyExternalForce(
            self.drone_id,
            -1,
            force,
            [0, 0, 0],
            p.LINK_FRAME
        )

        # ---------------------------------------------
        # ROLL TORQUE
        # ---------------------------------------------

        roll_torque = (
            -motor_1
            + motor_2
            + motor_3
            - motor_4
        ) * self.arm_length

        # ---------------------------------------------
        # PITCH TORQUE
        # ---------------------------------------------

        pitch_torque = (
            -motor_1
            - motor_2
            + motor_3
            + motor_4
        ) * self.arm_length

        # ---------------------------------------------
        # YAW TORQUE
        # ---------------------------------------------

        yaw_torque = (
            motor_1
            - motor_2
            + motor_3
            - motor_4
        ) * 0.02

        # ---------------------------------------------
        # APPLY TORQUE
        # ---------------------------------------------

        torque = [
            roll_torque,
            pitch_torque,
            yaw_torque
        ]

        p.applyExternalTorque(
            self.drone_id,
            -1,
            torque,
            p.LINK_FRAME
        )