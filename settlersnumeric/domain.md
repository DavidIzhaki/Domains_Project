# 🏗️ Settlers Numeric Domain (PDDL)

The Settlers Numeric Domain models a resource management and construction scenario where players develop settlements by gathering resources, building structures, and establishing transportation networks. This domain features complex resource dependencies, location-based constraints, and multiple transportation options.

Originally introduced by **Maria Fox and Derek Long** in IPC-3, this domain tests planners' ability to handle **numeric fluents**, **conditional effects**, and **complex resource management**.

---

## 📂 Domain Overview

### Objects

- **Places**: Locations with specific properties (e.g., woodland, mountain)
- **Vehicles**: Transportation units (carts, trains, ships) for moving resources
- **Resources**: Materials like wood, timber, ore, stone, iron, and coal

---

## 🧮 Domain Type: Linear Task (LT)

This domain qualifies as a **Linear Task (LT)** because it includes:

- Numeric fluents with complex dependencies  
- Resource consumption and production  
- Conditional effects based on resource availability  
- Linear arithmetic in preconditions and effects  

These features make it more expressive than SNT or RT domains, requiring planners that can handle linear numeric expressions.

---

## ⚙️ Domain Mechanics

### Predicates

```lisp
(connected-by-land ?p1 ?p2)
(connected-by-rail ?p1 ?p2)
(connected-by-sea ?p1 ?p2)
(woodland ?p)
(mountain ?p)
(metalliferous ?p)
(by-coast ?p)
(has-cabin ?p)
(has-coal-stack ?p)
(has-quarry ?p)
(has-mine ?p)
(has-sawmill ?p)
(has-ironworks ?p)
(has-docks ?p)
(has-wharf ?p)
(is-train ?v)
(is-ship ?v)
(is-at ?v ?p)
(potential ?v)

```

### Functions

```lisp

(available ?r ?s)
(space-in ?v)
(carts-at ?l)
(labour)
(resource-use)
(pollution)
(housing ?p)

```

## 🛠️ Actions

### 📦 `load`
Loads a resource from a place into a vehicle, consuming space and labor.

### 📤 `unload`
Unloads a resource from a vehicle to a place, freeing space and consuming labor.

### 🚚 `move-empty-cart`
Moves an empty cart between connected places, consuming labor.

### 🚛 `move-laden-cart`
Moves a cart with a resource between connected places, transferring the resource and consuming labor.

### 🚂 `move-train`
Moves a train between rail-connected places, consuming coal and generating pollution.

### 🚢 `move-ship`
Moves a ship between sea-connected places, consuming more coal and generating more pollution than trains.

---

## 🏗️ Construction Actions

### 🏠 `build-cabin`
Builds a cabin at a woodland location, consuming labor.

### ⛏️ `build-quarry`
Builds a quarry at a mountain location, consuming labor.

### 🏭 `build-coal-stack`
Builds a coal stack at any location with timber, consuming timber and labor.

### 🪚 `build-sawmill`
Builds a sawmill at any location with timber, consuming timber and labor.

### ⛰️ `build-mine`
Builds a mine at a metalliferous location, consuming wood and labor.

### 🔨 `build-ironworks`
Builds ironworks at a location with wood and stone, consuming both and labor.

### 🚢 `build-docks`
Builds docks at a coastal location, consuming wood, stone, and labor.

### 🛳️ `build-wharf`
Builds a wharf at a location with docks, consuming iron, stone, and labor.

### 🛤️ `build-rail`
Builds a rail connection between land-connected places, consuming wood, iron, and labor.

### 🏘️ `build-house`
Builds a house, increasing housing and consuming wood and stone.

### 🛒 `build-cart`
Builds a cart, consuming timber and labor.

### 🚂 `build-train`
Builds a train, consuming iron and labor. The train is initialized with zeroed resources and space.

### 🚢 `build-ship`
Builds a ship at a wharf location, consuming iron and labor. The ship is initialized with zeroed resources and space.

---

## 🔁 Resource Processing Actions

### 🌲 `fell-timber`
Harvests timber at a location with a cabin, consuming labor.

### 🪨 `break-stone`
Extracts stone at a location with a quarry, consuming labor and increasing resource use.

### ⛏️ `mine-ore`
Extracts ore at a location with a mine, consuming labor and increasing resource use.

### 🔥 `burn-coal`
Converts timber to coal at a location with a coal stack, generating pollution.

### 🪚 `saw-wood`
Converts timber to wood at a location with a sawmill.

### ⚒️ `make-iron`
Converts ore and coal to iron at a location with ironworks, generating pollution.

---

## 🔍 What the Planner Tries to Do

The planner must:

- Gather raw resources (timber, ore) from appropriate locations
- Process those resources into refined materials (wood, coal, iron)
- Build infrastructure (cabins, sawmills, mines, etc.)
- Construct transportation networks (carts, trains, ships, rails)
- Transport resources between locations efficiently
- Build housing to meet settlement requirements
- Manage pollution and resource consumption

All while **minimizing**:

- `(labour)`
- `(resource-use)`
- `(pollution)`

---

## 🧾 Example

### Scenario

- `location0` is woodland  
- `location1` is by the coast  
- **Goal**: Build a house at `location1`

### Initial State

- No resources or structures available

### Strategy

1. Build a cabin at `location0`
2. Fell timber at `location0`
3. Build a cart at `location0`
4. Move the laden cart with timber to `location1`
5. Build a quarry at a mountain location
6. Break stone and transport it to `location1`
7. Saw wood from timber at `location1`
8. Build a house at `location1` using wood and stone

---

## 🧪 Example Use Cases

- Supply chain and logistics planning  
- Resource management under constraints  
- Infrastructure development simulation  
- Environmental impact assessment  
- Multi-modal transportation planning  

---

## 🎒 Extras

This domain is especially useful for:

- Testing planners with complex resource dependencies  
- Evaluating numeric planning capabilities  
- Benchmarking optimization with multiple metrics  
- Modeling real-world construction and development scenarios  

