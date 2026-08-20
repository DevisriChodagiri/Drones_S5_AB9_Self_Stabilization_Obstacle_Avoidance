from ml_model import predict_safety


def check_unsafe(state):

    print()
    print("=" * 60)
    print("SCENARIO 5: MACHINE LEARNING SAFETY CHECK")
    print("=" * 60)

    # --------------------------------------------------------
    # After obstacle avoidance, the obstacle is behind the drone.
    # Therefore, the forward distance is considered SAFE.
    # --------------------------------------------------------

    obstacle_x = state["obstacle_x"]
    current_x = state["x"]

    if current_x >= obstacle_x:
        distance = 2.0
    else:
        distance = obstacle_x - current_x

    distance_cm = distance * 100.0

    speed = state["speed"]
    roll = state["roll"]
    pitch = state["pitch"]

    print()
    print(f"Distance : {distance_cm:.2f} cm")
    print(f"Speed    : {speed:.2f}")
    print(f"Roll     : {roll:.2f}")
    print(f"Pitch    : {pitch:.2f}")

    # --------------------------------------------------------
    # MACHINE LEARNING PREDICTION
    # --------------------------------------------------------

    try:

        prediction, probability = predict_safety(
            distance_cm,
            speed,
            roll,
            pitch
        )

        if prediction == 1:
            result = "SAFE"
        else:
            result = "UNSAFE"

        print()
        print(f"Prediction: {prediction}")
        print(f"RESULT: {result}")
        print(f"Probability: {probability}")

    except Exception as e:

        print()
        print("ML model error:")
        print(e)

        result = "SAFE"

    # --------------------------------------------------------
    # SCENARIO: ATTITUDE DISTURBANCE
    # --------------------------------------------------------

    print()
    print("Simulating attitude disturbance...")

    state["roll"] = 12.0
    state["pitch"] = 8.0

    print(
        f"Roll={state['roll']:+.2f}° | "
        f"Pitch={state['pitch']:+.2f}°"
    )

    # Physical safety threshold

    if (
        abs(state["roll"]) > 10.0
        or abs(state["pitch"]) > 10.0
    ):

        print("⚠ UNSAFE CONDITION DETECTED")
        print("Action: ENTER RECOVERY")

        state["mode"] = "UNSAFE"

        return True

    print("✓ ATTITUDE SAFE")

    return False