import pickle
import os
import pandas as pd


def main():

    print("Starting ML risk prediction...")

    # ------------------------------------------------
    # 1. LOAD TRAINED MODEL
    # ------------------------------------------------

    model_path = os.path.join(
        "results",
        "risk_model.pkl"
    )

    with open(
        model_path,
        "rb"
    ) as file:

        model = pickle.load(file)

    # ------------------------------------------------
    # 2. LOAD SCALER
    # ------------------------------------------------

    scaler_path = os.path.join(
        "results",
        "scaler.pkl"
    )

    with open(
        scaler_path,
        "rb"
    ) as file:

        scaler = pickle.load(file)

    print("Model loaded successfully.")
    print("Scaler loaded successfully.")

    # ------------------------------------------------
    # 3. NEW DRONE SENSOR VALUES
    # ------------------------------------------------

    distance = 1.0
    closing_speed = 1.5
    ttc = distance / closing_speed
    roll = 5.0
    pitch = 4.0

    # ------------------------------------------------
    # 4. CREATE INPUT
    # ------------------------------------------------

    
    input_data = pd.DataFrame(
    [[
        distance,
        closing_speed,
        ttc,
        roll,
        pitch
    ]],
    columns=[
        "Distance",
        "ClosingSpeed",
        "TTC",
        "Roll",
        "Pitch"
    ]
    )

    # ------------------------------------------------
    # 5. SCALE INPUT
    # ------------------------------------------------

    input_scaled = scaler.transform(
        input_data
    )

    # ------------------------------------------------
    # 6. PREDICT RISK
    # ------------------------------------------------

    prediction = model.predict(
        input_scaled
    )

    # ------------------------------------------------
    # 7. GET PROBABILITIES
    # ------------------------------------------------

    probabilities = model.predict_proba(
        input_scaled
    )

    # ------------------------------------------------
    # 8. DISPLAY INPUT
    # ------------------------------------------------

    print("\nDrone Flight Conditions:")
    print(
        "Distance:",
        distance,
        "m"
    )

    print(
        "Closing Speed:",
        closing_speed,
        "m/s"
    )

    print(
        "TTC:",
        round(ttc, 2),
        "seconds"
    )

    print(
        "Roll:",
        roll,
        "degrees"
    )

    print(
        "Pitch:",
        pitch,
        "degrees"
    )

    # ------------------------------------------------
    # 9. DISPLAY PREDICTION
    # ------------------------------------------------

    print(
        "\nPredicted Risk:",
        prediction[0]
    )

    # ------------------------------------------------
    # 10. DISPLAY PROBABILITIES
    # ------------------------------------------------

    print("\nRisk Probabilities:")

    for class_name, probability in zip(
        model.classes_,
        probabilities[0]
    ):

        print(
            f"{class_name}: "
            f"{probability * 100:.2f}%"
        )

    print(
        "\nML risk prediction completed."
    )


if __name__ == "__main__":
    main()