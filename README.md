# Autonomous Self-Stabilizing Drone with Obstacle Avoidance

## Amrita Logo

<p align="center">
  <img src="amrita_logo.png" width="200">
</p>

---

## Team Members

| Name | Roll No. | Email |
|---|---|---|
| Devisri Chodagiri | YOUR_ROLL_NO | devisri7142@gmail.com |
| Team Member 2 | ROLL_NO | EMAIL |
| Team Member 3 | ROLL_NO | EMAIL |

---

# Title

## Autonomous Self-Stabilizing Drone with Obstacle Avoidance

---

# Abstract

This project presents an autonomous drone control system that focuses on **self-stabilization, obstacle avoidance, instability detection, and safe/unsafe path prediction**.

The system uses simulated sensor data such as **Roll, Pitch, Speed, and Distance** to monitor the drone's condition. A **PID controller** is used to maintain stable flight by correcting attitude errors. An obstacle avoidance mechanism detects nearby obstacles and generates an appropriate avoidance response.

A **Logistic Regression machine learning model** is also used to classify the drone's current flight condition as **SAFE or UNSAFE** based on sensor parameters.

The complete system is implemented and tested using Python and MATLAB/Simulink-based simulation.

---

# 1. Introduction

Drones are increasingly used in applications such as surveillance, agriculture, delivery, disaster management, and aerial monitoring. For autonomous operation, a drone must be capable of maintaining stable flight and responding safely to obstacles and unstable conditions.

A drone can become unstable when its roll or pitch deviates significantly from the desired orientation. Similarly, an obstacle in the flight path can result in a collision if no corrective action is taken.

Therefore, this project combines:

- Drone attitude stabilization
- PID control
- Obstacle detection
- Obstacle avoidance
- High-attitude detection
- Recovery control
- Machine learning-based safety prediction

The objective is to develop a simulation-based autonomous drone system capable of maintaining stable and safer flight.

---

# 2. Objectives

The main objectives of the project are:

1. To simulate drone flight and sensor parameters.
2. To maintain drone stability using a PID controller.
3. To monitor Roll and Pitch values.
4. To detect high-attitude and unstable conditions.
5. To activate a recovery mechanism during instability.
6. To detect obstacles in the drone's path.
7. To perform obstacle avoidance.
8. To predict whether the current flight condition is SAFE or UNSAFE using Logistic Regression.
9. To record and analyze drone flight data.

---

# 3. Methodology

The proposed system consists of the following major components:

```text
Drone Simulation
       |
       v
Sensor Data
(Roll, Pitch, Speed, Distance)
       |
       +--------------------+
       |                    |
       v                    v
 PID Controller       Safety Prediction
       |              (Logistic Regression)
       v                    |
 Stability Control     SAFE / UNSAFE
       |
       v
Attitude Monitoring
       |
       +----------------------+
       |                      |
       v                      v
Stable Flight          High Attitude
                              |
                              v
                       Recovery Control

Distance Sensor
       |
       v
Obstacle Detection
       |
       v
Obstacle Avoidance
