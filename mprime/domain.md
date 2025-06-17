# 🧠 MPrime Domain (PDDL)

The **MPrime Domain** is a numerically extended version of the classic Mystery domain, created for the **First International Planning Competition (IPC-1)**.  
It models the emotional dynamics of agents interacting with consumable resources (foods), where **pleasures**, **pains**, and **cravings** evolve over time.  
This version adds a new action: `drink`, allowing resource transfer between food items — similar to resource flow in a network.

---

## 📂 Domain Overview

### Objects

- **Food**: Consumable items (e.g., `tuna`, `wurst`, `pistachio`, etc.)
- **Emotion**: Abstract emotional entities subdivided into:
  - `pleasure` (e.g., `rest`, `expectation`)
  - `pain` (e.g., `angina`, `depression`)

---

## 🧮 Domain Type: Restricted Numeric Planning (RNP)

This domain includes:

**Preconditions** made up of:
- **Predicates** and
- **Single-variable numeric conditions**:
```lisp
(and
    (craves ?c ?n)
    (craves ?v ?n)
    (>= (harmony ?v) 1)
)
```

**Effects** include a mix of:
- **Propositional changes**, and
- **Constant numeric updates**:
```lisp
(not (fears ?c ?v))
(craves ?c ?n)
(increase (harmony ?v) 1)
```

**Goals** are **purely propositional**:
```lisp
(and (craves depression chicken))
```

Since the domain contains **single-variable numeric constraints**, **constant effects**, and **predicate goals**, it is classified as **RNP (Restricted Numeric Planning)**.

---

## ⚙️ Domain Mechanics

### Predicates

- `(eats ?f1 ?f2)` — Food `f1` can transform into `f2`
- `(craves ?e ?f)` — Emotion `e` craves food `f`
- `(fears ?p ?v)` — Pain `p` fears pleasure `v`

---

### Functions

- `(harmony ?e - emotion)` — A numeric score indicating the balance of emotion `e`
- `(locale ?f - food)` — The quantity of food `f` available (a numeric fluent)

---

## 🛠️ Actions

### ✅ `overcome`

<pre>(:action overcome
  :parameters (?c - pain ?v - pleasure ?n - food)
  :precondition (and (craves ?c ?n)
                     (craves ?v ?n)
                     (>= (harmony ?v) 1))
  :effect (and (not (craves ?c ?n))
               (fears ?c ?v)
               (decrease (harmony ?v) 1))
)</pre>

**Description**:  
A pleasure helps overcome a pain by sacrificing one harmony unit, removing the pain’s craving and causing fear toward that pleasure.

---

### 🍽️ `feast`

<pre>(:action feast
  :parameters (?v - pleasure ?n1 ?n2 - food)
  :precondition (and (craves ?v ?n1)
                     (eats ?n1 ?n2)
                     (>= (locale ?n1) 1))
  :effect (and (not (craves ?v ?n1))
               (craves ?v ?n2)
               (decrease (locale ?n1) 1))
)</pre>

**Description**:  
A pleasure entity consumes `n1`, gains craving for the resulting `n2`, and reduces the stock of `n1`.

---

### 💀 `succumb`

<pre>(:action succumb
  :parameters (?c - pain ?v - pleasure ?n - food)
  :precondition (and (fears ?c ?v)
                     (craves ?v ?n))
  :effect (and (not (fears ?c ?v))
               (craves ?c ?n)
               (increase (harmony ?v) 1))
)</pre>

**Description**:  
Pain gives in to pleasure, stops fearing it, and adopts the pleasure's craving. The harmony of the pleasure increases.

---

### 💧 `drink`

<pre>(:action drink
  :parameters (?n1 ?n2 - food)
  :precondition (>= (locale ?n1) 1)
  :effect (and (decrease (locale ?n1) 1)
               (increase (locale ?n2) 1))
)</pre>

**Description**:  
Transfers one unit of food from `n1` to `n2`. Enables dynamic resource redistribution.

---

## 🔍 What the Planner Tries to Do

Given an initial emotional state, food availability, cravings, and harmony levels, the planner must:

- Decide which emotions to satisfy first
- Manage harmony costs and benefits
- Transfer and transform food resources (via `drink`, `feast`)
- Eliminate cravings and fear relations while satisfying the goal

---

## 🧪 Example Use Cases

- Emotion simulation: Modeling how agents respond to resources and emotions
- Resource-based planning: Tracking and transforming food quantities
- Flow dynamics: Using the `drink` action for transfer across food nodes

---

## 🎒 Extras

This domain is great for testing:

- Numeric precondition handling
- Causal reasoning through emotions
- Linear numeric effect propagation
- Planning over emotional and resource-based dependencies

---
