# 🚛 TPP-Metric Domain (PDDL)

The **Travelling Purchase Problem (TPP)** is a generalization of the classic **Travelling Salesman Problem (TSP)**. In this domain, the planner must **visit a set of markets to buy goods** in sufficient quantity, while **minimizing the total cost** — which includes both **travel costs** and **item prices**.

Originally introduced in **IPC-5**, this domain was designed to test **metric optimization**, particularly on real-world-like logistics problems involving multi-variable cost balancing.

> Authors: Alfonso Gerevini and Alessandro Saetti  
> Problem example by Enrico Scala and Miquel Ramirez

---

## 📂 Domain Overview

### Objects

- **Places**:
  - `depot`: Starting and ending point for the truck.
  - `market`: Locations where goods can be purchased.

- **Locatables**:
  - `truck`: Moves between places, carries no physical limit but costs money to drive.
  - `goods`: Products that must be purchased.

---

### 🧮 Domain Type: Restricted Linear (RL)

This domain uses numeric expressions such as:

- `(* (on-sale ?g ?m) (price ?g ?m))`  
- `(- (request ?g) (bought ?g))`

These are **linear terms involving multiple fluents and constants**, which disqualifies it from being a **Simple Numeric Task (SNT)**.

Therefore, it falls under the **Restricted Linear (RL)** category — where:

- Preconditions and effects can contain linear arithmetic over fluents
- Effects include `assign`, `increase`, `decrease` with arithmetic terms
- No conditionals or non-linear combinations are used

This makes it **harder to optimize** but **more expressive** than SNT.

---

## ⚙️ Domain Mechanics

### Predicates

- `(loc ?t - truck ?p - place)`  
  Indicates the current location of the truck.

---

### Functions

- `(price ?g ?m)` – Price of good `g` at market `m`.
- `(on-sale ?g ?m)` – Units of good `g` available at market `m`.
- `(drive-cost ?p1 ?p2)` – Travel cost from `p1` to `p2`.
- `(bought ?g)` – Quantity of good `g` already bought.
- `(request ?g)` – Quantity of good `g` required to fulfill.
- `(total-cost)` – Sum of all costs: travel + purchase.

---

## 🧪 Actions

### 🚚 `drive`

```lisp
(:action drive
 :parameters (?t - truck ?from ?to - place)
 :precondition (and (loc ?t ?from))
 :effect (and
   (not (loc ?t ?from))
   (loc ?t ?to)
   (increase (total-cost) (drive-cost ?from ?to))))
```

---

### 🛒 `buy-allneeded`

```lisp
(:action buy-allneeded
 :parameters (?t - truck ?g - goods ?m - market)
 :precondition (and
   (loc ?t ?m)
   (> (on-sale ?g ?m) 0)
   (> (on-sale ?g ?m) (- (request ?g) (bought ?g))))
 :effect (and
   (decrease (on-sale ?g ?m) (- (request ?g) (bought ?g)))
   (increase (total-cost) (* (- (request ?g) (bought ?g)) (price ?g ?m)))
   (assign (bought ?g) (request ?g))))
```

---

### 🛍️ `buy-all`

```lisp
(:action buy-all
 :parameters (?t - truck ?g - goods ?m - market)
 :precondition (and
   (loc ?t ?m)
   (> (on-sale ?g ?m) 0)
   (<= (on-sale ?g ?m) (- (request ?g) (bought ?g))))
 :effect (and
   (assign (on-sale ?g ?m) 0)
   (increase (total-cost) (* (on-sale ?g ?m) (price ?g ?m)))
   (increase (bought ?g) (on-sale ?g ?m))))
```

---

## 🎯 Planning Objective

The planner must:

- Drive the truck between markets strategically.
- Buy available goods to fulfill all `request` quantities.
- Return the truck to the depot.
- **Minimize total cost**, calculated as:

```
total-cost = ∑ drive-costs + ∑ item-costs
```

---

## 📄 Example Problem (pfile02)

```lisp
(:goal (and
  (>= (bought goods0) (request goods0))
  (>= (bought goods1) (request goods1))
  (loc truck0 depot0)))
(:metric minimize (total-cost))
```

---

## 🧾 Use Cases

- **Benchmarking cost-based planners**
- **Testing numeric heuristic guidance**
- **Realistic supply chain modeling**
- **Hybrid routing + resource planning**

---

## 🧩 Notes

- This domain is **Restricted Linear (RL)**, not SNT.
- It uses numeric `assign`, `increase`, and arithmetic preconditions.
- It does **not model inventory limits**.
- Truck travel is the main routing cost; market selection is a secondary challenge.

