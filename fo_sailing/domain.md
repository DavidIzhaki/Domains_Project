# ⛵ FO Sailing Problem Domain (PDDL)

The **FO Sailing Problem Domain** is an extended version of the classical Sailing domain. It models a scenario where boats navigate a 2D grid to save people while managing their speed and direction. This extension introduces **first-order control** over acceleration and deceleration, allowing boats to move more or less in a single action. The domain is designed to test **linear numeric planning** and **effect abstraction**.

This domain is particularly useful for testing:
- **First-order numeric control** (e.g., acceleration and deceleration)
- **Linear numeric planning**
- **Path optimization with velocity constraints**

---

## 📂 Domain Overview

### Objects

- **Boats**: Represent vessels that navigate the grid to save people.
- **Persons**: Represent individuals who need to be rescued.

---

## 🧮 Domain Type: Linear Task (LT)

This domain is classified as a **Linear Task (LT)** because it uses **linear arithmetic expressions** in both preconditions and effects. 

### Example:
```pddl
(increase (x ?b) (* (v ?b) 1.5))

```

This effect involves the multiplication of a constant (1.5) with a variable (v ?b), which is characteristic of LT domains. Such operations are permitted in LT domains but disallowed in more restrictive types like Simple Numeric Tasks (SNT).

The domain also includes other linear numeric effects, such as:
```pddl
(decrease (x ?b) (* (v ?b) 2))

```

These effects demonstrate that the domain relies on linear arithmetic operations for movement and velocity control, further classifying it as a Linear Task (LT).

## ⚙️ Domain Mechanics

### Predicates
- (saved ?t - person) — Indicates whether a person has been rescued.

---

### Functions

- (x ?b - boat) — The x-coordinate of a boat.
- (y ?b - boat) — The y-coordinate of a boat.
- (v ?b - boat) — The velocity of a boat.
- (d ?t - person) — The difficulty or distance threshold for saving a person.


### ⚙️ Actions

#### ↗️ go_north_east

<pre> 
(:action go_north_east :parameters (?b - boat) :precondition (and (not (dummy))) :effect (and (increase (x ?b) (* (v ?b) 1.5)) (increase (y ?b) (* (v ?b) 1.5)))) 
</pre>


#### Description:

Moves a boat diagonally northeast, increasing both x and y coordinates proportionally to its velocity.

#### ↖️ go_north_west

<pre>
 (:action go_north_west :parameters (?b - boat) :precondition (and (not (dummy))) :effect (and (decrease (x ?b) (* (v ?b) 1.5)) (increase (y ?b) (* (v ?b) 1.5)))) 
 </pre>

#### Description:

Moves a boat diagonally northwest, decreasing x and increasing y coordinates proportionally to its velocity.

#### ➡️ go_est
<pre>
 (:action go_est :parameters (?b - boat) :precondition (and (not (dummy))) :effect (and (increase (x ?b) (* (v ?b) 3)))) 
 </pre>

#### Description:

Moves a boat eastward, increasing the x coordinate proportionally to its velocity.

#### ⬅️ go_west
<pre>
 (:action go_west :parameters (?b - boat) :precondition (and (not (dummy))) :effect (and (decrease (x ?b) (* (v ?b) 3)))) 
 </pre>

#### Description:

Moves a boat westward, decreasing the x coordinate proportionally to its velocity.

#### ↘️ go_south_east
<pre> 
(:action go_south_east :parameters (?b - boat) :precondition (and (not (dummy))) :effect (and (increase (x ?b) (* (v ?b) 2)) (decrease (y ?b) (* (v ?b) 2))))
 </pre>

#### Description:

Moves a boat diagonally southeast, increasing x and decreasing y coordinates proportionally to its velocity.

#### ↙️ go_south_west

<pre>
 (:action go_south_west :parameters (?b - boat) :precondition (and (not (dummy))) :effect (and (decrease (x ?b) (* (v ?b) 2)) (decrease (y ?b) (* (v ?b) 2)))) 
 </pre>

#### Description:

Moves a boat diagonally southwest, decreasing both x and y coordinates proportionally to its velocity.

#### ⬇️ go_south

<pre>
 (:action go_south :parameters (?b - boat) :precondition (and (not (dummy))) :effect (and (decrease (y ?b) (* (v ?b) 2))))
</pre>

#### Description:

Moves a boat southward, decreasing the y coordinate proportionally to its velocity.

#### 🆙 accelerate

<pre>
 (:action accelerate :parameters (?b - boat) :precondition (and (<= (+ (v ?b) 1) 3)) :effect (and (increase (v ?b) 1)))
  </pre>

#### Description:

Increases the velocity of a boat by 1, up to a maximum of 3.

#### 🛑 decelerate

<pre>
 (:action decelerate :parameters (?b - boat) :precondition (and (>= (- (v ?b) 1) 1)) :effect (and (decrease (v ?b) 1))) 
 </pre>

#### Description:

Decreases the velocity of a boat by 1, down to a minimum of 1.

#### 🆘 save_person

<pre>
 (:action save_person :parameters (?b - boat ?t - person) :precondition (and (>= (+ (x ?b) (y ?b)) (d ?t)) (>= (- (y ?b) (x ?b)) (d ?t)) (<= (+ (x ?b) (y ?b)) (+ (d ?t) 25)) (<= (- (y ?b) (x ?b)) (+ (d ?t) 25)) (<= (v ?b) 1)) :effect (and (saved ?t)))
  </pre>

#### Description:

Rescues a person when the boat is within a specific area defined by coordinate constraints and is moving slowly enough (velocity ≤ 1).

## 🔍 What the Planner Tries to Do

The planner must:

- Navigate boats across a 2D coordinate system.
- Manage velocity using acceleration and deceleration actions.
- Satisfy coordinate-based constraints to rescue people.
- Optimize paths to minimize the number of actions required.

---

## 🧾 Example

Suppose:

- Boat b1 starts at coordinates (0,0) with velocity v(b1) = 1.
- Person p1 needs to be rescued with d(p1) = 10.

**Initial state:**

- x(b1) = 0, y(b1) = 0, v(b1) = 1.
- p1 is not saved.

**Goal:**

- p1 is saved.

The planner might decide:

1. Use accelerate (b1) to increase velocity to 2.
2. Use go_north_east (b1) twice to reach (6,6).
3. Use decelerate (b1) to reduce velocity to 1.
4. Use save_person (b1, p1) since (6+6) ≥ 10 and other constraints are satisfied.

---

## 🧪 Example Use Cases

- Maritime search and rescue operations.
- Velocity and direction control in navigation.
- Testing planners' ability to handle first-order numeric effects.
- Evaluating path optimization with velocity constraints.

---

## 🎒 Extras

This domain is especially useful for:

- Benchmarking planners with linear numeric effects.
- Modeling real-world scenarios involving velocity and direction control.
- Testing first-order control in numeric planning.
- Similar code found with 1 license type - View matches