class ObstacleAvoidance:

    def __init__(
        self,
        safe_distance=1.5,
        danger_distance=0.8,
        warning_ttc=5.0,
        danger_ttc=2.0
    ):

        self.safe_distance = safe_distance
        self.danger_distance = danger_distance

        self.warning_ttc = warning_ttc
        self.danger_ttc = danger_ttc

    def decide_action(
        self,
        distance,
        closing_speed,
        ttc
    ):

        # -----------------------------------------
        # 1. IMMEDIATE DANGER
        # -----------------------------------------

        if distance <= self.danger_distance:

            return "AVOID"

        # -----------------------------------------
        # 2. VERY LOW TTC
        # -----------------------------------------

        if ttc <= self.danger_ttc:

            return "AVOID"

        # -----------------------------------------
        # 3. WARNING CONDITION
        # -----------------------------------------

        if ttc <= self.warning_ttc:

            return "SLOW_DOWN"

        # -----------------------------------------
        # 4. HIGH CLOSING SPEED
        # -----------------------------------------

        if closing_speed >= 1.5:

            return "SLOW_DOWN"

        # -----------------------------------------
        # 5. SAFE
        # -----------------------------------------

        return "CONTINUE"