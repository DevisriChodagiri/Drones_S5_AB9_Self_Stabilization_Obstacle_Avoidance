import pybullet as p


class PhysicsWorld:

    def __init__(self):

        # Connect to the PyBullet graphical simulation
        self.client = p.connect(p.DIRECT)

        # Check whether the connection was successful
        if self.client < 0:
            raise RuntimeError("Could not connect to PyBullet.")

        print("PyBullet connection established.")
        print("Physics client ID:", self.client)

        # Set gravity
        p.setGravity(
            0,
            0,
            -9.81,
            physicsClientId=self.client
        )

        # Set simulation time step
        self.time_step = 1.0 / 240.0

        p.setTimeStep(
            self.time_step,
            physicsClientId=self.client
        )

        # Create the ground
        self.create_ground()

    def create_ground(self):

        # Create a flat ground collision shape
        ground_shape = p.createCollisionShape(
            p.GEOM_PLANE,
            physicsClientId=self.client
        )

        # Create the ground body
        self.ground = p.createMultiBody(
            baseMass=0,
            baseCollisionShapeIndex=ground_shape,
            basePosition=[0, 0, 0],
            physicsClientId=self.client
        )

    def step(self):

        # Check the physics connection before stepping
        if not p.isConnected(
            physicsClientId=self.client
        ):
            raise RuntimeError(
                "PyBullet connection was lost."
            )

        # Advance the physics simulation
        p.stepSimulation(
            physicsClientId=self.client
        )

    def close(self):

        # Close only our PyBullet connection
        if p.isConnected(
            physicsClientId=self.client
        ):
            p.disconnect(
                physicsClientId=self.client
            )

            print("PyBullet connection closed.")