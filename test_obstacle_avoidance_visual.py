import pybullet as p
import time
import math


# ============================================================
# 1. CONNECT TO PYBULLET
# ============================================================

client = p.connect(p.GUI)

if client < 0:
    raise RuntimeError("Could not connect to PyBullet GUI.")

print("==============================================")
print("   ZIG-ZAG 3 OBSTACLE AVOIDANCE SIMULATION")
print("==============================================")


# ============================================================
# 2. SIMULATION SETTINGS
# ============================================================

p.setGravity(0, 0, -9.81)

TIME_STEP = 1.0 / 240.0

p.setTimeStep(TIME_STEP)


# ============================================================
# 3. CAMERA
# ============================================================

p.resetDebugVisualizerCamera(
    cameraDistance=15,
    cameraYaw=0,
    cameraPitch=-45,
    cameraTargetPosition=[8, 0, 1]
)


# ============================================================
# 4. GROUND
# ============================================================

ground_shape = p.createCollisionShape(
    p.GEOM_PLANE
)

ground_id = p.createMultiBody(
    baseMass=0,
    baseCollisionShapeIndex=ground_shape,
    basePosition=[0, 0, 0]
)


# ============================================================
# 5. DRONE
# ============================================================

drone_shape = p.createCollisionShape(
    p.GEOM_BOX,
    halfExtents=[0.35, 0.35, 0.12]
)

drone_id = p.createMultiBody(
    baseMass=0,
    baseCollisionShapeIndex=drone_shape,
    basePosition=[0, 0, 1]
)


# ============================================================
# 6. CREATE OBSTACLE
# ============================================================

def create_obstacle(x, y):

    obstacle_shape = p.createCollisionShape(
        p.GEOM_BOX,
        halfExtents=[0.6, 0.8, 1.0]
    )

    obstacle_id = p.createMultiBody(
        baseMass=0,
        baseCollisionShapeIndex=obstacle_shape,
        basePosition=[x, y, 1]
    )

    return obstacle_id


# ============================================================
# 7. ZIG-ZAG OBSTACLES
# ============================================================

# Obstacle 1 → LEFT
obstacle_1 = create_obstacle(
    5.0,
    -1.8
)

# Obstacle 2 → RIGHT
obstacle_2 = create_obstacle(
    10.0,
    1.8
)

# Obstacle 3 → LEFT
obstacle_3 = create_obstacle(
    15.0,
    -1.8
)


obstacles = [
    obstacle_1,
    obstacle_2,
    obstacle_3
]


print()
print("Obstacle 1 : X = 5.0  Y = -1.8")
print("Obstacle 2 : X = 10.0 Y = +1.8")
print("Obstacle 3 : X = 15.0 Y = -1.8")
print()


# ============================================================
# 8. DISTANCE CALCULATION
# ============================================================

def calculate_distance(drone_x, drone_y, drone_z, obstacle_id):

    obstacle_position, obstacle_orientation = (
        p.getBasePositionAndOrientation(
            obstacle_id
        )
    )

    dx = obstacle_position[0] - drone_x
    dy = obstacle_position[1] - drone_y
    dz = obstacle_position[2] - drone_z

    distance = math.sqrt(
        dx * dx +
        dy * dy +
        dz * dz
    )

    return distance


# ============================================================
# 9. DRONE POSITION
# ============================================================

drone_x = 0.0
drone_y = 0.0
drone_z = 1.0


# ============================================================
# 10. SPEED SETTINGS
# ============================================================

# Good visible forward speed
FORWARD_SPEED = 2.0

# Slow down before obstacle
SLOW_SPEED = 0.8

# Sideways avoidance speed
AVOID_SPEED = 2.5

# Speed while returning to center
RETURN_SPEED = 2.0


# ============================================================
# 11. DISTANCE THRESHOLDS
# ============================================================

DETECTION_DISTANCE = 4.0

SLOW_DISTANCE = 3.0

AVOID_DISTANCE = 2.0

CLEAR_DISTANCE = 1.5


# ============================================================
# 12. FLIGHT PATH
# ============================================================

CENTER_Y = 0.0

TARGET_X = 21.0


# ============================================================
# 13. STATE VARIABLES
# ============================================================

current_obstacle_index = 0

mode = "FORWARD"

avoid_direction = 0

avoid_target_y = 0.0

obstacle_passed = False


# ============================================================
# 14. GET CURRENT OBSTACLE
# ============================================================

def get_current_obstacle():

    if current_obstacle_index >= len(obstacles):

        return None

    return obstacles[current_obstacle_index]


# ============================================================
# 15. MAIN SIMULATION
# ============================================================

start_time = time.time()

last_print_time = 0


while p.isConnected(client):

    current_time = time.time() - start_time


    # --------------------------------------------------------
    # Current obstacle
    # --------------------------------------------------------

    current_obstacle = get_current_obstacle()


    # --------------------------------------------------------
    # Distance to current obstacle
    # --------------------------------------------------------

    if current_obstacle is not None:

        distance = calculate_distance(
            drone_x,
            drone_y,
            drone_z,
            current_obstacle
        )

        obstacle_position, _ = (
            p.getBasePositionAndOrientation(
                current_obstacle
            )
        )

        obstacle_x = obstacle_position[0]
        obstacle_y = obstacle_position[1]

    else:

        distance = 999.0

        obstacle_x = 999.0
        obstacle_y = 0.0


    # ========================================================
    # MODE 1 — FORWARD
    # ========================================================

    if mode == "FORWARD":

        drone_x += (
            FORWARD_SPEED * TIME_STEP
        )


        # Detect obstacle only if it is ahead

        if current_obstacle is not None:

            x_difference = obstacle_x - drone_x

            if (
                x_difference > 0
                and distance <= DETECTION_DISTANCE
            ):

                mode = "SLOW"

                print()
                print("----------------------------------------------")
                print(
                    f"OBSTACLE {current_obstacle_index + 1} "
                    "DETECTED"
                )
                print(
                    f"Distance = {distance:.2f} m"
                )
                print("Action = SLOW DOWN")
                print("----------------------------------------------")


    # ========================================================
    # MODE 2 — SLOW
    # ========================================================

    elif mode == "SLOW":

        drone_x += (
            SLOW_SPEED * TIME_STEP
        )


        if distance <= AVOID_DISTANCE:

            # ------------------------------------------------
            # Decide avoidance direction
            # ------------------------------------------------

            if obstacle_y > drone_y:

                # Obstacle is on right
                # Move left

                avoid_direction = -1

                avoid_target_y = -2.8

            else:

                # Obstacle is on left
                # Move right

                avoid_direction = 1

                avoid_target_y = 2.8


            mode = "AVOID"

            print()
            print(
                f"Obstacle {current_obstacle_index + 1}"
            )

            print(
                "Action = AVOID"
            )

            if avoid_direction == 1:

                print("Moving RIGHT")

            else:

                print("Moving LEFT")


    # ========================================================
    # MODE 3 — AVOID
    # ========================================================

    elif mode == "AVOID":

        # Continue moving forward

        drone_x += (
            SLOW_SPEED * TIME_STEP
        )


        # Move sideways

        if drone_y < avoid_target_y:

            drone_y += (
                AVOID_SPEED * TIME_STEP
            )

        elif drone_y > avoid_target_y:

            drone_y -= (
                AVOID_SPEED * TIME_STEP
            )


        # Check whether drone passed obstacle

        if drone_x > obstacle_x + 1.2:

            obstacle_passed = True

            mode = "RETURN"

            print()
            print(
                f"Obstacle "
                f"{current_obstacle_index + 1} CLEARED"
            )

            print("Action = RETURN TO PATH")


    # ========================================================
    # MODE 4 — RETURN TO CENTER
    # ========================================================

    elif mode == "RETURN":

        # Move forward

        drone_x += (
            FORWARD_SPEED * TIME_STEP
        )


        # Move toward center line

        if drone_y > CENTER_Y:

            drone_y -= (
                RETURN_SPEED * TIME_STEP
            )

        elif drone_y < CENTER_Y:

            drone_y += (
                RETURN_SPEED * TIME_STEP
            )


        # Check center

        if abs(drone_y - CENTER_Y) <= 0.05:

            drone_y = CENTER_Y

            # Move to next obstacle

            current_obstacle_index += 1

            obstacle_passed = False

            mode = "FORWARD"

            print()
            print(
                "Returned to center path."
            )

            print(
                f"Next obstacle = "
                f"{current_obstacle_index + 1}"
            )


    # ========================================================
    # UPDATE DRONE
    # ========================================================

    p.resetBasePositionAndOrientation(
        drone_id,
        [
            drone_x,
            drone_y,
            drone_z
        ],
        [
            0,
            0,
            0,
            1
        ]
    )


    # ========================================================
    # DRAW FLIGHT PATH
    # ========================================================

    p.addUserDebugLine(
        [
            drone_x,
            drone_y,
            0.05
        ],
        [
            drone_x,
            drone_y,
            1.0
        ],
        lineWidth=3,
        lifeTime=0.2
    )


    # ========================================================
    # PRINT STATUS
    # ========================================================

    if current_time - last_print_time >= 0.5:

        last_print_time = current_time

        if current_obstacle is not None:

            print(
                f"Time={current_time:5.1f}s | "
                f"X={drone_x:5.2f} | "
                f"Y={drone_y:5.2f} | "
                f"Distance={distance:5.2f} | "
                f"Mode={mode}"
            )

        else:

            print(
                f"Time={current_time:5.1f}s | "
                f"X={drone_x:5.2f} | "
                f"Y={drone_y:5.2f} | "
                f"Mode={mode}"
            )


    # ========================================================
    # STEP SIMULATION
    # ========================================================

    p.stepSimulation()

    time.sleep(TIME_STEP)


    # ========================================================
    # FINISH
    # ========================================================

    if drone_x >= TARGET_X:

        print()
        print("==============================================")
        print("       ALL 3 OBSTACLES AVOIDED")
        print("==============================================")
        print(
            f"Final X = {drone_x:.2f} m"
        )
        print(
            f"Final Y = {drone_y:.2f} m"
        )
        print(
            "Obstacles completed = "
            f"{current_obstacle_index}"
        )
        print("==============================================")

        break


# ============================================================
# KEEP GUI OPEN
# ============================================================

if p.isConnected(client):

    print()
    print("Simulation completed successfully.")
    print("Close the PyBullet window when finished.")

    while p.isConnected(client):

        p.stepSimulation()

        time.sleep(TIME_STEP)


# ============================================================
# DISCONNECT
# ============================================================

if p.isConnected(client):

    p.disconnect(client)

print("PyBullet connection closed.")