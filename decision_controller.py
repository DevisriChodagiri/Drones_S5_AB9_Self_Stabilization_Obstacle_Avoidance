class DecisionController:

    def decide(
        self,
        risk,
        distance,
        closing_speed,
        ttc
    ):

        # -------------------------------------------------
        # SAFETY OVERRIDE 1
        # Very small distance always means DANGER.
        # -------------------------------------------------

        if distance <= 0.8:

            return "AVOID"


        # -------------------------------------------------
        # SAFETY OVERRIDE 2
        # Very small TTC means DANGER.
        # -------------------------------------------------

        if ttc <= 2.0:

            return "AVOID"


        # -------------------------------------------------
        # ML WARNING
        # -------------------------------------------------

        if risk == "DANGER":

            return "AVOID"


        if risk == "WARNING":

            return "SLOW_DOWN"


        # -------------------------------------------------
        # SAFE CONDITION
        # -------------------------------------------------

        if risk == "SAFE":

            return "CONTINUE"


        # -------------------------------------------------
        # UNKNOWN CONDITION
        # -------------------------------------------------

        return "STOP"