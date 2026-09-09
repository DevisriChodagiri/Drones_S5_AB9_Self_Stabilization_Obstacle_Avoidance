# Final Review Proposal (FRP)

## Project Title

**Autonomous Self-Stabilizing Drone with Intelligent Obstacle Avoidance**

---

## 1. Project Overview

The proposed project is an autonomous drone simulation system designed to maintain stable flight and intelligently avoid obstacles during navigation.

The system combines **drone stabilization, sensor-based obstacle detection, mathematical decision-making, and machine learning-based risk prediction**. The complete system will be developed and tested using **Python and PyBullet**.

The drone will continuously monitor its orientation and surrounding environment. A PID controller will be used for self-stabilization, while distance and motion information will be used to detect obstacles and estimate the risk of collision. A machine learning model will assist in classifying the current flight situation as safe, warning, or dangerous.

The final system will demonstrate autonomous navigation through different obstacle scenarios, including static and moving obstacles.

---

## 2. Problem Statement

A drone flying autonomously in an unknown environment must maintain its stability while simultaneously responding to obstacles.

Sudden disturbances or changes in the environment can cause changes in the drone's roll and pitch, while obstacles in its flight path can lead to collisions.

A system is therefore required that can:

* Maintain stable drone orientation.
* Detect obstacles before collision.
* Determine the level of collision risk.
* Slow down when an obstacle becomes a potential threat.
* Change its flight direction to avoid obstacles.
* Recover its original flight path after avoiding an obstacle.
* Handle different obstacle scenarios autonomously.

---

## 3. Proposed Solution

The proposed system will consist of multiple interacting modules.

### 3.1 Drone Simulation

The drone will be simulated in **PyBullet** using Python.

The simulation environment will contain:

* Drone model
* Ground/environment
* Obstacles
* Sensor information
* Flight trajectory
* Autonomous navigation logic

---

### 3.2 Self-Stabilization

The drone's orientation will be monitored using simulated IMU measurements.

The important attitude parameters are:

* Roll
* Pitch
* Yaw

PID control will be used to minimize the difference between the desired and actual orientation.

The PID error is:

$$
e(t) = r(t) - y(t)
$$

where:

* \(r(t)\) = desired orientation
* \(y(t)\) = actual orientation

The PID controller consists of:

$$
P = K_p e(t)
$$

$$
I = K_i \sum e(t)\Delta t
$$

$$
D = K_d\frac{e(t)-e(t-1)}{\Delta t}
$$

The final control signal is:

$$
u(t)=P+I+D
$$

The control signal will be converted into appropriate motor thrust corrections.

---

## 4. Obstacle Detection

The drone will obtain the distance between itself and obstacles using simulated distance sensing.

The Euclidean distance will be calculated as:

$$
D = \sqrt{
(x_o-x_d)^2 +
(y_o-y_d)^2 +
(z_o-z_d)^2
}
$$

where:

* \(x_d,y_d,z_d\) = drone position
* \(x_o,y_o,z_o\) = obstacle position

The measured distance will be continuously monitored during flight.

---

## 5. Collision Risk Estimation

The system will not depend only on the current distance.

It will also consider how quickly the drone is approaching an obstacle.

The approximate closing speed is:

$$
V_{relative} =
\frac{D_{previous}-D_{current}}{\Delta t}
$$

Time-to-collision (TTC) will then be estimated as:

$$
TTC =
\frac{D}{V_{relative}}
$$

when the closing speed is positive.

A smaller TTC indicates a higher collision risk.

The system will classify the situation into:

* **SAFE**
* **WARNING**
* **DANGER**

---

## 6. Intelligent Decision Making

Based on distance, closing speed, TTC, drone attitude, and predicted risk, the navigation system will select an appropriate action.

The proposed actions are:

| Situation                 | Action    |
| ------------------------- | --------- |
| Safe environment          | CONTINUE  |
| Increasing collision risk | SLOW DOWN |
| High collision risk       | AVOID     |
| Obstacle cleared          | RETURN    |
| Unstable flight condition | RECOVER   |

The drone will therefore not follow a completely fixed path. Its movement will change according to the sensed environment.

---

## 7. Machine Learning Component

A machine learning model will be trained to predict the risk level of the drone's current flight condition.

Possible input features include:

* Distance
* Closing speed
* Time-to-collision
* Roll
* Pitch

The model will classify the current condition into:

```text
SAFE
WARNING
DANGER
```

The predicted risk will be supplied to the navigation decision layer.

The machine learning component will therefore act as an additional intelligence layer rather than directly controlling the motors.

---

## 8. Obstacle Avoidance

The drone will be tested using multiple obstacles arranged in different configurations.

The initial visual simulation will include **three obstacles arranged in a zig-zag pattern**.

The drone will:

1. Move forward.
2. Detect the first obstacle.
3. Reduce its speed.
4. Move sideways to avoid it.
5. Pass the obstacle.
6. Return toward the original flight path.
7. Continue toward the next obstacle.
8. Repeat the process for the remaining obstacles.
9. Reach the final destination without collision.

Later experiments will include moving obstacles and obstacles with different motion patterns.

---

## 9. Dynamic Obstacle Scenario

A further objective is to introduce moving obstacles.

The system will calculate the relative motion between the drone and the obstacle.

For example, an obstacle may approach the drone with increasing velocity.

The system will continuously update:

* Distance
* Closing speed
* TTC
* Risk level
* Navigation decision

This will allow the drone to react differently to a slowly approaching obstacle and a rapidly approaching obstacle.

---

## 10. System Architecture

The proposed architecture is:

```text
                 ┌──────────────────┐
                 │ PyBullet World   │
                 └────────┬─────────┘
                          │
                          ↓
                 ┌──────────────────┐
                 │ Drone Simulation │
                 └────────┬─────────┘
                          │
              ┌───────────┴───────────┐
              ↓                       ↓
       ┌─────────────┐         ┌──────────────┐
       │ IMU Sensor  │         │ Distance     │
       │ Roll/Pitch  │         │ Sensor       │
       └──────┬──────┘         └──────┬───────┘
              │                       │
              ↓                       ↓
       ┌─────────────┐         ┌──────────────┐
       │ PID         │         │ Risk         │
       │ Controller  │         │ Estimation   │
       └──────┬──────┘         └──────┬───────┘
              │                       │
              │                ┌──────┴───────┐
              │                │ ML Risk      │
              │                │ Prediction   │
              │                └──────┬───────┘
              │                       │
              └───────────┬───────────┘
                          ↓
                 ┌──────────────────┐
                 │ Decision         │
                 │ Controller       │
                 └────────┬─────────┘
                          ↓
              ┌────────────────────────┐
              │ CONTINUE / SLOW /      │
              │ AVOID / RETURN /       │
              │ RECOVER                │
              └───────────┬────────────┘
                          ↓
                 ┌──────────────────┐
                 │ Motor Control    │
                 └────────┬─────────┘
                          ↓
                 ┌──────────────────┐
                 │ Drone Movement   │
                 └──────────────────┘
```

---

## 11. Proposed Technologies

### Programming Language

* Python

### Simulation

* PyBullet

### Machine Learning

* Scikit-learn

### Data Processing

* NumPy
* Pandas

### Visualization

* Matplotlib

### Development Environment

* Visual Studio Code

### Version Control

* Git
* GitHub

---

## 12. Experimental Scenarios

The proposed system will be evaluated through multiple scenarios.

### Scenario 1 — Stable Flight

The drone will fly without obstacles and maintain the desired orientation.

### Scenario 2 — Static Obstacle

The drone will encounter stationary obstacles and autonomously avoid them.

### Scenario 3 — Multiple Obstacles

Three or more obstacles will be placed along the flight path in different configurations, including a zig-zag arrangement.

### Scenario 4 — Moving Obstacle

An obstacle will move toward or across the drone's flight path.

### Scenario 5 — Increasing-Speed Obstacle

The obstacle velocity will be increased during the simulation to test the response of the risk estimation and avoidance system.

### Scenario 6 — Disturbance and Recovery

External disturbances will be introduced to evaluate the drone's ability to recover its desired orientation using PID control.

---

## 13. Performance Evaluation

The system will be evaluated using measurable parameters such as:

* Obstacle detection distance
* Minimum distance from obstacle
* Collision occurrence
* Successful avoidance rate
* Time-to-collision estimation
* Drone position
* Roll error
* Pitch error
* PID response
* Recovery time
* Flight trajectory
* ML classification performance

Graphs and simulation results will be generated for analysis.

---

## 14. Expected Outcome

The expected outcome is a PyBullet-based autonomous drone simulation capable of maintaining stable flight and avoiding obstacles using a combination of control and intelligent decision-making techniques.

The final system is expected to:

* Maintain the desired roll and pitch.
* Detect obstacles before collision.
* Estimate collision risk.
* Slow down when required.
* Avoid multiple obstacles.
* Handle zig-zag obstacle configurations.
* Respond to moving obstacles.
* Recover its flight path after avoidance.
* Demonstrate ML-based risk prediction.
* Provide measurable simulation results.

---

## 15. Project Novelty

The proposed system combines **low-level control and high-level intelligent navigation**.

Instead of using only a predefined obstacle-avoidance path, the system will combine:

**PID stabilization + sensor-based measurements + TTC-based risk estimation + machine learning + decision-based navigation.**

The ML model will provide risk information, while the decision layer converts this information into navigation actions. PID control will operate at the stabilization level to maintain the drone's attitude during these maneuvers.

This separation allows the system to demonstrate both **control intelligence and navigation intelligence** within a single autonomous drone simulation.

---

## 16. Development Plan

```text
Phase 1
PyBullet drone simulation
        ↓
Phase 2
Drone movement and flight environment
        ↓
Phase 3
PID self-stabilization
        ↓
Phase 4
Obstacle detection
        ↓
Phase 5
Three-obstacle zig-zag avoidance
        ↓
Phase 6
TTC and collision-risk estimation
        ↓
Phase 7
Machine learning risk prediction
        ↓
Phase 8
Moving and increasing-speed obstacles
        ↓
Phase 9
Full PID + ML + obstacle avoidance integration
        ↓
Phase 10
Testing, graphs and performance evaluation
```

---

## 17. Repository and Version Control

The project will be maintained using Git and GitHub.

The `main` branch will contain the latest stable version of the project.

Individual team members may work on separate branches for their respective modules. After testing and verification, the completed work will be merged into the `main` branch.

The repository will therefore maintain a single integrated version for project evaluation.

---

## 18. Conclusion

This project proposes an autonomous drone simulation that combines self-stabilization and intelligent obstacle avoidance.

The system will use PyBullet for simulation, PID control for attitude stabilization, sensor-based mathematical calculations for obstacle detection and collision prediction, and machine learning for risk classification.

The final objective is to demonstrate a drone that can maintain stable flight, detect and assess obstacles, make navigation decisions, avoid multiple static and dynamic obstacles, and safely continue its mission.
