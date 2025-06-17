# 🚢 Sailing Domain (PDDL)

The **Sailing Domain** models a maritime rescue scenario where sailing boats navigate to save people stranded in an unbounded ocean area. Each boat and person has 2D coordinates, and the model accounts for varied sailing speeds depending on wind direction, with the wind assumed to come from the north.

This domain models **direction-based movement and location-based rescues**, useful for evaluating numeric planning strategies that involve 2D coordinate navigation and area-based constraints.

---

## 📂 Domain Overview

### Objects

- **Boats**: Vessels that navigate the ocean to rescue people.
- **People**: Individuals who need to be rescued from their locations.

---

## 🧮 Domain Type: Simple Numeric Planning (SNP)

This domain includes:

**Preconditions** with **linear expressions** over multiple fluents and constants:
```lisp
(>= (+ (x ?b) (y ?b)) (d ?t))
(>= (- (y ?b) (x ?b)) (d ?t))
(<= (+ (x ?b) (y ?b)) (+ (d ?t) 25))
(<= (- (y ?b) (x ?b)) (+ (d ?t) 25))
```

**Effects** apply **constant updates** to individual fluents:
```lisp
(increase (x ?b) 2)
(decrease (y ?b) 2)
```

**Goals** are propositional:
```lisp
(saved p0)
```

Since the domain uses **linear numeric preconditions**, **constant effects**, and **predicate-only goals**, it is classified as **SNP (Simple Numeric Planning)**.

---

## ⚙️ Domain Mechanics

### Predicates

- (saved ?t) — Person ?t has been rescued.

---

### Functions

- (x ?b) — The x-coordinate of boat ?b.
- (y ?b) — The y-coordinate of boat ?b.
- (d ?t) — Parameter related to the position of person ?t.

---

### ⚙️ Actions

#### ↗️ go_north_east

<pre>
(:action go_north_east
 :parameters (?b - boat)
 :effect (and
   (increase (x ?b) 1.5)
   (increase (y ?b) 1.5)))
</pre>

#### Description:
Moves a boat diagonally northeast, increasing both x and y coordinates by 1.5 units.

---

#### ↖️ go_north_west

<pre>
(:action go_north_west
 :parameters (?b - boat)
 :effect (and
   (decrease (x ?b) 1.5)
   (increase (y ?b) 1.5)))
</pre>

#### Description:
Moves a boat diagonally northwest, decreasing x and increasing y coordinates by 1.5 units.

---

#### ➡️ go_est

<pre>
(:action go_est
 :parameters (?b - boat)
 :effect (and
   (increase (x ?b) 3)))
</pre>

#### Description:
Moves a boat eastward, increasing the x coordinate by 3 units.

---

#### ⬅️ go_west

<pre>
(:action go_west
 :parameters (?b - boat)
 :effect (and
   (decrease (x ?b) 3)))
</pre>

#### Description:
Moves a boat westward, decreasing the x coordinate by 3 units.

---

#### ↘️ go_south_west

<pre>
(:action go_south_west
 :parameters (?b - boat)
 :effect (and
   (increase (x ?b) 2)
   (decrease (y ?b) 2)))
</pre>

#### Description:
Moves a boat diagonally southwest, increasing x and decreasing y coordinates by 2 units.

---

#### ↙️ go_south_east

<pre>
(:action go_south_east
 :parameters (?b - boat)
 :effect (and
   (decrease (x ?b) 2)
   (decrease (y ?b) 2)))
</pre>

#### Description:
Moves a boat diagonally southeast, decreasing both x and y coordinates by 2 units.

---

#### ⬇️ go_south

<pre>
(:action go_south
 :parameters (?b - boat)
 :effect (and
   (decrease (y ?b) 2)))
</pre>

#### Description:
Moves a boat southward, decreasing the y coordinate by 2 units.

---

#### 🆘 save_person

<pre>
(:action save_person
 :parameters (?b - boat ?t - person)
 :precondition (and
   (>= (+ (x ?b) (y ?b)) (d ?t))
   (>= (- (y ?b) (x ?b)) (d ?t))
   (<= (+ (x ?b) (y ?b)) (+ (d ?t) 25))
   (<= (- (y ?b) (x ?b)) (+ (d ?t) 25)))
 :effect (and
   (saved ?t)))
</pre>

#### Description:
Rescues a person when the boat is within a specific area defined by coordinate constraints.

---


## 🔍 What the Planner Tries to Do

The planner must:

- Navigate boats across a 2D coordinate system
- Account for different sailing speeds in various directions
- Determine efficient paths to reach people in need of rescue
- Satisfy complex coordinate-based constraints for rescue operations
- Mark people as saved once they're rescued

---

## 🧾 Example

Suppose:

- Boat b1 starts at coordinates (0,0)
- Person p1 needs to be rescued with d(p1) = 10

**Initial state:**
- x(b1) = 0, y(b1) = 0
- p1 is not saved

**Goal:**
- p1 is saved

The planner might decide:
1. Use go_north_east (b1) twice to reach (3,3)
2. Use go_north_east (b1) again to reach (4.5,4.5)
3. Use go_north_east (b1) one more time to reach (6,6)
4. Use save_person (b1, p1) since (6+6)≥10 and other constraints are satisfied

---

## 🧪 Example Use Cases

- Maritime search and rescue operations
- Wind-influenced navigation planning
- Coordinate-based path planning with directional constraints
- Region-based target acquisition

---

## 🎒 Extras

This domain is especially useful for:

- Testing numeric planning with coordinate systems
- Evaluating movement strategies with directional speed variations
- Benchmarking region-based goal achievement algorithms
- Modeling real-world scenarios where movement speed depends on environmental factors
