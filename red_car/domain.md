# 🚗 RedCar Domain (PDDL)

The **RedCar Domain** is a grid-based planning domain inspired by the classic Rush Hour puzzle. In this domain, vehicles (cars and trucks) are placed on a 6×6 grid and must be moved according to specific movement rules until the red car reaches an exit position. This domain is designed for evaluating numeric planners and heuristic search methods in grid-based scenarios.

---

## 📂 Domain Overview

### Objects

- **Vehicles:**
  - **Horizontal Cars** (`horizontalCar`): Represent vehicles that can move left or right and typically occupy 2 consecutive grid cells.
  - **Vertical Cars** (`verticalCar`): Represent vehicles that can move up or down and also typically occupy 2 consecutive cells.
  - **Horizontal Trucks** (`horizontalTruck`): Represent trucks that move laterally over 3 consecutive cells.
  - **Vertical Trucks** (`verticalTruck`): Represent trucks that move vertically over 3 consecutive cells.

- **Positions:**
  - Individual grid cells are modeled as objects (e.g., `p0`, `p1`, ..., `p5`).
  - Each cell is mapped to numeric coordinates by the functions:
    - `(pos-cell-x ?p)` and `(pos-cell-y ?p)`

---

## 🧮 Domain Type: Simple Numeric Task (SNT)

This domain is classified as a **Simple Numeric Task (SNT)** because:
- All numeric fluents (such as vehicle positions and cost) are updated using **constant increase** or **decrease** operations.
- Numerical preconditions involve only **simple arithmetic expressions** (e.g., adding or subtracting a constant).
- There are no complex linear equations or functions combining multiple fluents.

Alternate classifications such as **Restricted Linear (RL)** or **Linear Task (LT)** could be considered if more complex numeric operations were used. In this domain, however, the operations remain simple and constant-based.

---

## ⚙️ Domain Mechanics

### Functions & Fluents

- **Vehicle Position Functions:**
  - `(pos-x ?v - vehicle)`: Returns the X coordinate of a vehicle.
  - `(pos-y ?v - vehicle)`: Returns the Y coordinate of a vehicle.

- **Grid Boundary Functions:**
  - `(min_x)`, `(max_x)`, `(min_y)`, `(max_y)`: Define the grid's numerical limits.

- **Cell Mapping Functions:**
  - `(pos-cell-x ?p - position)`: Maps a cell object to its numeric X coordinate.
  - `(pos-cell-y ?p - position)`: Maps a cell object to its numeric Y coordinate.

- **Cost Tracking:**
  - `(total-cost)`: A numeric fluent that accumulates the movement cost.

### Predicates

- **Cell Occupancy:**
  - `(clear ?p1 ?p2 - position)`: A Boolean predicate indicating whether a grid cell is free. By default, a cell is false (occupied) unless explicitly declared clear in the `:init` section.

---

## ⚙️ Actions

Below are the primary movement actions defined in the domain, with sample PDDL-style definitions outlining their preconditions and effects.

### Horizontal Car Actions

#### ➕ `move-car-right`
<pre>
(:action move-car-right
  :parameters (?c - horizontalCar ?targetCell - position ?row - position)
  :precondition (and
    ; The cell two positions to the right of the car must be within the grid
    (< (pos-cell-x ?targetCell) (max_x))
    ; The row of the target cell must match the car's current row
    (= (pos-cell-y ?row) (pos-y ?c))
    ; The target cell must be clear
    (clear ?targetCell ?row)
  )
  :effect (and
    ; Free the leftmost cell (i.e., the current tail cell of the car)
    (clear (pos-x ?c) (pos-y ?c))
    ; Mark the target cell as occupied
    (not (clear ?targetCell ?row))
    ; Update the car's x-coordinate (move right by 1)
    (increase (pos-x ?c) 1)
    ; Increment total-cost by 1
    (increase (total-cost) 1)
  )
)
</pre>

#### ➖ `move-car-left`
<pre>
(:action move-car-left
  :parameters (?c - horizontalCar ?targetCell - position ?row - position)
  :precondition (and
    ; Ensure the target cell (to the left) is within grid bounds
    (> (pos-cell-x ?targetCell) (min_x))
    ; The row of the target cell must match the car's current row
    (= (pos-cell-y ?row) (pos-y ?c))
    ; The target cell is clear
    (clear ?targetCell ?row)
  )
  :effect (and
    ; Free the rightmost cell (the tail of the car)
    (clear (pos-x ?c) (pos-y ?c))
    ; Occupy the target cell
    (not (clear ?targetCell ?row))
    ; Decrease the car's x-coordinate by 1 (move left)
    (decrease (pos-x ?c) 1)
    ; Increment total-cost by 1
    (increase (total-cost) 1)
  )
)
</pre>

### Vertical Car Actions

#### ⬆ `move-car-up`
<pre>
(:action move-car-up
  :parameters (?c - verticalCar ?targetCell - position ?col - position)
  :precondition (and
    ; Check that the target cell (above the car) is within the grid boundary
    (> (pos-cell-y ?targetCell) (min_y))
    ; The column of the target cell must be the same as the car's current column
    (= (pos-cell-x ?col) (pos-x ?c))
    ; The target cell must be clear
    (clear ?col ?targetCell)
  )
  :effect (and
    ; Free the bottom cell that the car is leaving
    (clear (pos-x ?c) (pos-y ?c))
    ; Mark the target cell as occupied
    (not (clear ?col ?targetCell))
    ; Decrease the car's y-coordinate by 1 (move up)
    (decrease (pos-y ?c) 1)
    ; Increase the total-cost by 1
    (increase (total-cost) 1)
  )
)
</pre>

#### ⬇ `move-car-down`
<pre>
(:action move-car-down
  :parameters (?c - verticalCar ?targetCell - position ?col - position)
  :precondition (and
    ; Ensure the target cell (below the car) is within the grid boundary
    (< (pos-cell-y ?targetCell) (max_y))
    ; The column of the target cell must match the car's current column
    (= (pos-cell-x ?col) (pos-x ?c))
    ; The target cell must be clear
    (clear ?col ?targetCell)
  )
  :effect (and
    ; Free the top cell that the car is leaving
    (clear (pos-x ?c) (pos-y ?c))
    ; Mark the target cell as occupied
    (not (clear ?col ?targetCell))
    ; Increase the car's y-coordinate by 1 (move down)
    (increase (pos-y ?c) 1)
    ; Increase the total-cost by 1
    (increase (total-cost) 1)
  )
)
</pre>

### Truck Actions

For trucks (which typically span 3 consecutive cells), the actions are analogous but operate on groups of cells. For example:

#### ➕ `move-truck-right`
<pre>
(:action move-truck-right
  :parameters (?t - horizontalTruck ?newCell - position ?row - position)
  :precondition (and
    ; The new cell at the truck’s right extreme must be within grid bounds
    (< (pos-cell-x ?newCell) (max_x))
    ; The target row must match the truck's current row
    (= (pos-cell-y ?row) (pos-y ?t))
    ; The target cell is clear
    (clear ?newCell ?row)
  )
  :effect (and
    ; Free the leftmost cell the truck previously occupied
    (clear (pos-x ?t) (pos-y ?t))
    ; Mark the new rightmost cell as occupied
    (not (clear ?newCell ?row))
    ; Increase the truck's x-coordinate by 1
    (increase (pos-x ?t) 1)
    (increase (total-cost) 1)
  )
)
</pre>

#### ➖ `move-truck-left`
<pre>
(:action move-truck-left
  :parameters (?t - horizontalTruck ?newCell - position ?row - position)
  :precondition (and
    ; Ensure the new cell at the truck's left extreme is within grid bounds
    (> (pos-cell-x ?newCell) (min_x))
    ; The target row must match the truck's current row
    (= (pos-cell-y ?row) (pos-y ?t))
    ; The new left cell is clear
    (clear ?newCell ?row)
  )
  :effect (and
    ; Free the rightmost cell of the truck
    (clear (pos-x ?t) (pos-y ?t))
    ; Mark the new left cell as occupied
    (not (clear ?newCell ?row))
    ; Decrease the truck's x-coordinate by 1
    (decrease (pos-x ?t) 1)
    (increase (total-cost) 1)
  )
)
</pre>

#### ⬆ `move-truck-up`
<pre>
(:action move-truck-up
  :parameters (?t - verticalTruck ?newCell - position ?col - position)
  :precondition (and
    ; The new cell at the truck’s top extreme must be within grid bounds
    (> (pos-cell-y ?newCell) (min_y))
    ; The target column must match the truck’s current column
    (= (pos-cell-x ?col) (pos-x ?t))
    ; The new top cell is clear
    (clear ?col ?newCell)
  )
  :effect (and
    ; Free the bottom cell the truck previously occupied
    (clear (pos-x ?t) (pos-y ?t))
    ; Mark the new top cell as occupied
    (not (clear ?col ?newCell))
    ; Decrease the truck's y-coordinate by 1
    (decrease (pos-y ?t) 1)
    (increase (total-cost) 1)
  )
)
</pre>

#### ⬇ `move-truck-down`
<pre>
(:action move-truck-down
  :parameters (?t - verticalTruck ?newCell - position ?col - position)
  :precondition (and
    ; The new cell at the truck's bottom extreme must be within grid bounds
    (< (pos-cell-y ?newCell) (max_y))
    ; The target column must match the truck's current column
    (= (pos-cell-x ?col) (pos-x ?t))
    ; The new bottom cell is clear
    (clear ?col ?newCell)
  )
  :effect (and
    ; Free the top cell the truck previously occupied
    (clear (pos-x ?t) (pos-y ?t))
    ; Mark the new bottom cell as occupied
    (not (clear ?col ?newCell))
    ; Increase the truck's y-coordinate by 1
    (increase (pos-y ?t) 1)
    (increase (total-cost) 1)
  )
)
</pre>

---

## 🔍 What the Planner Tries to Do

In each case, the planner is required to:
- Verify that the target cell or group of cells is within grid boundaries.
- Ensure that the target cell(s) is clear.
- Move the vehicle by updating its numeric positions (via an increase or decrease).
- Update the overall cost (using a constant increment).

The planner's task is to chain together a sequence of such actions until the goal state is reached (typically, the red car reaches the exit).

---

## 🎒 Extras

This domain type is classified as a **Simple Numeric Task (SNT)** because:
- The only arithmetic performed in preconditions and effects is constant addition or subtraction.
- No complex linear combinations of numeric fluents are used.
- The domain is both efficient and straightforward for numeric planners to handle.

Alternate classifications:
- **Restricted Linear (RL)** or **Linear Task (LT)** would apply if more complex arithmetic or linear constraints were involved.
- In this domain, however, the operations are simple enough to be classified as **SNT**.

---
