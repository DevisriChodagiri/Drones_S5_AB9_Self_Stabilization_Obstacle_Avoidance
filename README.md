# Autonomous Self-Stabilizing Drone with Obstacle Avoidance

<!-- ========================================================= -->
<!--                     AMRITA LOGO                           -->
<!-- ========================================================= -->

<p align="center">
  <img src="results/amrita_logo.png" alt="Amrita Vishwa Vidyapeetham Logo" width="180">
</p>

<p align="center">
  <b>AMRITA VISHWA VIDYAPEETHAM</b><br>
  Coimbatore, Tamil Nadu<br>
  Department of Computer Science and Engineering
</p>

---

# Project Report

## Project Title

# Autonomous Self-Stabilizing Drone with Obstacle Avoidance

---

## Team Members

| S.No | Name | Roll Number | Email |
|------|------|-------------|-------|
| 1 | Devisri | CB.SC.U4AIE24163 | **[Add Email]** |
| 2 | Monisha | CB.SC.U4AIE24157 | **[Add Email]** |
| 3 | Myagi | CB.SC.U4AIE24143 | **[Add Email]** |

**Team Number:** 2

---

# Abstract

Autonomous drones require reliable flight stabilization, obstacle detection, and safety mechanisms to operate effectively in dynamic environments. An unstable drone can experience excessive roll or pitch angles, which may result in loss of control or collision with obstacles.

This project presents an autonomous self-stabilizing drone system that combines PID-based attitude stabilization, obstacle detection, obstacle avoidance, Machine Learning-based flight safety prediction, and an automatic recovery controller.

The drone's attitude is monitored using roll and pitch information obtained from an IMU-based sensing system. A PID controller is used to reduce the error between the desired and current orientation and maintain stable flight. An ultrasonic sensor is used to detect obstacles based on distance measurements.

In addition, a Logistic Regression Machine Learning model is used to classify the current flight condition as either SAFE or UNSAFE based on parameters such as distance, speed, roll, and pitch. When an unsafe attitude condition is detected, a recovery controller is activated to gradually bring the drone back toward a stable orientation.

The system was implemented and evaluated using MATLAB/Simulink and Python-based Machine Learning components. The experimental results demonstrate stabilization, safety classification, recovery from unstable conditions, obstacle avoidance, and return to forward flight.

---

# 1. Introduction

Unmanned Aerial Vehicles (UAVs), commonly known as drones, are increasingly used in surveillance, agriculture, delivery, inspection, disaster management, and autonomous navigation.

For autonomous operation, a drone must maintain its orientation while continuously responding to changes in its environment. Two important challenges are:

1. Maintaining stable flight.
2. Detecting and avoiding obstacles.

A drone may become unstable when its roll or pitch angle deviates significantly from the desired orientation. Without an appropriate stabilization mechanism, such deviations can lead to loss of control.

Similarly, when an obstacle appears in the drone's path, the drone must detect it and change its motion accordingly.

This project addresses these challenges by integrating multiple control and decision-making components into a single autonomous drone framework.

The proposed system consists of:

- IMU-based attitude monitoring
- PID stabilization
- Ultrasonic obstacle detection
- Obstacle avoidance
- Machine Learning-based safety classification
- High-attitude detection
- Automatic recovery control
- Return-to-forward-flight mechanism

---

# 2. Problem Statement

Autonomous drones must maintain stable flight while navigating through environments containing potential obstacles. Sudden changes in orientation or the presence of obstacles can cause unsafe flight conditions.

Therefore, the objective of this project is to develop a drone control framework that can:

- Maintain stable roll and pitch.
- Detect unsafe flight conditions.
- Predict whether the current condition is SAFE or UNSAFE.
- Detect obstacles.
- Avoid obstacles.
- Recover automatically from unstable attitudes.
- Resume forward flight after the obstacle is cleared.

---

# 3. Objectives

The main objectives of the project are:

1. To develop a PID-based drone stabilization system.
2. To monitor the roll and pitch angles of the drone.
3. To detect high-attitude and unstable flight conditions.
4. To develop a Machine Learning model for flight safety prediction.
5. To classify flight conditions as SAFE or UNSAFE.
6. To detect obstacles using distance measurements.
7. To implement an obstacle avoidance controller.
8. To develop an automatic recovery controller.
9. To safely return the drone to forward flight after recovery or obstacle avoidance.
10. To evaluate the complete system using simulation and experimental results.

---

# 4. Background

## 4.1 Drone Stability

Drone stability refers to the ability of the drone to maintain its desired orientation despite disturbances or changes in its motion.

The primary attitude parameters considered in this project are:

- Roll
- Pitch

The desired attitude is compared with the current attitude, and the resulting error is used by the PID controller to calculate the required correction.

---

## 4.2 Roll

Roll represents rotation around the longitudinal axis of the drone.

A positive or negative roll indicates that the drone is tilting toward one side.

---

## 4.3 Pitch

Pitch represents rotation around the lateral axis of the drone.

It indicates whether the drone is tilting forward or backward.

---

## 4.4 IMU

An Inertial Measurement Unit (IMU) provides information about the motion and orientation of the drone.

The project considers an MPU6050-based sensing system for obtaining attitude information.

The sensor contains:

- 3-axis accelerometer
- 3-axis gyroscope

Together, these measurements can be used to estimate the drone's orientation.

---

## 4.5 Ultrasonic Sensor

An ultrasonic sensor measures the distance between the drone and an obstacle.

The sensor emits an ultrasonic pulse and measures the time taken for the reflected signal to return.

The distance can be calculated as:

$$
d = \frac{v t}{2}
$$

where:

- $d$ = distance to obstacle
- $v$ = speed of sound
- $t$ = round-trip travel time

The division by 2 is required because the ultrasonic signal travels to the obstacle and back.

---

# 5. Proposed Methodology

The proposed system consists of several interconnected modules.

```text
                    ┌─────────────────────┐
                    │     Drone Model     │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │   Sensor System     │
                    │                     │
                    │ IMU + Ultrasonic    │
                    └──────────┬──────────┘
                               │
                ┌──────────────▼──────────────┐
                │     Flight Monitoring       │
                │                             │
                │ Distance / Speed / Roll     │
                │ Pitch                       │
                └──────────────┬──────────────┘
                               │
                 ┌─────────────▼─────────────┐
                 │    Safety Prediction      │
                 │                           │
                 │   Logistic Regression     │
                 └─────────────┬─────────────┘
                               │
                       ┌───────▼───────┐
                       │ Decision Unit │
                       └───┬───────┬───┘
                           │       │
                         SAFE    UNSAFE
                           │       │
                           │   ┌───▼──────────┐
                           │   │   Recovery   │
                           │   │  Controller  │
                           │   └──────────────┘
                           │
                  ┌────────▼────────┐
                  │ Obstacle Check  │
                  └────────┬────────┘
                           │
                    Obstacle detected
                           │
                  ┌────────▼────────┐
                  │ Obstacle        │
                  │ Avoidance       │
                  └────────┬────────┘
                           │
                  ┌────────▼────────┐
                  │ Return to       │
                  │ Forward Flight  │
                  └─────────────────┘
