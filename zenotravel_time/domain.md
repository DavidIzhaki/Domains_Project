# Zenotravel Domain (Extended Version)

This document describes the **Zenotravel domain**, extended to tracking only **total-time** for flight durations.


## Overview

The **Zenotravel domain** models air travel with constraints on fuel consumption and passenger capacity. In this extended version, new **functions** and **actions** have been added to track **flight durations**, enabling more detailed planning and optimization based solely on travel time.


## Key Features & Changes

### 1. New Functions
To account for flight duration, the following functions were added:

- **`total-time`** → Tracks the total cumulative travel time.
- **`slow-speed`** → Defines the speed of an aircraft during slow flights.
- **`fast-speed`** → Defines the speed of an aircraft during fast flights.

### 2. Updated Actions

#### **Fly-Slow (`fly-slow`)**
- Moves an aircraft from one city to another.
- Consumes fuel based on the `slow-burn` rate.
- **NEW**: Increases `total-time` based on the distance and `slow-speed`.

#### **Fly-Fast (`fly-fast`)**
- Moves an aircraft from one city to another.
- Consumes fuel based on the `fast-burn` rate.
- **NEW**: Increases `total-time` based on the distance and `fast-speed`.
- Restricted by the `zoom-limit` (passenger capacity for fast travel).


## Predicates
These define the state of the world:

- **`located(?x - locatable, ?c - city)`** → Defines the location of an object.
- **`in(?p - person, ?a - aircraft)`** → Indicates that a person is inside an aircraft.


## Functions
These numerical functions track fuel levels, distances, and time:

- **`fuel(?a - aircraft)`** → Current fuel level of an aircraft.
- **`distance(?c1 - city, ?c2 - city)`** → Distance between two cities.
- **`slow-burn(?a - aircraft)`** → Fuel consumption rate during slow flights.
- **`fast-burn(?a - aircraft)`** → Fuel consumption rate during fast flights.
- **`capacity(?a - aircraft)`** → Maximum fuel capacity.
- **`total-time`** → **(New!)** Tracks cumulative travel time.
- **`onboard(?a - aircraft)`** → Number of passengers in an aircraft.
- **`zoom-limit(?a - aircraft)`** → Maximum passengers allowed for fast flights.
- **`slow-speed(?a - aircraft)`** → **(New!)** Speed of an aircraft during slow flights.
- **`fast-speed(?a - aircraft)`** → **(New!)** Speed of an aircraft during fast flights.


## Actions

### 1. Boarding & Debarking
- **Board (`board`)** → A person enters an aircraft.
- **Debark (`debark`)** → A person exits an aircraft.

### 2. Flight Actions

#### **Fly-Slow (`fly-slow`)**
- Moves an aircraft between cities.
- Consumes fuel based on `slow-burn`.
- **NEW**: Updates `total-time` based on `slow-speed`.

#### **Fly-Fast (`fly-fast`)**
- Moves an aircraft between cities.
- Consumes fuel based on `fast-burn`.
- **NEW**: Updates `total-time` based on `fast-speed`.
- Restricted by `zoom-limit` (passenger capacity).

### 3. Refueling
- **Refuel (`refuel`)** → Restores fuel to an aircraft's capacity.

 ## Domain Type: Linear Task (LT) 
 This domain models fuel consumption and movement in air travel using **numeric fluents** and **linear arithmetic expressions**. It qualifies as a **Linear Task (LT)** due to the following characteristics: 
 - ✅ Uses **numeric fluents** such as `fuel`, `onboard`, and `fuel-used` 
 - ✅ Includes **linear preconditions** involving static functions like `distance` and `burn rate`, e.g., `(>= (fuel ?a) (* (slow-burn ?a) (distance ?c1 ?c2)))` 
 - ✅ Numeric effects use `increase` and `decrease` with **linear expressions** based on static terms (e.g., `(increase (fuel-used) (* (slow-burn ?a) (distance ?c1 ?c2)))`) 
 - ❌ Does **not** use assignments (`:=`) or non-linear expressions 
 - ❌ Violates **SNT** constraints because the `increase`/`decrease` operations are **not by constant literals**, but by computed static terms involving parameters This makes the domain a clear **Linear Task (LT)** 
 — expressive enough for real-world modeling while still compatible with many numeric planners that support linear arithmetic.

## Summary
This extended **Zenotravel domain** introduces **total-time tracking** for flights, allowing for more realistic travel planning based solely on time. By differentiating between **slow and fast flights** with corresponding speeds, the domain now enables **time-aware decision-making** in automated planning without tracking total fuel consumption.

This version can be used for planning problems where the optimization criterion is purely based on minimizing travel time.
