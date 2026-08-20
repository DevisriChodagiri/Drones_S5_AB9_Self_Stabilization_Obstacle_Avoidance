import time


def run_recovery(state):

    print()
    print("=" * 60)
    print("SCENARIO 6: PID RECOVERY")
    print("=" * 60)

    state["mode"] = "RECOVER"

    print()
    print("Recovery controller activated.")
    print("Stabilizing roll and pitch...")

    # --------------------------------------------------------
    # PID-STYLE ATTITUDE RECOVERY
    # Gradually reduce roll and pitch toward zero.
    # --------------------------------------------------------

    recovery_step = 3.0

    while (
        abs(state["roll"]) > 0.0
        or abs(state["pitch"]) > 0.0
    ):

        # -----------------------------
        # Roll correction
        # -----------------------------

        if state["roll"] > 0:
            state["roll"] -= recovery_step

        elif state["roll"] < 0:
            state["roll"] += recovery_step

        # -----------------------------
        # Pitch correction
        # -----------------------------

        if state["pitch"] > 0:
            state["pitch"] -= recovery_step

        elif state["pitch"] < 0:
            state["pitch"] += recovery_step

        # -----------------------------
        # Prevent crossing zero
        # -----------------------------

        if abs(state["roll"]) < recovery_step:
            state["roll"] = 0.0

        if abs(state["pitch"]) < recovery_step:
            state["pitch"] = 0.0

        print(
            f"Recovery | "
            f"Roll={state['roll']:+.2f} deg | "
            f"Pitch={state['pitch']:+.2f} deg"
        )

        time.sleep(0.2)

    # --------------------------------------------------------
    # FINAL STABILIZATION
    # --------------------------------------------------------

    state["roll"] = 0.0
    state["pitch"] = 0.0
    state["yaw"] = 0.0

    state["speed"] = 0.0

    state["mode"] = "STABLE"

    print()
    print("Attitude stabilized.")
    print(
        f"Roll  = {state['roll']:+.2f} deg"
    )
    print(
        f"Pitch = {state['pitch']:+.2f} deg"
    )
    print(
        f"Yaw   = {state['yaw']:+.2f} deg"
    )

    print()
    print("[OK] PID RECOVERY SUCCESSFUL")