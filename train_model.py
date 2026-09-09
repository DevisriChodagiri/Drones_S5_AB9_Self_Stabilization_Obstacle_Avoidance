import pandas as pd
import os
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


def main():

    print("Starting ML model training...")

    # ------------------------------------------------
    # 1. LOAD DATASET
    # ------------------------------------------------

    dataset_path = os.path.join(
        "data",
        "flight_data.csv"
    )

    data = pd.read_csv(dataset_path)

    print("\nDataset loaded successfully.")
    print("Total samples:", len(data))

    # ------------------------------------------------
    # 2. SELECT INPUT FEATURES
    # ------------------------------------------------

    features = [
        "Distance",
        "ClosingSpeed",
        "TTC",
        "Roll",
        "Pitch"
    ]

    X = data[features]

    # ------------------------------------------------
    # 3. SELECT TARGET
    # ------------------------------------------------

    y = data["Risk"]

    # ------------------------------------------------
    # 4. SPLIT DATA
    # ------------------------------------------------

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    print("\nTraining samples:", len(X_train))
    print("Testing samples:", len(X_test))

    # ------------------------------------------------
    # 5. FEATURE SCALING
    # ------------------------------------------------

    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(
        X_train
    )

    X_test_scaled = scaler.transform(
        X_test
    )

    # ------------------------------------------------
    # 6. CREATE LOGISTIC REGRESSION MODEL
    # ------------------------------------------------

    model = LogisticRegression(
        max_iter=1000
    )

    # ------------------------------------------------
    # 7. TRAIN MODEL
    # ------------------------------------------------

    model.fit(
        X_train_scaled,
        y_train
    )

    print("\nModel training completed.")

    # ------------------------------------------------
    # 8. PREDICT TEST DATA
    # ------------------------------------------------

    predictions = model.predict(
        X_test_scaled
    )

    # ------------------------------------------------
    # 9. CALCULATE ACCURACY
    # ------------------------------------------------

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    print(
        "\nModel Accuracy:",
        round(accuracy * 100, 2),
        "%"
    )

    # ------------------------------------------------
    # 10. CLASSIFICATION REPORT
    # ------------------------------------------------

    print("\nClassification Report:")

    print(
        classification_report(
            y_test,
            predictions
        )
    )

    # ------------------------------------------------
    # 11. CREATE RESULTS DIRECTORY
    # ------------------------------------------------

    results_directory = "results"

    os.makedirs(
        results_directory,
        exist_ok=True
    )

    # ------------------------------------------------
    # 12. SAVE TRAINED MODEL
    # ------------------------------------------------

    model_path = os.path.join(
        results_directory,
        "risk_model.pkl"
    )

    with open(
        model_path,
        "wb"
    ) as file:

        pickle.dump(
            model,
            file
        )

    # ------------------------------------------------
    # 13. SAVE SCALER
    # ------------------------------------------------

    scaler_path = os.path.join(
        results_directory,
        "scaler.pkl"
    )

    with open(
        scaler_path,
        "wb"
    ) as file:

        pickle.dump(
            scaler,
            file
        )

    print("\nTrained model saved:")
    print(model_path)

    print("\nScaler saved:")
    print(scaler_path)

    print("\nML training and saving completed successfully.")


if __name__ == "__main__":
    main()