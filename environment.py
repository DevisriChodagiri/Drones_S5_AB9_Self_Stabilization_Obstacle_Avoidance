import pybullet as p


class Environment:

    def __init__(self):

        self.obstacles = []

    def add_static_obstacle(self, position, size):

        # Create the collision shape of the obstacle
        collision_shape = p.createCollisionShape(
            p.GEOM_BOX,
            halfExtents=size
        )

        # Create the obstacle in the simulation
        obstacle_id = p.createMultiBody(
            baseMass=0,
            baseCollisionShapeIndex=collision_shape,
            basePosition=position
        )

        # Store the obstacle ID
        self.obstacles.append(obstacle_id)

        return obstacle_id

    def get_obstacles(self):

        return self.obstacles