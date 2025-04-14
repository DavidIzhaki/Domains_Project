# 🚜 FO_Farmland Domain (PDDL)

The **FO_Farmland Domain** (a.k.a. `farmland_ln`) extends the original **Farmland Domain** by incorporating **dynamic scaling via numeric parameters**, such as the number of cars used to transport workers. This allows for **variable-capacity movement** and introduces **non-constant numeric effects**, pushing the domain into the **fully observable linear numeric planning** class.

This domain was introduced in:

> Li, Dongxu, Scala, Enrico, Haslum, Patrik, & Bogomolov, Sergiy.  
> *Effect-abstraction based relaxation for linear numeric planning*.  
> In Proceedings of the 27th International Joint Conference on Artificial Intelligence (IJCAI), 2018, pp. 4787–4793.  
> ([Link](https://www.ijcai.org/proceedings/2018/0667.pdf))

It is useful for testing:
- **Advanced numeric reasoning** with parametric effects
- **Action instantiation with dynamic values**
- **Search heuristics that reason about linear multipliers**

---

## 📂 Domain Overview

### Objects

- **Farms** (`farm`): Represent nodes where workers reside and move to/from.

---

## ➕ Predicates

- `(adj ?f1 ?f2)`  
  Indicates adjacency between two farms.

- `(dummy)`  
  A technical placeholder to prevent multiple `hire-car` invocations in trivial settings.

---

## 🔢 Functions

- `(x ?f - farm)`  
  The number of workers currently at farm `?f`.

- `(cost)`  
  The cumulative numeric cost accumulated through movement actions.

- `(num-of-cars)`  
  The number of cars available to perform high-capacity transport.

---

## ⚙️ Actions

### 🚗 `move-by-car`
Moves workers using all available cars. The number of workers moved is `4 × (num-of-cars)` and incurs cost proportional to that amount.

- **Parameters**: `?f1 ?f2 - farm`
- **Preconditions**:
  - `?f1 ≠ ?f2`
  - `?f1` has at least `4 × (num-of-cars)` workers
  - `?f1` and `?f2` are adjacent
- **Effects**:
  - Decrease `x(?f1)` by `4 × (num-of-cars)`
  - Increase `x(?f2)` by `4 × (num-of-cars)`
  - Increase `(cost)` by `0.1 × (4 × num-of-cars)`

---

### 🐢 `move-slow`
Moves 1 worker from one farm to an adjacent one.

- **Parameters**: `?f1 ?f2 - farm`
- **Preconditions**:
  - `?f1 ≠ ?f2`
  - `?f1` has at least 1 worker
  - `?f1` and `?f2` are adjacent
- **Effects**:
  - Decrease `x(?f1)` by 1
  - Increase `x(?f2)` by 1

---

### 🛻 `hire-car`
Increases the number of available cars by 1. Can be used once in some formulations to initialize transport capabilities.

- **Parameters**: *None*
- **Precondition**:
  - `(not (dummy))`
- **Effect**:
  - Increase `(num-of-cars)` by 1

---

## 📌 Domain Type: Linear Task (LT)

This domain is a **Linear Task (LT)** because:
- It uses **linear numeric fluents** and **parameterized expressions**
- Effects include linear multiplications with **external numeric fluents**
- Preconditions may involve linear arithmetic

This makes it a **more expressive** benchmark for planners supporting full linear numeric modeling, such as:
- **DiNo**
- **OPTIC**
- **Metric-FF (limited)**

---

## 📧 Attribution

Created by:
- Enrico Scala (<enricos83@gmail.com>)
- Dongxu Li (<dongxu.li@anu.edu.au>)

Please cite the 2018 IJCAI paper if using this domain in academic research.
