import csv
import random
import os


def calculate_ttc(distance, closing_speed):

    if closing_speed > 0:
        return distance / closing_speed

    return float("inf")


def determine_risk(distance, closing_speed, ttc, roll, pitch):

    # -------------------------------
    # DANGER CONDITIONS
    # -------------------------------

    if distance <= 0.8:
        return "DANGER"

    if ttc <= 2.0:
        return "DANGER"

    if abs(roll) >= 25 or abs(pitch) >= 25:
        return "DANGER"

    # -------------------------------
    # WARNING CONDITIONS
    # -------------------------------

    if ttc <= 5.0:
        return "WARNING"

    if closing_speed >= 1.5:
        return "WARNING"

    if abs(roll) >= 15 or abs(pitch) >= 15:
        return "WARNING"

    # -------------------------------
    # SAFE
    # -------------------------------

    return "SAFE"


def generate_safe_sample():

    distance = random.uniform(4.0, 6.0)

    closing_speed = random.uniform(
        0.1,
        0.6
    )

    roll = random.uniform(
        -10.0,
        10.0
    )

    pitch = random.uniform(
        -10.0,
        10.0
    )

    ttc = calculate_ttc(
        distance,
        closing_speed
    )

    risk = determine_risk(
        distance,
        closing_speed,
        ttc,
        roll,
        pitch
    )

    return [
        distance,
        closing_speed,
        ttc,
        roll,
        pitch,
        risk
    ]


def generate_warning_sample():

    distance = random.uniform(
        2.0,
        4.5
    )

    closing_speed = random.uniform(
        0.6,
        1.4
    )

    roll = random.uniform(
        -14.0,
        14.0
    )

    pitch = random.uniform(
        -14.0,
        14.0
    )

    ttc = calculate_ttc(
        distance,
        closing_speed
    )

    risk = determine_risk(
        distance,
        closing_speed,
        ttc,
        roll,
        pitch
    )

    return [
        distance,
        closing_speed,
        ttc,
        roll,
        pitch,
        risk
    ]


def generate_danger_sample():

    distance = random.uniform(
        0.5,
        2.5
    )

    closing_speed = random.uniform(
        1.0,
        2.5
    )

    roll = random.uniform(
        -20.0,
        20.0
    )

    pitch = random.uniform(
        -20.0,
        20.0
    )

    ttc = calculate_ttc(
        distance,
        closing_speed
    )

    risk = determine_risk(
        distance,
        closing_speed,
        ttc,
        roll,
        pitch
    )

    return [
        distance,
        closing_speed,
        ttc,
        roll,
        pitch,
        risk
    ]


def generate_dataset(samples_per_class):

    dataset = []

    # -------------------------------
    # SAFE SAMPLES
    # -------------------------------

    while len([
        row for row in dataset
        if row[5] == "SAFE"
    ]) < samples_per_class:

        sample = generate_safe_sample()

        if sample[5] == "SAFE":
            dataset.append(sample)

    # -------------------------------
    # WARNING SAMPLES
    # -------------------------------

    while len([
        row for row in dataset
        if row[5] == "WARNING"
    ]) < samples_per_class:

        sample = generate_warning_sample()

        if sample[5] == "WARNING":
            dataset.append(sample)

    # -------------------------------
    # DANGER SAMPLES
    # -------------------------------

    while len([
        row for row in dataset
        if row[5] == "DANGER"
    ]) < samples_per_class:

        sample = generate_danger_sample()

        if sample[5] == "DANGER":
            dataset.append(sample)

    # Shuffle samples
    random.shuffle(dataset)

    return dataset


def save_dataset(dataset, filename):

    directory = os.path.dirname(filename)

    if directory:
        os.makedirs(
            directory,
            exist_ok=True
        )

    with open(
        filename,
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Distance",
            "ClosingSpeed",
            "TTC",
            "Roll",
            "Pitch",
            "Risk"
        ])

        for row in dataset:

            writer.writerow([
                f"{row[0]:.4f}",
                f"{row[1]:.4f}",
                f"{row[2]:.4f}",
                f"{row[3]:.4f}",
                f"{row[4]:.4f}",
                row[5]
            ])


def main():

    print(
        "Starting balanced ML dataset generation..."
    )

    samples_per_class = 500

    dataset = generate_dataset(
        samples_per_class
    )

    filename = os.path.join(
        "data",
        "flight_data.csv"
    )

    save_dataset(
        dataset,
        filename
    )

    print(
        "\nDataset generation completed."
    )

    print(
        "Total samples:",
        len(dataset)
    )

    print(
        "Samples per class:",
        samples_per_class
    )

    print(
        "Saved file:",
        filename
    )


if __name__ == "__main__":
    main()