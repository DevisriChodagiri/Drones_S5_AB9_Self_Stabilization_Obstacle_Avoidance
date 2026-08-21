<p align="center">
  <img width="441" height="114" alt="logo-branding-amrita-universiy-2024" src="https://github.com/user-attachments/assets/d939ec0b-574a-4d8e-8140-80275a9c9fa7" />
</p>

<div align="center"> <h2> AUTONOMOUS SELF-STABILIZING DRONE WITH OBSTACLE AVOIDANCE </h2> </div>

<p align="center">
  <img src="./results/amrita_logo.png" alt=""C:\Users\DEVI SRI\OneDrive\Desktop\Downloads\logo-branding-amrita-universiy-2024.jpeg"" width="200">
</p>

<p align="center">
  <b>AMRITA VISHWA VIDYAPEETHAM</b><br>
  Coimbatore, Tamil Nadu<br>
  Department of Computer Science and Engineering(Artificial Intelligence)
</p>

---

## TEAM MEMBER DETAILS

| S.No. | Name | Roll Number | Email |
|---|---|---|---|
| 1 | Devisri | CB.SC.U4AIE24163 | devisri7142@gmail.com |
| 2 | Monisha | CB.SC.U4AIE24157 | vemurimonishareddy@gmail.com |
| 3 | Myagi | CB.SC.U4AIE24143 | patimamyagi@gmail.com |

**Team Number:** AB14

---

## TITLE

### Autonomous Self-Stabilizing Drone with Obstacle Avoidance

---

## ABSTRACT

Autonomous drones require stability, environmental awareness, and safe decision-making to operate effectively without continuous human intervention. A drone may become unstable due to changes in its roll and pitch, while obstacles in its flight path can lead to collisions.

This project presents an **Autonomous Self-Stabilizing Drone with Obstacle Avoidance** that combines PID-based stabilization, Machine Learning-based safety prediction, high-attitude detection, automatic recovery, obstacle detection, and obstacle avoidance.

The drone continuously monitors important flight parameters such as **roll, pitch, speed, and distance from obstacles**. A PID controller is used to reduce the error between the desired and current attitude and maintain stable flight.

A **Logistic Regression** model is used as a Machine Learning safety layer. The model uses distance, speed, roll, and pitch as input features and predicts whether the current flight condition is **SAFE or UNSAFE**.

When the drone reaches an unsafe attitude condition, the high-attitude detection mechanism identifies the instability and activates a recovery controller. The recovery controller gradually reduces the attitude deviation and brings the drone back toward a stable state.

An ultrasonic distance measurement is used to detect obstacles in the drone's path. When an obstacle is detected, the drone enters obstacle avoidance mode. After the obstacle is cleared, the system returns the drone to forward flight.

The complete system is developed and evaluated using **Simulink** and **Python-based Machine Learning components**.

---

## INTRODUCTION

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

## METHODOLOGY

The proposed system consists of multiple modules that work together to provide autonomous and safe drone operation.

The major stages of the methodology are:

#### Complete System Operation

The complete system operates through the following sequence:

1. **Sensor Monitoring**  
   The drone continuously monitors roll, pitch, speed, and distance.

2. **PID Stabilization**  
   Roll and pitch deviations are corrected using the PID controller.

3. **Machine Learning Safety Prediction**  
   The Logistic Regression model classifies the current flight condition as SAFE or UNSAFE.

4. **Instability Detection**  
   If the drone reaches an unsafe attitude, the high-attitude detection mechanism is activated.

5. **Recovery Control**  
   The recovery controller reduces the attitude deviation and brings the drone toward a stable state.

6. **Obstacle Detection**  
   The distance measurement is continuously checked for obstacles.

7. **Obstacle Avoidance**  
   If an obstacle is detected, the drone enters avoidance mode.

8. **Return to Forward Flight**<br>
   After the obstacle is cleared, the drone returns to forward flight.

   
   ---
   ---
## 7. RESULTS

The proposed **Autonomous Self-Stabilizing Drone with Obstacle Avoidance** was tested by evaluating the individual modules and their integrated behavior. The results demonstrate the performance of the machine learning safety prediction, PID-based stabilization, obstacle avoidance, and recovery control mechanisms.

### 7.1 ML-Based Safe/Unsafe Prediction

The Logistic Regression model was used to classify the current drone flight condition as **SAFE** or **UNSAFE**. The model takes parameters such as distance, speed, roll, and pitch as input and predicts whether the current flight condition is suitable for safe operation.

The testing results demonstrate that the trained model can distinguish between safe and potentially unsafe drone states based on the given flight parameters.

**Figure 1: ML-based Safe/Unsafe prediction result**

<!-- Add ML result image here -->
<img width="851" height="245" alt="ml_prediction_safe" src="https://github.com/user-attachments/assets/af836e16-d887-4fc4-9138-0c93c44bead5" />
(<img width="482" height="222" alt="ml_prediction_unsafe" src="https://github.com/user-attachments/assets/86fb111d-3269-40b9-97a5-9ff11cdd16b9" />
)


### 7.2 PID Stabilization Result

The PID controller was implemented to maintain the drone's desired orientation during flight. The controller continuously monitors the roll and pitch values and calculates corrective responses whenever the drone deviates from its desired orientation.

The simulation results show that the controller reduces attitude deviations and brings the drone back toward a stable orientation. This demonstrates the ability of the PID controller to maintain self-stabilization during flight.

**Figure 2: PID-based drone stabilization result**

<!-- Add PID stabilization image here -->
(<img width="1477" height="275" alt="PID_Stabilization_Result" src="https://github.com/user-attachments/assets/04d6818c-0f29-4528-9a78-2982bca23a5a" />)


### 7.3 Obstacle Avoidance Result

The ultrasonic sensor simulation was used to measure the distance between the drone and an obstacle. When the measured distance decreases below the defined safety threshold, the obstacle avoidance mechanism is activated.

The drone changes its flight behavior to avoid the detected obstacle instead of continuing its normal forward flight. After the obstacle is sufficiently cleared, the system can return toward its normal forward-flight behavior.

**Figure 3: Obstacle detection and avoidance result**

<!-- Add obstacle avoidance image here -->
(<img width="881" height="547" alt="Obstacle_Avoidance_Result" src="https://github.com/user-attachments/assets/45ac078e-22d9-44a8-b12d-51150bfcaa00" />)


### 7.4 Recovery Control Result

The recovery controller is activated when the drone experiences a large roll or pitch deviation and becomes unstable. The controller applies corrective actions to reduce the attitude error and restore the drone to a stable state.

The simulation results show the roll and pitch values progressively decreasing toward the stable region during recovery. This demonstrates that the recovery controller can respond to unstable flight conditions and attempt to restore stable flight.

**Figure 4: Recovery controller response**

<!-- Add recovery control image here -->
(<img width="1201" height="591" alt="Recovery_Controller_Result" src="https://github.com/user-attachments/assets/c5c8394c-2902-47ae-9170-54435acdef1a" />)





### 7.5 Overall Results

The experimental and simulation results demonstrate that the proposed system can:

- Predict whether a flight condition is **SAFE or UNSAFE** using Logistic Regression.
- Maintain drone orientation using **PID-based stabilization**.
- Detect obstacles using distance measurements and initiate **obstacle avoidance**.
- Detect significant attitude deviations and activate the **recovery controller**.
- Integrate all the modules into an autonomous flight-control framework.

Overall, the results indicate that the proposed **Autonomous Self-Stabilizing Drone with Obstacle Avoidance** provides a combined approach for improving drone stability, obstacle awareness, and flight safety.

---
## 8. CONCLUSION

The proposed **Autonomous Self-Stabilizing Drone with Obstacle Avoidance** was successfully designed and evaluated using MATLAB/Simulink and machine learning techniques. The system combines **PID-based attitude stabilization, ultrasonic-based obstacle detection, obstacle avoidance, recovery control, and Logistic Regression-based safety prediction** into a unified autonomous flight-control framework.

The PID controller helps maintain the drone's roll and pitch stability during flight, while the ultrasonic sensor enables the system to detect obstacles and initiate appropriate avoidance actions. When significant attitude deviations occur, the recovery controller is activated to bring the drone back toward a stable condition. In addition, the Logistic Regression model classifies the current flight condition as **SAFE or UNSAFE** based on important flight parameters such as distance, speed, roll, and pitch.

The simulation results demonstrate that the individual modules and their integrated operation perform as expected under the tested conditions. The system is therefore capable of improving **flight stability, obstacle awareness, and autonomous safety decision-making**.

Overall, this project demonstrates how **control systems, sensor-based decision-making, simulation, and machine learning** can be combined to develop a more reliable autonomous drone system. Future work can focus on real-time hardware implementation, additional sensors, more advanced machine learning models, and testing under real-world flight conditions.

---
## 9. REFERENCES

1. López-Sánchez, I., & Moreno-Valenzuela, J. (2023).  
   **PID Control of Quadrotor UAVs: A Survey.**  
   *Annual Reviews in Control, 56, 100900.*  
   [Paper Link](https://doi.org/10.1016/j.arcontrol.2023.100900)

2. Sun, X., & Yang, J. (2023).  
   **Design of a Quadcopter Based on Ultrasonic Obstacle Avoidance.**  
   *Journal of Hebei University of Water Resources and Electric Engineering.*  
   [Paper Link](https://xuebao.hbwe.edu.cn/EN/10.16046/j.cnki.issn2096-5680.2023.03.002)

3. Lotufo, M. A., Colangelo, L., Perez-Montenegro, C. N., Canuto, E., & Novara, C. (2019).  
   **UAV Quadrotor Attitude Control: An ADRC-EMC Combined Approach.**  
   *Control Engineering Practice, 84, 13–22.*  
   [Paper Link](https://doi.org/10.1016/j.conengprac.2018.11.002)

4. López-Sánchez, I., & Moreno-Valenzuela, J. (2019).  
   **Position and Attitude Control of Multi-Rotor Aerial Vehicles: A Survey.**  
   *Annual Reviews in Control.*  
   [Paper Link](https://doi.org/10.1016/j.arcontrol.2019.03.001)

5. **Design of Rules for In-Flight Non-Parametric Tuning of PID Controllers for Unmanned Aerial Vehicles.** (2019).  
   *Journal of the Franklin Institute.*  
   [Paper Link](https://doi.org/10.1016/j.jfranklin.2018.10.015)
