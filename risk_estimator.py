class RiskEstimator:

    def __init__(
        self,
        warning_ttc=5.0,
        danger_ttc=2.0,
        danger_distance=0.8
    ):

        # -----------------------------------------
        # RISK THRESHOLDS
        # -----------------------------------------

        self.warning_ttc = warning_ttc
        self.danger_ttc = danger_ttc
        self.danger_distance = danger_distance

    def calculate_risk(
        self,
        distance,
        closing_speed,
        ttc
    ):

        # -----------------------------------------
        # 1. IMMEDIATE DANGER
        # -----------------------------------------

        if distance <= self.danger_distance:

            return "DANGER"

        # -----------------------------------------
        # 2. VERY LOW TTC
        # -----------------------------------------

        if ttc <= self.danger_ttc:

            return "DANGER"

        # -----------------------------------------
        # 3. WARNING TTC
        # -----------------------------------------

        if ttc <= self.warning_ttc:

            return "WARNING"

        # -----------------------------------------
        # 4. HIGH CLOSING SPEED
        # -----------------------------------------

        if closing_speed >= 1.5:

            return "WARNING"

        # -----------------------------------------
        # 5. OTHERWISE SAFE
        # -----------------------------------------

        return "SAFE"