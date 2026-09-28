# 🚦 Smart Traffic Light Intersection

### Intelligent Traffic Signal Simulation with Python & Pygame

<p align="center">
  <strong>🚗 Realistic Traffic Simulation • 🧠 Smart Signal Control • 🚑 Emergency Priority • 📊 Performance Analytics</strong>
</p>

<p align="center">
  A modular traffic intersection simulator built with <strong>Python</strong> and <strong>Pygame</strong>, featuring Fixed-Time and Smart adaptive traffic-light control.
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.x-00A86B?style=for-the-badge\&logo=python\&logoColor=white)
![Architecture](https://img.shields.io/badge/Architecture-Modular-8A2BE2?style=for-the-badge)
![AI Controller](https://img.shields.io/badge/Controller-Smart%20Adaptive-FF6B35?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-2EA44F?style=for-the-badge)

</p>

---

## 📌 Overview

**Smart Traffic Light Intersection** is a traffic simulation designed to demonstrate how adaptive traffic-light systems can respond to changing traffic conditions.

Instead of relying only on fixed timing, the simulator includes a **Smart Controller** that evaluates traffic conditions and dynamically determines how long each direction should receive a green light.

The project also simulates:

* 🚗 Vehicle acceleration and braking
* 🛑 Safe stopping distances
* 🚦 Traffic-light state transitions
* 📊 Traffic density and queues
* 🚑 Emergency vehicle priority
* 📈 Traffic statistics
* 🚧 Traffic backlog outside the map
* ⚡ Fixed vs Smart comparison
* 🎮 Interactive controls
* 🧩 Modular architecture ready for ML/RL integration

---

# ✨ Features

| Feature                        | Description                                   |
| ------------------------------ | --------------------------------------------- |
| 🚦 **Fixed Mode**              | Traditional fixed-time traffic signals        |
| 🧠 **Smart Mode**              | Adaptive green-light control based on traffic |
| 🚗 **Vehicle Physics**         | Acceleration, braking and safety distance     |
| 🛑 **Red-Light Safety**        | Vehicles never cross a red signal             |
| 🟡 **Yellow Logic**            | Vehicles stop if safe; otherwise continue     |
| 🔄 **Safe Transitions**        | `GREEN → YELLOW → ALL_RED → GREEN`            |
| 🚑 **Emergency Priority**      | Emergency vehicles receive priority           |
| 📊 **Traffic Score**           | Combines cars, queues and waiting time        |
| 🚧 **Backlog Tracking**        | Vehicles waiting outside the map are counted  |
| ⏱️ **Starvation Guard**        | Prevents excessive waiting                    |
| 🌙 **Time Modes**              | Auto, Night, Normal, AM Rush, PM Rush         |
| 📈 **Statistics**              | Measures traffic performance                  |
| 🧪 **Headless Comparison**     | Fixed vs Smart using the same seed            |
| 🎮 **Interactive UI**          | Controls available directly in the dashboard  |
| 🧩 **Extensible Architecture** | Ready for ML/RL controllers                   |

---

# 🖥️ Simulation

<p align="center">

<!-- Replace this with your actual screenshot -->

<img src="assets/simulation.png" width="850">

</p>

> 💡 **Tip:** Add your best screenshot to `assets/simulation.png` to make the repository immediately visual and professional.

---

# 🧠 Smart Traffic Control

The Smart Controller dynamically calculates the required green-light duration using the current traffic conditions.

### Green-Time Formula

```text
Green Time =
    15
  + 2 × cars
  + 0.2 × average_wait
```

The result is then limited between configurable minimum and maximum values:

```text
MIN_GREEN ≤ Green Time ≤ MAX_GREEN
```

This means that:

* 🚗 More vehicles → longer green time
* ⏳ Higher waiting time → longer green time
* 🟢 Empty roads → green can finish earlier
* 🚨 Excessive waiting → starvation protection activates

---

# 📊 Traffic Score

The Smart Controller evaluates traffic using:

```text
Traffic Score =
    cars
  + 1.5 × queue
  + 0.2 × average_wait
```

This combines three important signals:

```text
             ┌──────────────┐
             │ Traffic Data │
             └──────┬───────┘
                    │
       ┌────────────┼────────────┐
       ▼            ▼            ▼
    🚗 Cars      🚧 Queue    ⏳ Wait Time
       │            │            │
       └────────────┼────────────┘
                    ▼
             Traffic Score
                    │
                    ▼
          🧠 Smart Controller
                    │
                    ▼
             🚦 Green Time
```

---

# 🚦 Traffic-Light State Machine

The simulator never jumps directly from one green direction to the other.

```text
              ┌───────────────┐
              │     GREEN     │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │    YELLOW     │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │    ALL RED    │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │ OTHER GREEN   │
              └───────────────┘
```

This provides a safer transition between traffic directions.

---

# 🚗 Vehicle Behaviour

Vehicles are simulated with basic acceleration and braking behaviour.

Each vehicle considers:

```text
Acceleration
     ↓
Current speed
     ↓
Distance to vehicle ahead
     ↓
Traffic signal
     ↓
Safe stopping distance
     ↓
Target speed
```

### Safe stopping rule

The simulator uses the braking-distance relationship:

```text
v²
─── ≤ distance
2a
```

If a vehicle can safely stop before the intersection, it stops.

If stopping would no longer be safe, the vehicle continues through the yellow phase.

This avoids unrealistic instant braking.

---

# 🚑 Emergency Priority

Emergency vehicles can be introduced dynamically using:

```text
E
```

The priority system:

```text
Emergency detected
       │
       ▼
Identify direction
       │
       ▼
Check current signal
       │
       ▼
Finish opposing green safely
       │
       ▼
Yellow
       │
       ▼
All Red
       │
       ▼
🚑 Emergency Green
       │
       ▼
Emergency passes
       │
       ▼
Return to Smart/Fixed control
```

Supported emergency types include:

* 🚑 Ambulance
* 🚒 Fire Truck
* 🚓 Police

---

# 🌡️ Traffic Density

The simulator supports four traffic-density levels:

| Level | Mode      |
| ----- | --------- |
| 🟢    | LOW       |
| 🟡    | MEDIUM    |
| 🟠    | HIGH      |
| 🔴    | VERY HIGH |

Change density during simulation using:

```text
1 → LOW
2 → MEDIUM
3 → HIGH
4 → VERY HIGH
```

---

# 🕐 Time Modes

Press:

```text
T
```

to cycle through:

```text
AUTO
  ↓
NIGHT
  ↓
NORMAL
  ↓
AM RUSH
  ↓
PM RUSH
  ↓
AUTO
```

Different time periods can generate different traffic behaviour and densities.

---

# 🎮 Controls

|   Key   | Action                        |
| :-----: | ----------------------------- |
|   `F`   | Switch to Fixed Mode          |
|   `S`   | Switch to Smart Mode          |
| `SPACE` | Pause / Resume                |
|   `R`   | Reset simulation              |
|   `1`   | LOW traffic                   |
|   `2`   | MEDIUM traffic                |
|   `3`   | HIGH traffic                  |
|   `4`   | VERY HIGH traffic             |
|   `T`   | Change time mode              |
|   `E`   | Spawn emergency vehicle       |
|   `C`   | Run Fixed vs Smart comparison |

### ⚡ Simulation Speed

The dashboard also provides:

```text
0.5×   1×   2×   5×   10×
```

---

# 📈 Fixed vs Smart

The project includes an actual headless comparison system.

Press:

```text
C
```

to run a comparison between:

```text
┌──────────────────┐
│   SAME SEED      │
└────────┬─────────┘
         │
    ┌────┴────┐
    ▼         ▼
 Fixed      Smart
    │         │
    ▼         ▼
Simulation Simulation
    │         │
    └────┬────┘
         ▼
   📊 Statistics
```

Using the same random seed allows both controllers to be evaluated under the same generated traffic conditions.

Typical metrics can include:

* Average waiting time
* Maximum waiting time
* Queue size
* Throughput
* Number of vehicles
* Backlog
* Simulation duration

> This makes the comparison reproducible rather than simply comparing two different random simulations.

---

# 🏗️ Architecture

The project follows a modular architecture so that simulation logic, AI logic and UI remain separated.

```text
smart_traffic/
│
├── 📄 config.py
│
├── 📁 simulation/
│   ├── car.py
│   ├── traffic_light.py
│   ├── intersection.py
│   ├── traffic_manager.py
│   ├── statistics.py
│   ├── simulation.py
│   └── comparison.py
│
├── 📁 ai/
│   ├── traffic_controller.py
│   ├── traffic_score.py
│   └── priority_system.py
│
├── 📁 ui/
│   ├── renderer.py
│   └── dashboard.py
│
├── 📄 main.py
├── 📄 requirements.txt
└── 📄 README.md
```

---

# 🔌 Controller Interface

The traffic controller exposes a small interface:

```python
green_time(...)
should_end_green(...)
choose_next_axis(...)
```

This makes it possible to replace the current Smart Controller without rewriting the simulation.

Current architecture:

```text
                Simulation
                    │
                    ▼
             Traffic Manager
                    │
                    ▼
          ┌──────────────────┐
          │ Traffic Controller│
          └────────┬─────────┘
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
   FixedController      SmartController
                              │
                              ▼
                       Traffic Metrics
```

---

# 🤖 Future ML / RL Integration

The architecture is designed to support a future Machine Learning or Reinforcement Learning controller.

For example:

```text
Camera / YOLO
     │
     ▼
Vehicle Detection
     │
     ▼
Traffic Metrics
     │
     ▼
ML / RL Controller
     │
     ▼
Traffic Signal
```

A future controller could learn from:

```text
State:
├── Number of vehicles
├── Queue length
├── Average waiting time
├── Current signal
├── Time since last switch
└── Emergency vehicles

Action:
├── Keep green
├── Switch direction
└── Extend green

Reward:
├── Lower waiting time
├── Lower queue length
├── Higher throughput
└── Emergency priority
```

The existing simulation can remain unchanged while replacing only the controller.

---

# 📷 Computer Vision Integration

A future version can replace the simulated traffic source with real camera data.

Possible pipeline:

```text
📹 Traffic Camera
       │
       ▼
   YOLO Detection
       │
       ▼
Vehicle Counting
       │
       ▼
Queue Estimation
       │
       ▼
Traffic Metrics
       │
       ▼
Smart Controller
       │
       ▼
🚦 Traffic Signal
```

This would allow the project to evolve from a simulation into a real-world traffic-management prototype.

---

# ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/smart-traffic.git
cd smart-traffic
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the simulation

```bash
python main.py
```

---

# 💻 Requirements

Recommended environment:

```text
Python 3.11+
Pygame 2.x
Windows / Linux
```

The simulation is lightweight and does not require a dedicated GPU.

---

# 🧪 Example Workflow

A typical test session can look like:

```text
1. Start simulation
        ↓
2. Select VERY HIGH traffic
        ↓
3. Run Fixed Mode
        ↓
4. Observe queues / waiting
        ↓
5. Switch to Smart Mode
        ↓
6. Observe adaptive green times
        ↓
7. Spawn emergency vehicle
        ↓
8. Observe priority handling
        ↓
9. Press C
        ↓
10. Compare Fixed vs Smart
```

---

# 📊 Project Goals

The project aims to demonstrate several concepts together:

### 🚦 Traffic Simulation

Real-time intersection behaviour with vehicles, queues and signals.

### 🧠 Adaptive Control

Traffic lights respond to current traffic conditions instead of using only fixed timing.

### 🚑 Priority Management

Emergency vehicles can temporarily override normal traffic control.

### 📈 Data Analysis

Simulation statistics can be used to evaluate controller performance.

### 🤖 AI Ready

The architecture provides a clean path toward ML/RL-based traffic control.

---

# 🛣️ Roadmap

* [x] Basic intersection simulation
* [x] Vehicle movement
* [x] Acceleration / braking
* [x] Safe stopping logic
* [x] Fixed traffic controller
* [x] Smart traffic controller
* [x] Traffic scoring
* [x] Emergency priority
* [x] Traffic backlog
* [x] Simulation statistics
* [x] Fixed vs Smart comparison
* [x] Interactive dashboard
* [ ] Multiple lanes
* [ ] Left / right turns
* [ ] Pedestrian crossings
* [ ] Multiple intersections
* [ ] Network-wide traffic control
* [ ] YOLO vehicle detection
* [ ] Real camera input
* [ ] Reinforcement Learning controller
* [ ] Real-time analytics dashboard

---

# 🎯 Why This Project?

Traditional traffic signals often rely on predefined timing.

Real traffic, however, is dynamic.

A road can suddenly become:

```text
LOW
 ↓
MEDIUM
 ↓
HIGH
 ↓
VERY HIGH
```

while another direction remains almost empty.

An adaptive system can use live traffic information to adjust the signal accordingly.

This project provides a controlled environment for experimenting with these ideas before moving toward computer vision, machine learning and real-world traffic systems.

---

# 👨‍💻 Project Structure Philosophy

The main design principle is:

> **Keep the simulation independent from the intelligence controlling it.**

That means:

```text
Simulation ≠ AI ≠ UI
```

Each component has its own responsibility:

```text
Simulation
→ What happens?

AI Controller
→ What should the traffic light do?

UI
→ How does the user see and control it?
```

This separation makes the project easier to test, maintain and extend.

---

# ⭐ Future Vision

The long-term goal is to evolve the project into a complete intelligent traffic-management platform:

```text
             🚗 🚗 🚗
          🚗           🚗
               │
               │
        📹 Traffic Camera
               │
               ▼
          YOLO Detection
               │
               ▼
        Traffic Analytics
               │
               ▼
       🧠 AI / RL Controller
               │
               ▼
          🚦 Smart Signals
               │
               ▼
        📊 Performance Data
               │
               └──────────────┐
                              │
                              ▼
                         Continuous
                          Learning
```

---

## 📜 License

Add your preferred license here, for example:

```text
MIT License
```

---

<p align="center">

### 🚦 Built with Python • Pygame • AI-oriented Architecture

**Smart Traffic Light Intersection**

</p>
