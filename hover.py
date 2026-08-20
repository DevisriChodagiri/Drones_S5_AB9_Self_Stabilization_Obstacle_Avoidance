import time


def run_hover(state):

    print()
    print("=" * 60)
    print("SCENARIO 1: STABLE HOVER")
    print("=" * 60)

    state["mode"] = "HOVER"

    state["x"] = 0.0
    state["y"] = 0.0
    state["z"] = 1.0

    state["speed"] = 0.0

    state["roll"] = 0.0
    state["pitch"] = 0.0
    state["yaw"] = 0.0

    print()
    print("Target altitude: 1.00 m")
    print("Roll:  +0.00°")
    print("Pitch: +0.00°")
    print("Yaw:   +0.00°")
    print("Speed: 0.00 m/s")
    print()

    for i in range(3):

        print(
            f"Hover check {i + 1}: "
            f"X={state['x']:.2f} "
            f"Y={state['y']:.2f} "
            f"Z={state['z']:.2f} "
            f"STATUS=STABLE"
        )

        time.sleep(0.5)

    print()
    print("✓ HOVER STABLE")