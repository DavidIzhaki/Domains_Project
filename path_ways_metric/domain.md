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

## 🧪 Actions

### ✅ `choose`

Marks a simple molecule as chosen and no longer possible.

```lisp
(:action choose
 :parameters (?x - simple)
 :precondition (and (possible ?x))
 :effect (and
   (chosen ?x)
   (not (possible ?x))
   (increase (num-subs) 1)))
```

---

### 🧫 `initialize`

Adds 1 unit of availability for a molecule after it was chosen.

```lisp
(:action initialize
 :parameters (?x - simple)
 :precondition (and (chosen ?x))
 :effect (and
   (increase (available ?x) 1)))
```

---

### 🔬 `associate`

Consumes two molecules to produce a complex one.

```lisp
(:action associate
 :parameters (?x1 ?x2 - molecule ?x3 - complex)
 :precondition (and
   (>= (available ?x1) (need-for-association ?x1 ?x2 ?x3))
   (>= (available ?x2) (need-for-association ?x2 ?x1 ?x3))
   (association-reaction ?x1 ?x2 ?x3))
 :effect (and
   (decrease (available ?x1) (need-for-association ?x1 ?x2 ?x3))
   (decrease (available ?x2) (need-for-association ?x2 ?x1 ?x3))
   (increase (available ?x3) (prod-by-association ?x1 ?x2 ?x3))))
```

---

### ⚗️ `associate-with-catalyze`

Same as `associate`, but for catalyzed reactions.

```lisp
(:action associate-with-catalyze
 :parameters (?x1 ?x2 - molecule ?x3 - complex)
 :precondition (and
   (>= (available ?x1) (need-for-catalyzed-association ?x1 ?x2 ?x3))
   (>= (available ?x2) (need-for-catalyzed-association ?x2 ?x1 ?x3))
   (catalyzed-association-reaction ?x1 ?x2 ?x3))
 :effect (and
   (decrease (available ?x1) (need-for-catalyzed-association ?x1 ?x2 ?x3))
   ;; (x2 is consumed and then re-increased — effectively a catalyst)
   ;(decrease (available ?x2) (need-for-catalyzed-association ?x2 ?x1 ?x3))
   ;(increase (available ?x2) (need-for-catalyzed-association ?x2 ?x1 ?x3))
   (increase (available ?x3) (prod-by-catalyzed-association ?x1 ?x2 ?x3))))
```

---

### 🧪 `self-associate-with-catalyze`

Catalyzed self-association of a molecule into a complex.

```lisp
(:action self-associate-with-catalyze
 :parameters (?x1 - molecule ?x3 - complex)
 :precondition (and
   (>= (available ?x1) (need-for-catalyzed-self-association ?x1 ?x3))
   (catalyzed-self-association-reaction ?x1 ?x3))
 :effect (and
   (decrease (available ?x1) (need-for-catalyzed-self-association ?x1 ?x3))
   (increase (available ?x3) (prod-by-catalyzed-self-association ?x1 ?x3))))
```

---

### 🧬 `synthesize`

Synthesizes one molecule from another.

```lisp
(:action synthesize
 :parameters (?x1 ?x2 - molecule)
 :precondition (and
   (>= (available ?x1) (need-for-synthesis ?x1 ?x2))
   (synthesis-reaction ?x1 ?x2))
 :effect (and
   ;; (x1 is used and then restored — acting like a catalyst)
   ;(decrease (available ?x1) (need-for-synthesis ?x1 ?x2))
   ;(increase (available ?x1) (need-for-synthesis ?x1 ?x2))
   (increase (available ?x2) (prod-by-synthesis ?x1 ?x2))))
```

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

## 🧩 Notes

- This domain **ignores time** (a-temporal).
- Originally appeared in **IPC-5** under a different name, now refactored to fit SNT numeric planning formats.
- Extended from academic benchmarks, suitable for both theoretical and practical numeric planning tests.
