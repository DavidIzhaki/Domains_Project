# 💧 Hydro Power Domain (PDDL)

The **Hydro Power Domain** models a system where hydroelectric reservoirs are used to generate financial gains. The system involves pumping water when energy is cheap, storing it in reservoirs, and selling it when energy prices are higher. The domain is designed to evaluate **resource flow management** and **numeric planning**.

This domain is particularly useful for testing:
- **Numeric resource management**
- **Temporal planning**
- **Optimization of financial gains**

---

## 📂 Domain Overview

### Objects

- **Turn Values**: Represent numeric values associated with energy demand or financial gains.
- **Time**: Represents discrete time points for scheduling actions.
- **Power Stations**: Represent hydroelectric reservoirs or stations.

---

## 🧮 Domain Type: Linear Task (LT)

Since we have effect calculations like:

```lisp
(decrease (funds) (* 1.05 (value ?n1)))

```
that involve 2 numeric fluents this domain qualifies as a **Linear Task (LT)**.

---

## ⚙️ Domain Mechanics

### Predicates

- `(timenow ?t - time)` — Indicates the current time step.
- `(before ?t1 - time ?t2 - time)` — Specifies the temporal order between two time points.
- `(demand ?t - time ?n - turnvalue)` — Indicates the energy demand at a specific time and its associated value.
- `(faultrepair ?t - time)` — Indicates that a fault repair is scheduled at a specific time.
- `(faultrepaired ?t - time)` — Indicates that a fault has been repaired.

---

### Functions

- `(funds)` — Represents the current financial resources.
- `(stored_units)` — Represents the amount of water stored in the reservoir.
- `(stored_capacity)` — Represents the maximum capacity of the reservoir.
- `(value ?n - turnvalue)` — Represents the numeric value associated with a turn value.

---

### ⚙️ Actions

#### ⏩ `advance_time`

<pre>
(:action advance_time
  :parameters (?t1 - time ?t2 - time)
  :precondition (and
    (timenow ?t1)
    (before ?t1 ?t2)
  )
  :effect (and
    (timenow ?t2)
    (not (timenow ?t1))
  )
)
</pre>

Advances the current time step to the next time point.

---

#### 💧 `pump_water_up`

<pre>
(:action pump_water_up
  :parameters (?t1 - time ?n1 - turnvalue)
  :precondition (and
    (timenow ?t1)
    (>= (funds) (* 1.05 (value ?n1)))
    (>= (stored_capacity) 1)
    (demand ?t1 ?n1)
  )
  :effect (and
    (increase (stored_units) 1)
    (decrease (stored_capacity) 1)
    (decrease (funds) (* 1.05 (value ?n1)))
  )
)
</pre>

Pumps water into the reservoir, consuming funds and reducing available capacity.

---

#### ⚡ `generate`

<pre>
(:action generate
  :parameters (?t1 - time ?n1 - turnvalue)
  :precondition (and
    (timenow ?t1)
    (>= (stored_units) 1)
    (demand ?t1 ?n1)
  )
  :effect (and
    (decrease (stored_units) 1)
    (increase (stored_capacity) 1)
    (increase (funds) (value ?n1))
  )
)
</pre>

Generates energy by releasing water from the reservoir, increasing funds.

---

## 🔍 What the Planner Tries to Do

Given:

- A set of time points and energy demands
- Initial funds and stored water capacity
- Numeric constraints on resources

The planner must:

- Optimize financial gains by scheduling actions like `pump_water_up` and `generate`.
- Ensure that actions respect temporal constraints (`before` predicates).
- Avoid exceeding the reservoir's capacity or depleting funds.

---

## 🧾 Example

Suppose the system starts with:

- **Funds**: 1000
- **Stored Capacity**: 3
- **Stored Units**: 0

At time `t0000`, the demand is `n7` with a value of 7. The planner can:

1. Use `pump_water_up` to store water, consuming funds.
2. Use `generate` to release water and increase funds when demand is high.
3. Advance time to the next step and repeat the process.

---

## 🧪 Example Use Cases

- **Energy market optimization**
- **Hydroelectric power management**
- **Temporal planning with numeric constraints**
- **Resource flow modeling in AI planning**

---

## 🎒 Extras

This domain pairs well with:

- **Numeric planners** (e.g. Metric-FF)
- **Temporal planners** (e.g., TFD, POPF)
- **Optimization algorithms** for resource management
