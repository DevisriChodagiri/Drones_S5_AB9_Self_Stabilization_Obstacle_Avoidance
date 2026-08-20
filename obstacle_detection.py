def detect_obstacle(state):

    print()
    print("=" * 60)
    print("SCENARIO 3: ULTRASONIC OBSTACLE DETECTION")
    print("=" * 60)

    obstacle_x = state["obstacle_x"]

    distance = obstacle_x - state["x"]

    print()
    print(f"Drone X       : {state['x']:.2f} m")
    print(f"Obstacle X    : {obstacle_x:.2f} m")
    print(f"Distance      : {distance:.2f} m")

    if distance <= 1.5:

        print()
        print("⚠ OBSTACLE DETECTED")
        print("Ultrasonic sensor: OBSTACLE")
        print("Action: BRAKE")

        state["speed"] = 0.0
        state["mode"] = "BRAKE"

        return True

    print()
    print("Path clear.")

    return False