# 🌾 Farmland Domain (PDDL)

The **Farmland Domain** models the allocation of manpower across farms. The objective is to **maximize a numeric benefit** (captured via a metric fluent) by **moving workers** between farms under adjacency and capacity constraints.

This domain was introduced in:

> Scala, Enrico, Haslum, Patrik, Thiébaux, Sylvie, and Ramirez, Miquel.  
> *Subgoaling techniques for satisficing and optimal numeric planning.*  
> Journal of Artificial Intelligence Research 68 (2020): 691–752.  
> ([Link](https://jair.org/index.php/jair/article/view/11343))

It is useful for testing:
- **Numeric planning** with flowing resource quantities
- **Satisficing and optimal search** under numeric constraints
- **Local transfer actions** subject to adjacency

---

## 📂 Domain Overview

### Objects

- **Farms** (`farm`): Represented as nodes in a graph, each with a numeric resource `x` representing available workers.

---

## 📌  Domain Type: Simple Numeric Planning (SNP)

This domain includes:

**Preconditions** involving:
- **Predicates** and **constant-based numeric constraints**:
```lisp
(adj ?f1 ?f2)
(>= (x ?f1) 4)
```

**Effects** are **constant updates** to numeric fluents:
```lisp
(decrease (x ?f1) 4)
(increase (x ?f2) 2)
(increase (cost) 1)
```

**Goals** contain **linear numeric expressions**, for example:
```lisp
(>= (+ (* 1.0 (x farm0)) (+ (* 1.7 (x farm1)) 0)) 840.0)
```

> This is a linear goal comparing a weighted sum of fluents to a constant.

Since the domain uses **constant effects**, **constant/predicate preconditions**, and **linear goal expressions**, it is classified as **SNP (Simple Numeric Planning)**.

---

## ➕ Predicates

- `(adj ?f1 ?f2)`  
  Indicates adjacency between two farms. This governs whether workers can move between farms.

---

## 🔢 Functions

- `(x ?f - farm)`  
  The number of workers currently assigned to farm `?f`.

- `(cost)`  
  The total cost accumulated through movement actions.

---

## ⚙️ Actions

### 🔸 `move-fast`
Moves **4 workers out** of a farm and sends **2 to a neighbor**, representing a fast, but lossy transfer.

- **Parameters**: `?f1 ?f2 - farm`
- **Preconditions**:
  - `?f1 ≠ ?f2`
  - `?f1` has at least 4 workers
  - `?f1` and `?f2` are adjacent
- **Effects**:
  - Decrease `x(?f1)` by 4
  - Increase `x(?f2)` by 2
  - Increase `(cost)` by 1

---

### 🔹 `move-slow`
Moves **1 worker** from one farm to another, fully conserved.

- **Parameters**: `?f1 ?f2 - farm`
- **Preconditions**:
  - `?f1 ≠ ?f2`
  - `?f1` has at least 1 worker
  - `?f1` and `?f2` are adjacent
- **Effects**:
  - Decrease `x(?f1)` by 1
  - Increase `x(?f2)` by 1
  - Increase `(cost)` by 1

---

## 🛠 Changes

We made the following modification to the original domain:

- **Added a cost of 1 to the `move-slow` action**, to align it with the cost structure of `move-fast` and enable cost-based optimization.  
  This change affects the `(cost)` fluent by incrementing it whenever `move-slow` is applied.

---

## 📧 Attribution

Created by:
- Enrico Scala (<enricos83@gmail.com>)
- Miquel Ramirez (<miquel.ramirez@gmail.com>)

Please cite their 2020 JAIR paper if using this domain in academic research.
