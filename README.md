# AUTONOMOUS SELF-STABILIZING DRONE WITH OBSTACLE AVOIDANCE

<p align="center">
  <img src="./results/amrita_logo.png" alt=""C:\Users\DEVI SRI\OneDrive\Desktop\Downloads\logo-branding-amrita-universiy-2024.jpeg"" width="200">
</p>

<p align="center">
  <b>AMRITA VISHWA VIDYAPEETHAM</b><br>
  Coimbatore, Tamil Nadu<br>
  Department of Computer Science and Engineering
</p>

---

# TEAM MEMBER DETAILS

| S.No. | Name | Roll Number | Email |
|---|---|---|---|
| 1 | Devisri | CB.SC.U4AIE24163 | devisri7142@gmail.com |
| 2 | Monisha | CB.SC.U4AIE24157 | vemurimonishareddy@gmail.com |
| 3 | Myagi | CB.SC.U4AIE24143 | patimamyagi@gmail.com |

**Team Number:** AB14

---

# TITLE

## Autonomous Self-Stabilizing Drone with Obstacle Avoidance

---

# ABSTRACT

Autonomous drones require stability, environmental awareness, and safe decision-making to operate effectively without continuous human intervention. A drone may become unstable due to changes in its roll and pitch, while obstacles in its flight path can lead to collisions.

This project presents an **Autonomous Self-Stabilizing Drone with Obstacle Avoidance** that combines PID-based stabilization, Machine Learning-based safety prediction, high-attitude detection, automatic recovery, obstacle detection, and obstacle avoidance.

The drone continuously monitors important flight parameters such as **roll, pitch, speed, and distance from obstacles**. A PID controller is used to reduce the error between the desired and current attitude and maintain stable flight.

A **Logistic Regression** model is used as a Machine Learning safety layer. The model uses distance, speed, roll, and pitch as input features and predicts whether the current flight condition is **SAFE or UNSAFE**.

When the drone reaches an unsafe attitude condition, the high-attitude detection mechanism identifies the instability and activates a recovery controller. The recovery controller gradually reduces the attitude deviation and brings the drone back toward a stable state.

An ultrasonic distance measurement is used to detect obstacles in the drone's path. When an obstacle is detected, the drone enters obstacle avoidance mode. After the obstacle is cleared, the system returns the drone to forward flight.

The complete system is developed and evaluated using **MATLAB/Simulink** and **Python-based Machine Learning components**.

---

# INTRODUCTION

Drones are increasingly being used in surveillance, agriculture, inspection, delivery, mapping, disaster management, and autonomous navigation.

For autonomous operation, a drone must be able to maintain its orientation while also responding to its surroundings. Two important challenges in autonomous drone operation are **flight stabilization** and **obstacle avoidance**.

A drone may become unstable when its roll or pitch deviates significantly from the desired orientation. At the same time, obstacles in the flight path can cause collisions if they are not detected and avoided.

This project focuses on developing a drone system that combines **self-stabilization, safety prediction, instability detection, recovery, and obstacle avoidance**.

The major components of the proposed system are:

- **PID-based self-stabilization**
- **Roll and pitch monitoring**
- **Machine Learning-based safety prediction**
- **High-attitude / instability detection**
- **Automatic recovery controller**
- **Obstacle detection**
- **Obstacle avoidance**
- **Return to forward flight**

The system continuously monitors the drone's condition and responds according to the current flight situation. The objective is to make the drone more stable and capable of responding automatically to unsafe conditions and obstacles.

---

# METHODOLOGY

The proposed system consists of multiple modules that work together to provide autonomous and safe drone operation.

The major stages of the methodology are:

```text
                    DRONE
                      |
                      v
              SENSOR MONITORING
                      |
          +-----------+-----------+
          |                       |
      Roll / Pitch             Distance
          |                       |
          v                       v
   PID STABILIZATION       OBSTACLE DETECTION
          |
          v
   ML SAFETY PREDICTION
          |
      +---+---+
      |       |
    SAFE    UNSAFE
              |
              v
       HIGH-ATTITUDE
          DETECTION
              |
              v
          RECOVERY
              |
              v
       STABLE FLIGHT
              |
              v
      OBSTACLE AVOIDANCE
              |
              v
      FORWARD FLIGHT
