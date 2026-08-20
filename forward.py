import time


def run_forward(state):

    print()
    print("=" * 60)
    print("SCENARIO 2: SLOW FORWARD FLIGHT")
    print("=" * 60)

    state["mode"] = "FORWARD"

    forward_speed = 0.5

    # Move toward the obstacle,
    # but stop before reaching it.

    while state["x"] < 4.0:

        state["x"] += 0.5

        state["speed"] = forward_speed

        state["roll"] = 0.0
        state["pitch"] = 2.0
        state["yaw"] = 0.0

        print(
            f"Forward flight | "
            f"X={state['x']:.2f} m | "
            f"Y={state['y']:.2f} m | "
            f"Z={state['z']:.2f} m | "
            f"Speed={state['speed']:.2f} m/s"
        )

        time.sleep(0.3)

    print()
    print("✓ FORWARD FLIGHT STABLE")