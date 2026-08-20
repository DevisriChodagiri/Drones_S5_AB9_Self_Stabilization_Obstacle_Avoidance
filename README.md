# Autonomous Self-Stabilizing Drone with Obstacle Avoidance

## 📌 Project Overview

This project focuses on developing an autonomous drone control system capable of maintaining stable flight, detecting obstacles, avoiding them, and safely returning to forward flight.

The system combines PID-based flight stabilization, sensor-based monitoring, Machine Learning-based safety prediction, automatic recovery, and obstacle avoidance.

---

## 🎯 Objectives

1. Maintain stable drone flight using PID control.
2. Monitor the drone's roll and pitch angles.
3. Detect obstacles using an ultrasonic sensor.
4. Predict whether the current flight condition is safe or unsafe using Machine Learning.
5. Automatically recover the drone when it becomes unstable.
6. Avoid detected obstacles and safely return to forward flight.

---

## 🧠 System Architecture

```text
                  ┌──────────────────────┐
                  │     Drone Model      │
                  └──────────┬───────────┘
                             │
                  ┌──────────▼───────────┐
                  │    Sensor Inputs     │
                  │                      │
                  │  MPU6050 / IMU       │
                  │  Ultrasonic Sensor   │
                  └──────────┬───────────┘
                             │
                  ┌──────────▼───────────┐
                  │  Flight Monitoring   │
                  │                      │
                  │ Roll / Pitch         │
                  │ Distance / Speed     │
                  └──────────┬───────────┘
                             │
                  ┌──────────▼───────────┐
                  │  Machine Learning    │
                  │ Logistic Regression  │
                  └──────────┬───────────┘
                             │
                  ┌──────────▼───────────┐
                  │   Decision Making    │
                  └───────┬───────┬──────┘
                          │       │
                       SAFE     UNSAFE
                          │       │
                          │   ┌───▼────────────┐
                          │   │ Recovery       │
                          │   │ Controller     │
                          │   └────────────────┘
                          │
                  ┌───────▼───────────┐
                  │  Obstacle Check   │
                  └────────┬──────────┘
                           │
                    Obstacle Detected
                           │
                  ┌────────▼──────────┐
                  │ Obstacle Avoidance│
                  │    Controller     │
                  └────────┬──────────┘
                           │
                  ┌────────▼──────────┐
                  │ Return to Forward │
                  │      Flight       │
                  └───────────────────┘
