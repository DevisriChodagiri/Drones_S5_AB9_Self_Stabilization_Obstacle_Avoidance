import pandas as pd
from sklearn.linear_model import LogisticRegression


# Load dataset
data = pd.read_csv("dataset.csv")


# Features
X = data[["Distance", "Speed", "Roll", "Pitch"]]


# Target
y = data["Safe"]


# Train Logistic Regression
model = LogisticRegression()

model.fit(X, y)


# ============================================================
# PREDICTION FUNCTION
# ============================================================

def predict_safety(distance, speed, roll, pitch):

    features = pd.DataFrame(
        [[distance, speed, roll, pitch]],
        columns=["Distance", "Speed", "Roll", "Pitch"]
    )

    prediction = model.predict(features)[0]

    probability = model.predict_proba(features)[0]

    return prediction, probability


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    distance = 50
    speed = 5
    roll = 5
    pitch = 6

    prediction, probability = predict_safety(
        distance,
        speed,
        roll,
        pitch
    )

    print("Distance :", distance)
    print("Speed    :", speed)
    print("Roll     :", roll)
    print("Pitch    :", pitch)

    print()

    print("Prediction:", prediction)

    if prediction == 1:
        print("RESULT: SAFE")
    else:
        print("RESULT: UNSAFE")

    print("Probability:", probability)