# 🌱 Extended Plant Watering Domain (PDDL)

The **Extended Plant Watering Domain** models a team of agents navigating a 2D grid to water plants. Agents carry limited amounts of water from a central tap and distribute it to plants, while managing total water usage and individual capacity constraints.

This domain reflects **resource-constrained spatial planning**, combining geometric navigation, numeric resource control, and continuous action tracking.

---

## 📂 Domain Overview

### Objects

- **Agents**: Move across the map to load and pour water.  
- **Plants**: Need to be watered to reach a certain goal amount.  
- **Taps**: Fixed locations where water is loaded.  
- **Locations**: Points on the grid with x/y coordinates.

---

## ⚙️ Domain Mechanics

### Predicates

This domain uses only numeric fluents and does not rely on traditional predicates.

---

### Functions

- `(x ?t)` — X-coordinate of thing `?t`.  
- `(y ?t)` — Y-coordinate of thing `?t`.  
- `(maxx)` — Maximum allowed x-coordinate.  
- `(maxy)` — Maximum allowed y-coordinate.  
- `(minx)` — Minimum allowed x-coordinate.  
- `(miny)` — Minimum allowed y-coordinate.  
- `(max_carry ?a)` — Max volume of water agent `?a` can carry.  
- `(carrying ?a)` — Water currently carried by agent `?a`.  
- `(poured ?p)` — Amount of water poured on plant `?p`.  
- `(water_reserve)` — Remaining water in the system.  
- `(total_poured)` — Total water poured so far.  
- `(total_loaded)` — Total water taken from the tap so far.

---

## ⚙️ Actions

### 🔼 `move_up`

<pre>
(:action move_up
 :parameters (?a - agent)
 :precondition (and (<= (+ (y ?a) 1) (maxy)))
 :effect (increase (y ?a) 1))
</pre>

### 🔽 `move_down`

<pre>
(:action move_down
 :parameters (?a - agent)
 :precondition (and (>= (- (y ?a) 1) (miny)))
 :effect (decrease (y ?a) 1))
</pre>

### ▶️ `move_right`

<pre>
(:action move_right
 :parameters (?a - agent)
 :precondition (and (<= (+ (x ?a) 1) (maxx)))
 :effect (increase (x ?a) 1))
</pre>

### ◀️ `move_left`

<pre>
(:action move_left
 :parameters (?a - agent)
 :precondition (and (>= (- (x ?a) 1) (minx)))
 :effect (decrease (x ?a) 1))
</pre>

### 🔼◀️ `move_up_left`

<pre>
(:action move_up_left
 :parameters (?a - agent)
 :precondition (and (>= (- (x ?a) 1) (minx)) (<= (+ (y ?a) 1) (maxy)))
 :effect (and (increase (y ?a) 1) (decrease (x ?a) 1)))
</pre>

### 🔼▶️ `move_up_right`

<pre>
(:action move_up_right
 :parameters (?a - agent)
 :precondition (and (<= (+ (x ?a) 1) (maxx)) (<= (+ (y ?a) 1) (maxy)))
 :effect (and (increase (y ?a) 1) (increase (x ?a) 1)))
</pre>

### 🔽◀️ `move_down_left`

<pre>
(:action move_down_left
 :parameters (?a - agent)
 :precondition (and (>= (- (x ?a) 1) (minx)) (>= (- (y ?a) 1) (miny)))
 :effect (and (decrease (x ?a) 1) (decrease (y ?a) 1)))
</pre>

### 🔽▶️ `move_down_right`

<pre>
(:action move_down_right
 :parameters (?a - agent)
 :precondition (and (<= (+ (x ?a) 1) (maxx)) (>= (- (y ?a) 1) (miny)))
 :effect (and (decrease (y ?a) 1) (increase (x ?a) 1)))
</pre>

### 💧 `load`

<pre>
(:action load
 :parameters (?a - agent ?t - tap)
 :precondition (and
   (= (x ?a) (x ?t))
   (= (y ?a) (y ?t))
   (<= (+ (carrying ?a) 1) (max_carry ?a))
   (>= (- (water_reserve) 1) 0))
 :effect (and
   (decrease (water_reserve) 1)
   (increase (carrying ?a) 1)
   (increase (total_loaded) 1)))
</pre>

### 🌿 `pour`

<pre>
(:action pour
 :parameters (?a - agent ?p - plant)
 :precondition (and
   (= (x ?a) (x ?p))
   (= (y ?a) (y ?p))
   (>= (carrying ?a) 1))
 :effect (and
   (decrease (carrying ?a) 1)
   (increase (poured ?p) 1)
   (increase (total_poured) 1)))
</pre>

---

## 🧮 Domain Type: Linear Task (LT)

This domain includes numeric constraints using arithmetic in **preconditions**, like:

<pre>
(<= (+ (carrying ?a) 1) (max_carry ?a))
(>= (- (water_reserve) 1) 0)
</pre>

These expressions go beyond constants and involve general linear updates, making this a **Linear Task (LT)** — the most expressive among SNT, RT, and LT.

---

## 🔍 What the Planner Tries to Do

The planner must:

- Navigate agents through a grid-based map  
- Load and distribute water efficiently  
- Ensure no agent exceeds its carrying limit  
- Manage the global water reserve  
- Reach all plants and meet their watering requirements

---

## 🧾 Example

Suppose:

- Agent `a1` has `max_carry = 3`  
- Tap `t1` is at `(2,2)`  
- Plant `p1` is at `(5,5)`  
- `water_reserve = 10`

**Initial state:**

- `a1` starts at `(2,2)`  
- `carrying(a1) = 0`, `poured(p1) = 0`

**Goal:**  
Deliver 3 units of water to `p1`.

**Strategy:**

- Load 3 units at the tap  
- Move to `p1` via shortest path  
- Pour 3 times

---

## 🧪 Example Use Cases

- Multi-agent field watering tasks  
- Environmental conservation scenarios  
- Resource-delivery logistics with constraints  
- Energy-aware spatial task planning

---

## 🎒 Extras

This domain is especially useful for:

- Testing planners with capacity and global resource constraints  
- Evaluating path-finding combined with numeric effects  
- Benchmarking linear constraint reasoning in multi-agent systems

