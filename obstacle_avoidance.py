import time


def run_avoidance(state):

    print()
    print("=" * 60)
    print("SCENARIO 4: OBSTACLE AVOIDANCE")
    print("=" * 60)

    state["mode"] = "AVOID"

    original_y = state["y"]

    # Move sideways around obstacle.

    target_y = -1.0

    print()
    print(f"Moving sideways from Y={original_y:.2f} m")
    print(f"Avoidance target Y={target_y:.2f} m")

    while state["y"] > target_y:

        state["y"] -= 0.25

        state["speed"] = 0.25

        state["roll"] = -2.0
        state["pitch"] = 0.0
        state["yaw"] = 0.0

        print(
            f"Avoiding | "
            f"X={state['x']:.2f} m | "
            f"Y={state['y']:.2f} m | "
            f"Roll={state['roll']:+.2f}°"
        )

        time.sleep(0.3)

    print()
    print("Obstacle bypass path established.")

    # Pass the obstacle.

    state["x"] = 5.8

    state["speed"] = 0.4

    print(
        f"Passed obstacle | "
        f"X={state['x']:.2f} m"
    )

    # Return toward center.

    while state["y"] < 0.0:

        state["y"] += 0.25

        print(
            f"Returning to center | "
            f"Y={state['y']:.2f} m"
        )

        time.sleep(0.2)

    state["y"] = 0.0
    state["speed"] = 0.0
    state["roll"] = 0.0
    state["pitch"] = 0.0

    print()
    print("✓ OBSTACLE AVOIDED")