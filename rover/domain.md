# 🛰️ Rover Domain (PDDL)

The **Rover Domain** simulates a planetary exploration mission in which multiple rovers navigate across terrain, collect samples, take images, and transmit data via landers. It tests planning under resource constraints, calibration dependencies, and multi-agent coordination.

---

## 📂 Domain Overview

### Objects

- **Rovers**: Agents that navigate and operate sensors
- **Stores**: Storage compartments to hold samples
- **Cameras**: Imaging devices mounted on rovers
- **Waypoints**: Locations across the planetary terrain
- **Landers**: Stations used for data transmission and recharging
- **Objectives**: Targets for imaging from specified waypoints

---

## 🧮 Domain Type: Restricted Numeric Planning (RNP)

This domain includes:

**Preconditions** combining **predicates** and **single-variable numeric constraints**:
```lisp
(>= (energy ?r) 5)
(at_rock_sample ?w)
(equipped_for_rock_analysis ?r)
(store_of ?s ?r)
(empty ?s)
```

**Effects** include both:
- **Propositional changes**:
```lisp
(not (empty ?s))
(full ?s)
(have_rock_analysis ?r ?w)
(not (at_rock_sample ?w))
```

- And **constant numeric updates**:
```lisp
(decrease (energy ?r) 5)
```

**Goals** are entirely **predicate-based**:
```lisp
(communicated_soil_data waypoint0)
(communicated_rock_data waypoint0)
(communicated_image_data objective1 low_res)
```

Since preconditions use **single fluents and predicates**, effects are **constant or logical**, and goals are **propositional**, this domain is classified as **RNP (Restricted Numeric Planning)**.

---

## ⚙️ Domain Mechanics

### Predicates

- **`(at_soil_sample ?w)`**
- **`(at_rock_sample ?w)`**
- **`(in_sun ?w)`**
- **`(in ?r ?w)`**
- **`(on_board ?c ?r)`**
- **`(available ?r)`**
- **`(equipped_for_imaging ?r)`**
- **`(equipped_for_rock_analysis ?r)`**
- **`(equipped_for_soil_analysis ?r)`**
- **`(empty ?s)`**
- **`(full ?s)`**
- **`(store_of ?s ?r)`**
- **`(calibration_target ?c ?o)`**
- **`(supports ?c ?m)`**
- **`(channel_free ?l)`**
- **`(at_lander ?l ?w)`**
- **`(visible ?w1 ?w2)`**
- **`(visible_from ?o ?w)`**
- **`(calibrated ?c ?o ?r)`**
- **`(have_soil_analysis ?r ?w)`**
- **`(have_rock_analysis ?r ?w)`**
- **`(have_image ?r ?o ?m)`**
- **`(communicated_soil_data ?w)`**
- **`(communicated_rock_data ?w)`**
- **`(communicated_image_data ?o ?m)`**

### Functions

- **`(energy ?r)`** — current energy level of rover  
- **`(recharges)`** — total number of recharge operations used

---

## 🔧 Actions

### 🔋 `recharge`
<pre>
(:action recharge
 :parameters (?r - rover ?w - waypoint)
 :precondition (and (in ?r ?w) (in_sun ?w) (<= (energy ?r) 80))
 :effect (and (increase (energy ?r) 20) (increase (recharges) 1)))
</pre>

---

### 🧪 `sample_soil`
<pre>
(:action sample_soil
 :parameters (?r - rover ?s - store ?w - waypoint)
 :precondition (and (in ?r ?w) (>= (energy ?r) 3) (at_soil_sample ?w)
                    (equipped_for_soil_analysis ?r) (store_of ?s ?r) (empty ?s))
 :effect (and (not (empty ?s)) (full ?s) (decrease (energy ?r) 3)
              (have_soil_analysis ?r ?w) (not (at_soil_sample ?w))))
</pre>

---

### 🪨 `sample_rock`
<pre>
(:action sample_rock
 :parameters (?r - rover ?s - store ?w - waypoint)
 :precondition (and (in ?r ?w) (>= (energy ?r) 5) (at_rock_sample ?w)
                    (equipped_for_rock_analysis ?r) (store_of ?s ?r) (empty ?s))
 :effect (and (not (empty ?s)) (full ?s) (decrease (energy ?r) 5)
              (have_rock_analysis ?r ?w) (not (at_rock_sample ?w))))
</pre>

---

### 🪙 `drop`
<pre>
(:action drop
 :parameters (?r - rover ?s - store)
 :precondition (and (store_of ?s ?r) (full ?s))
 :effect (and (not (full ?s)) (empty ?s)))
</pre>

---

### ⚙️ `calibrate`
<pre>
(:action calibrate
 :parameters (?r - rover ?c - camera ?o - objective ?w - waypoint)
 :precondition (and (equipped_for_imaging ?r) (calibration_target ?c ?o)
                    (in ?r ?w) (visible_from ?o ?w) (on_board ?c ?r) (>= (energy ?r) 2))
 :effect (and (calibrated ?c ?o ?r) (decrease (energy ?r) 2)))
</pre>

---

### 📷 `take_image`
<pre>
(:action take_image
 :parameters (?r - rover ?w - waypoint ?o - objective ?c - camera ?m - mode)
 :precondition (and (calibrated ?c ?o ?r) (on_board ?c ?r) (equipped_for_imaging ?r)
                    (supports ?c ?m) (visible_from ?o ?w) (in ?r ?w) (>= (energy ?r) 1))
 :effect (and (have_image ?r ?o ?m) (not (calibrated ?c ?o ?r)) (decrease (energy ?r) 1)))
</pre>

---

### 🚚 `navigate`
<pre>
(:action navigate
 :parameters (?r - rover ?from - waypoint ?to - waypoint)
 :precondition (and (can_traverse ?r ?from ?to) (available ?r)
                    (in ?r ?from) (visible ?from ?to) (>= (energy ?r) 8))
 :effect (and (decrease (energy ?r) 8) (not (in ?r ?from)) (in ?r ?to)))
</pre>

---

### 📤 `communicate_soil_data`
<pre>
(:action communicate_soil_data
 :parameters (?r - rover ?l - lander ?p - waypoint ?x - waypoint ?y - waypoint)
 :precondition (and (in ?r ?x) (at_lander ?l ?y) (have_soil_analysis ?r ?p)
                    (visible ?x ?y) (available ?r) (channel_free ?l)
                    (not (communicated_soil_data ?p)) (>= (energy ?r) 4))
 :effect (and (communicated_soil_data ?p) (available ?r) (decrease (energy ?r) 4)))
</pre>

---

### 📤 `communicate_rock_data`
<pre>
(:action communicate_rock_data
 :parameters (?r - rover ?l - lander ?p - waypoint ?x - waypoint ?y - waypoint)
 :precondition (and (in ?r ?x) (at_lander ?l ?y) (have_rock_analysis ?r ?p)
                    (visible ?x ?y) (available ?r) (channel_free ?l)
                    (not (communicated_rock_data ?p)) (>= (energy ?r) 4))
 :effect (and (communicated_rock_data ?p) (available ?r) (decrease (energy ?r) 4)))
</pre>

---

### 📤 `communicate_image_data`
<pre>
(:action communicate_image_data
 :parameters (?r - rover ?l - lander ?o - objective ?m - mode ?x - waypoint ?y - waypoint)
 :precondition (and (in ?r ?x) (at_lander ?l ?y) (have_image ?r ?o ?m)
                    (visible ?x ?y) (available ?r) (channel_free ?l)
                    (not (communicated_image_data ?o ?m)) (>= (energy ?r) 6))
 :effect (and (communicated_image_data ?o ?m) (available ?r) (decrease (energy ?r) 6)))
</pre>

---

## 🔍 What the Planner Tries to Do

The planner aims to:

- Navigate rovers to waypoints with resources  
- Calibrate cameras and take images of objectives  
- Collect samples (soil, rock) using stores  
- Transmit collected data via landers  
- Use energy efficiently and minimize `(recharges)`

---

## 🧾 Example

### Scenario

- There is one rover at waypoint0
- waypoint0 contains a soil sample
- The lander is also at waypoint0
- The rover is equipped for soil analysis
- The goal is to communicate soil data from waypoint0

### Initial State

- Rover: rover0
- Location: waypoint0
- Energy: 50
- Equipped for: Soil analysis
- Store: rover0store (empty, linked to rover0)
- Lander: general at waypoint0 with free channel
- Soil sample at: waypoint0
- In sun: waypoint0

### Goal

```lisp
(communicated_soil_data waypoint0)

```

### Strategy

1. 🧪 Use sample_soil at waypoint0

2. 📤 Use communicate_soil_data from waypoint0 while near the lander

---

## 🧪 Example Use Cases

- Robotic Mars exploration  
- Autonomous scientific data collection  
- Energy-aware path planning  
- Sensor calibration strategies  
- Multi-agent coordination under constraints

---

## 🎒 Extras

This domain is ideal for:

- Evaluating planners on numeric fluents and conditional effects  
- Testing multi-agent collaboration and resource sharing  
- Simulating real-world rover missions with constrained resources
