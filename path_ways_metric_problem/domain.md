# 🧬 Pathways-Metric Domain (PDDL)

The **Pathways-Metric** domain models the problem of **biochemical pathway synthesis** — finding a sequence of **chemical reactions** to create complex molecules from simpler ones. It captures molecular associations, catalyzed reactions, and synthesis steps.

Originally based on the **IPC-5 "Pathways ComplexPreferences"** domain, this version comes from:

> Coles, Amanda, M. Fox, and D. Long.  
> *"A hybrid LP-RPG heuristic for modelling numeric resource flows in planning."*  
> Journal of Artificial Intelligence Research 46 (2013): 343–412.

This domain is ideal for evaluating **numeric resource flows**, especially in biological and chemical contexts.

---

## 📂 Domain Overview

### Objects

- **Molecules**
  - `simple`: basic molecules (e.g., precursors)
  - `complex`: synthesized results of reactions

- **Levels** (optional typing in some extensions)

---

### 🧮 Domain Type: Simple Numeric Task (SNT)

This domain qualifies as a **Simple Numeric Task (SNT)**:
- Effects use only constant `increase` / `decrease` operations.
- No arithmetic expressions in preconditions.
- No use of functions combining multiple fluents.

This makes it compatible with many numeric planners, and ideal for testing **resource flow heuristics**.

---

## ⚙️ Domain Mechanics

### Predicates

- `(association-reaction ?x1 ?x2 ?x3)`  
- `(catalyzed-association-reaction ?x1 ?x2 ?x3)`  
- `(catalyzed-self-association-reaction ?x1 ?x3)`  
- `(synthesis-reaction ?x1 ?x2)`  
- `(possible ?x)` – a candidate simple molecule  
- `(chosen ?x)` – a molecule selected for the pathway  

---

### Functions

- `(available ?molecule)` – how much of a molecule is currently available
- `(num-subs)` – number of substances selected
- Reaction-specific costs and products, e.g.:
  - `(need-for-association ...)`, `(prod-by-synthesis ...)`
  - `(duration-...)` (declared but not used in effects)

---

### 🧪 Actions

#### ✅ `choose`

Marks a `simple` molecule as chosen and increments `num-subs`.

#### 🧫 `initialize`

Adds 1 unit of availability for a chosen molecule.

#### 🔬 `associate`

Consumes molecules `?x1` and `?x2` to create a complex `?x3`.

#### ⚗️ `associate-with-catalyze`

Like `associate`, but with a catalyzed variant.

#### 🧪 `self-associate-with-catalyze`

Uses a single molecule to produce a complex version of itself with a catalyst.

#### 🧬 `synthesize`

Produces one molecule from another via a synthesis reaction.

---

## 🎯 Planning Objective

The planner’s job is to:

- Select valid precursor molecules (`choose`, `initialize`)
- Execute legal chemical reactions to transform and combine them
- Reach a state where the required **target molecules** are available in sufficient quantity

This models real-world biological pathway design and is used to simulate **biochemical synthesis chains**.

---

## 🧾 Example Use Cases

- **Pathway planning in synthetic biology**
- **Testing numeric heuristic planners**
- **Biological modeling of molecular systems**
- **Teaching chemical reaction modeling with planning**

---

## 🧪 Example Instance (Conceptual)

Initial State:
- `(possible mol-A)`
- `(association-reaction mol-A mol-B mol-C)`

Goal:
- `(>= (available mol-C) 1)`

Plan:
1. `choose mol-A`
2. `initialize mol-A`
3. `associate mol-A mol-B mol-C`

---

## 🧩 Notes

- This domain **ignores time** (a-temporal).
- Originally appeared in **IPC-5** under a different name, now refactored to fit SNT numeric planning formats.
- Extended from academic benchmarks, suitable for both theoretical and practical numeric planning tests.
