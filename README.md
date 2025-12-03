# Power System Stability Control – IEEE 9-Bus  
Simulation of PID, AVR, and UPFC Controllers for Improving Transient Stability  
*Faculty of Electrical Engineering Sarajevo – Department of Automation and Electronics*

This project analyzes transient stability of the **WECC 3-machine, 9-bus system** using **ModelSolver**.  
The work includes simulations of **PID controllers**, **AVR regulators**, and an integrated **PID + UPFC** approach under different fault conditions.

## Team
- **Ajla Herak** – aherak1@etf.unsa.ba  
- **Adelisa Hasic** – ahasic2@etf.unsa.ba
- **Naida Mehic** – nmehic1@etf.unsa.ba  
  
Department of Automation and Electronics, Faculty of Electrical Engineering, Sarajevo, Bosnia and Herzegovina

---

## Project Overview

The goal is to evaluate how different controllers influence system stability during disturbances such as short circuits and line outages.  
The system is modeled using **DAE equations**, with power-flow initialization, swing equations, and controller dynamics.

Key objectives:

- Analyze the dynamic behavior of the IEEE 9-bus system  
- Compare PID vs. AVR performance  
- Investigate UPFC + PID for enhanced damping  
- Tune controller parameters using **GA** and **PSO**  
- Run full transient simulations in **ModelSolver**

---

## Features

### ModelSolver Simulations
- Time-domain DAE simulation  
- Newton–Raphson power-flow  
- Multi-machine swing equation modeling  

### Controllers Implemented
- **PID generator speed controllers**  
- **AVR (Automatic Voltage Regulator)**  
- **UPFC with PID**, damping logic, anti-windup  

### Optimization
- Genetic Algorithm for PID tuning  
- Particle Swarm Optimization for UPFC tuning  

### Fault Scenarios Simulated
1. Transmission line outage (6–7)  
2. Three-phase short-circuit at Bus 7 + line 5–7 disconnection  

### System Variables Observed  
- Frequencies  
- Rotor speeds  
- Direct/Quadrature currents  
- Bus voltages  
- Rotor/phase angles  

