# AUTONOMOUS SELF-STABILIZING DRONE WITH OBSTACLE AVOIDANCE

<p align="center">
  <img src="./results/amrita_logo.png" alt="Amrita Vishwa Vidyapeetham Logo" width="200">
</p>

<h3 align="center">
AMRITA VISHWA VIDYAPEETHAM<br>
Coimbatore, Tamil Nadu<br>
Department of Computer Science and Engineering
</h3>

---

# PROJECT REPORT

## Project Title

# Autonomous Self-Stabilizing Drone with Obstacle Avoidance

---

## Team Details

| S.No. | Name | Roll Number | Email |
|---|---|---|---|
| 1 | Devisri | CB.SC.U4AIE24163 | **[ADD EMAIL]** |
| 2 | Monisha | CB.SC.U4AIE24157 | **[ADD EMAIL]** |
| 3 | Myagi | CB.SC.U4AIE24143 | **[ADD EMAIL]** |

**Team Number:** 2

---

# 1. Abstract

Autonomous drones require reliable stabilization, environmental sensing, obstacle detection, and safety mechanisms to operate effectively in dynamic environments. A drone that experiences excessive roll or pitch deviation may become unstable and potentially collide with obstacles or lose control.

This project presents an autonomous self-stabilizing drone system that integrates PID-based attitude stabilization, ultrasonic obstacle detection, obstacle avoidance, Machine Learning-based flight safety prediction, high-attitude detection, and an automatic recovery controller.

The drone's orientation is monitored using roll and pitch measurements obtained from an IMU-based sensing system. A PID controller is used to minimize the error between the desired and current attitude and maintain stable flight. An ultrasonic sensor is used to determine the distance between the drone and nearby obstacles.

A Logistic Regression model is incorporated as a Machine Learning-based safety classifier. The model uses distance, speed, roll, and pitch as input features and predicts whether the current flight condition is SAFE or UNSAFE. When excessive attitude deviation is detected, a recovery controller is activated to gradually bring the drone toward a stable orientation.

The complete system was developed and evaluated using MATLAB/Simulink and Python-based Machine Learning components. The results demonstrate the working of stabilization, safety classification, high-attitude detection, recovery, obstacle avoidance, and return-to-forward-flight mechanisms.

---

# 2. Introduction

Unmanned Aerial Vehicles (UAVs), commonly known as drones, are increasingly being used in applications such as surveillance, agriculture, infrastructure inspection, delivery, disaster management, mapping, and autonomous navigation.

For autonomous operation, a drone must continuously maintain its orientation while responding to changes in its environment. Two major challenges in autonomous drone operation are maintaining flight stability and avoiding obstacles.

Drone stability is commonly described using attitude parameters such as roll, pitch, and yaw. In this project, roll and pitch are primarily considered for attitude monitoring and stabilization.

A drone can become unstable when its current attitude deviates significantly from its desired attitude. A control mechanism is therefore required to continuously calculate the error and apply corrective action.

PID controllers are widely used for such control applications because they respond to current error, accumulated error, and rate of change of error [2].

In addition to stabilization, autonomous drones must be capable of detecting obstacles in their flight path. Distance measurements obtained from an ultrasonic sensor can be used to determine whether an obstacle is sufficiently close to require avoidance.

Machine Learning can further enhance autonomous safety by learning patterns associated with safe and unsafe flight conditions. In this project, Logistic Regression is used as a binary classifier for predicting the safety condition of the drone.

The proposed system therefore combines classical control, sensor-based perception, Machine Learning, and recovery mechanisms into a single autonomous drone framework.

---

# 3. Problem Statement

An autonomous drone must maintain stable flight while navigating through an environment containing potential obstacles.

Sudden changes in orientation may result in unsafe flight conditions, while obstacles in the drone's path may cause collisions.

Therefore, this project aims to develop a drone control system capable of:

- Maintaining stable roll and pitch.
- Detecting unstable or high-attitude conditions.
- Predicting whether a flight condition is SAFE or UNSAFE.
- Detecting obstacles.
- Avoiding detected obstacles.
- Recovering automatically from unstable attitudes.
- Returning safely to forward flight.

---

# 4. Objectives

The main objectives of this project are:

1. To implement PID-based stabilization for drone attitude control.
2. To monitor the roll and pitch of the drone.
3. To detect high-attitude and unstable conditions.
4. To develop a Machine Learning model for flight safety prediction.
5. To classify flight conditions as SAFE or UNSAFE.
6. To detect obstacles using ultrasonic distance measurements.
7. To implement an obstacle avoidance mechanism.
8. To implement an automatic recovery controller.
9. To return the drone to forward flight after obstacle avoidance.
10. To evaluate the complete system using simulation and experimental results.

---

# 5. Background and Related Work

## 5.1 Autonomous Drone Control

Autonomous drone systems require multiple control layers to maintain stable flight and perform navigation tasks.

Control systems are responsible for maintaining the drone's desired attitude, while perception systems provide information about the surrounding environment.

Research in UAV control has investigated PID controllers, model-based control, adaptive control, and intelligent control approaches.

The base paper selected for this project is provided in the References section.

**Base Paper: [ADD BASE PAPER HERE]**

---

## 5.2 PID-Based Stabilization

PID control is a commonly used approach for maintaining the desired attitude of a dynamic system.

The controller uses three components:

- Proportional control
- Integral control
- Derivative control

The combination allows the controller to respond to present error, accumulated error, and changes in error.

---

## 5.3 Machine Learning for Safety Prediction

Machine Learning can be used to identify patterns in flight data and classify different operating conditions.

In this project, Logistic Regression is used because the problem is formulated as a binary classification task:

```text
SAFE
UNSAFE
