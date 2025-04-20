#!/usr/bin/env python3
import os
import re
import json
import argparse

def remove_comments(text: str) -> str:
    """Strip PDDL ‘;’ comments."""
    return "\n".join(
        line for line in text.splitlines()
        if not line.strip().startswith(";")
    )

def parse_objects(pddl: str):
    """Map each aircraft/person/city name → integer index."""
    m = re.search(r"\(:objects(.*?)\(:init", pddl, re.DOTALL | re.IGNORECASE)
    if not m:
        raise RuntimeError("No :objects block")
    block = m.group(1).strip().rstrip(")")
    aircraft = {}; persons = {}; cities = {}
    for line in block.splitlines():
        line = line.strip().rstrip(")")
        if "-" not in line:
            continue
        names, kind = line.split("-",1)
        kind = kind.strip().lower()
        target = (
            aircraft if kind=="aircraft" else
            persons  if kind=="person"   else
            cities
        )
        for n in names.split():
            if n not in target:
                target[n] = len(target)
    return aircraft, persons, cities

def parse_init(pddl: str, aircraft, persons, cities):
    """
    Parse (:init …) and return:
      - aircraft_info: dict plane→{capacity,fuel,slow_burn,slow_speed,fast_burn,fast_speed,onboard,zoom_limit,location}
      - persons_info:  dict person→{location,on_airplane=-1}
      - distances_flat: dict "i,j"→distance
    """
    m = re.search(r"\(:init(.*?)\(:goal", pddl, re.DOTALL | re.IGNORECASE)
    if not m:
        raise RuntimeError("No :init block")
    init = m.group(1)

    # prepare
    aircraft_info = {p:{} for p in aircraft}
    persons_info = {p:{} for p in persons}
    distances_flat = {}

    # located predicates
    for obj, loc in re.findall(r"\(located\s+(\S+)\s+(\S+)\)", init, re.IGNORECASE):
        if obj in aircraft and loc in cities:
            aircraft_info[obj]["location"] = cities[loc]
        if obj in persons and loc in cities:
            persons_info[obj]["location"] = cities[loc]

    # numeric aircraft attributes
    for pred, key in [
        ("capacity",   "capacity"),
        ("fuel",       "fuel"),
        ("slow-burn",  "slow_burn"),
        ("fast-burn",  "fast_burn"),
        ("slow-speed", "slow_speed"),
        ("fast-speed", "fast_speed"),
        ("onboard",    "onboard"),
        ("zoom-limit", "zoom_limit"),
    ]:
        regex = re.compile(rf"\(=\s*\({pred}\s+(\S+)\)\s+(\d+)\)", re.IGNORECASE)
        for plane, val in regex.findall(init):
            if plane in aircraft_info:
                aircraft_info[plane][key] = int(val)

    # distances
    for c1, c2, dist in re.findall(
        r"\(=\s*\(distance\s+(\S+)\s+(\S+)\)\s+(\d+)\)", init, re.IGNORECASE
    ):
        if c1 in cities and c2 in cities:
            i1, i2 = cities[c1], cities[c2]
            distances_flat[f"{i1},{i2}"] = int(dist)

    # defaults
    for info in aircraft_info.values():
        info.setdefault("location", 0)
        for k in ["capacity","fuel","slow_burn","slow_speed",
                  "fast_burn","fast_speed","onboard","zoom_limit"]:
            info.setdefault(k, 0)
    for info in persons_info.values():
        info.setdefault("location", 0)
        info["on_airplane"] = -1

    return aircraft_info, persons_info, distances_flat

def parse_goal(pddl: str, aircraft, persons, cities):
    """
    Parse (:goal (and …)) and return two lists:
      - airplane_goals: [[plane_idx, city_idx],…]
      - person_goals:   [[person_idx,city_idx],…]
    """
    # strip off any metric
    goal_sec = re.split(r"\(:metric", pddl, flags=re.IGNORECASE)[0]
    gm = re.search(r"\(:goal\s+\(and(.*)\)\s*\)", goal_sec, re.DOTALL | re.IGNORECASE)
    if not gm:
        raise RuntimeError("No :goal block")
    text = gm.group(1)
    ag=[]; pg=[]
    for obj,loc in re.findall(r"\(located\s+(\S+)\s+(\S+)\)", text, re.IGNORECASE):
        if loc not in cities:
            continue
        ci = cities[loc]
        if obj in aircraft: ag.append([ aircraft[obj], ci ])
        elif obj in persons: pg.append([ persons[obj], ci ])
    return ag, pg

def parse_metric(pddl: str):
    """
    Parse (:metric minimize …) and return {fuel:coef, time:coef}.
    Supports any combination of total-fuel-used and total-time.
    Defaults to 1 for each if present, else 0.
    """
    mblock = re.search(r"\(:metric(.*)\)\s*$", pddl, re.DOTALL|re.IGNORECASE)
    text = mblock.group(1) if mblock else ""
    fuel_term = re.search(r"\(\*\s*(\d+)\s*\(total-fuel-used\)\)", text, re.IGNORECASE)
    time_term = re.search(r"\(\*\s*(\d+)\s*\(total-time\)\)",      text, re.IGNORECASE)
    fuel = int(fuel_term.group(1)) if fuel_term else (1 if "total-fuel-used" in text.lower() else 0)
    time = int(time_term.group(1)) if time_term else (1 if "total-time"      in text.lower() else 0)
    return {"fuel":fuel, "time":time}

def convert_pddl_to_json(path: str):
    pddl = remove_comments(open(path).read())
    aircraft, persons, cities = parse_objects(pddl)
    ai, pi, dist_flat = parse_init(pddl, aircraft, persons, cities)
    num_cities = len(cities)
    ag, pg     = parse_goal(pddl, aircraft, persons, cities)
    metric     = parse_metric(pddl)

    # build ordered lists
    planes = [None]*len(aircraft)
    for name,idx in aircraft.items():
        info = ai[name]
        planes[idx] = {
            "index":      idx,
            "slow_burn":  info["slow_burn"],
            "slow_speed": info["slow_speed"],
            "fast_burn":  info["fast_burn"],
            "fast_speed": info["fast_speed"],
            "capacity":   info["capacity"],
            "fuel":       info["fuel"],
            "location":   info["location"],
            "zoom_limit": info["zoom_limit"],
            "onboard":    info["onboard"],
        }

    people = [None]*len(persons)
    for name,idx in persons.items():
        info = pi[name]
        people[idx] = {
            "location":    info["location"],
            "on_airplane": info["on_airplane"],
        }

    # group distances by origin, skip i→i
    grouped = {}
    for k,d in dist_flat.items():
        i1,i2 = k.split(",",1)
        if i1==i2: continue
        grouped.setdefault(i1, []).append([int(i2), d])

    return {
        "state": {
            "airplanes": planes,
            "persons":   people,
        },
        "problem": {
            "goal":       { "airplanes":ag, "persons":pg },
            "num_cities": num_cities,
            "distances":  grouped,
            "minimize":   metric,
        }
    }

def main(inp: str, outp: str):
    os.makedirs(outp, exist_ok=True)
    for fn in os.listdir(inp):
        if fn.lower().endswith(".pddl"):
            dst = os.path.join(outp, fn[:-5]+".json")
            try:
                j = convert_pddl_to_json(os.path.join(inp,fn))
                with open(dst,"w") as f:
                    json.dump(j,f,indent=2)
                print("✓", fn)
            except Exception as e:
                print("✗", fn, e)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("input_dir")
    p.add_argument("output_dir")
    a=p.parse_args()
    main(a.input_dir,a.output_dir)
