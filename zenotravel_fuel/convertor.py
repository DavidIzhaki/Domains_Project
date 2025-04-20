#!/usr/bin/env python3
import os
import re
import json
import argparse

def remove_comments(text):
    """Strip out PDDL ‘;’ comments."""
    return "\n".join(line for line in text.splitlines()
                     if not line.strip().startswith(";"))

def parse_objects(pddl: str):
    """Return dicts mapping each aircraft/person/city name → index."""
    m = re.search(r"\(:objects(.*?)\(:init", pddl, re.DOTALL | re.IGNORECASE)
    if not m:
        raise RuntimeError("No :objects block")
    block = m.group(1).strip().rstrip(")")
    aircraft = {}; persons = {}; cities = {}
    for line in block.splitlines():
        line = line.strip().rstrip(")")
        if "-" not in line:
            continue
        names, typ = line.split("-", 1)
        names = names.split()
        typ = typ.strip().lower()
        target = (
            aircraft if typ == "aircraft" else
            persons  if typ == "person"  else
            cities
        )
        for n in names:
            if n not in target:
                target[n] = len(target)
    return aircraft, persons, cities

def parse_init(pddl: str, aircraft, persons, cities):
    """
    Reads :init and returns:
      - aircraft_info: { plane_name: {capacity,fuel,slow_burn,fast_burn,onboard,zoom_limit,location} }
      - persons_info:  { person_name: {location,on_airplane=-1} }
      - distances_flat:{ "i,j": dist } including self‑distances
    """
    m = re.search(r"\(:init(.*?)\(:goal", pddl, re.DOTALL | re.IGNORECASE)
    if not m:
        raise RuntimeError("No :init block")
    init = m.group(1)

    aircraft_info = {p: {} for p in aircraft}
    persons_info = {p: {} for p in persons}
    distances_flat = {}

    # located predicates
    for obj, loc in re.findall(r"\(located\s+(\S+)\s+(\S+)\)", init, re.IGNORECASE):
        if obj in aircraft and loc in cities:
            aircraft_info[obj]["location"] = cities[loc]
        if obj in persons and loc in cities:
            persons_info[obj]["location"] = cities[loc]

    # numeric aircraft props
    for pred, key in [
        ("capacity",   "capacity"),
        ("fuel",       "fuel"),
        ("slow-burn",  "slow_burn"),
        ("fast-burn",  "fast_burn"),
        ("onboard",    "onboard"),
        ("zoom-limit", "zoom_limit"),
    ]:
        regex = re.compile(rf"\(=\s*\({pred}\s+(\S+)\)\s+(\d+)\)", re.IGNORECASE)
        for plane, val in regex.findall(init):
            if plane in aircraft_info:
                aircraft_info[plane][key] = int(val)

    # distances — flat map
    for c1, c2, dist in re.findall(
        r"\(=\s*\(distance\s+(\S+)\s+(\S+)\)\s+(\d+)\)", init, re.IGNORECASE
    ):
        if c1 in cities and c2 in cities:
            i1, i2 = cities[c1], cities[c2]
            distances_flat[f"{i1},{i2}"] = int(dist)

    # defaults for missing values
    for pl in aircraft_info.values():
        pl.setdefault("location", 0)
        for key in ("capacity","fuel","slow_burn","fast_burn","onboard","zoom_limit"):
            pl.setdefault(key, 0)
    for pp in persons_info.values():
        pp.setdefault("location", 0)
        pp["on_airplane"] = -1

    return aircraft_info, persons_info, distances_flat

def parse_goal(pddl: str, aircraft, persons, cities):
    """Return airplane_goals and person_goals as lists of [index, city_index]."""
    goal_section = re.split(r"\(:metric", pddl, flags=re.IGNORECASE)[0]
    gm = re.search(r"\(:goal\s+\(and(.*)\)\s*\)", goal_section,
                   re.DOTALL | re.IGNORECASE)
    if not gm:
        raise RuntimeError("No :goal block")
    text = gm.group(1)
    airplane_goals = []
    person_goals   = []
    for obj, loc in re.findall(r"\(located\s+(\S+)\s+(\S+)\)", text, re.IGNORECASE):
        if loc not in cities:
            continue
        ci = cities[loc]
        if obj in aircraft:
            airplane_goals.append([ aircraft[obj], ci ])
        if obj in persons:
            person_goals.append([ persons[obj], ci ])
    return airplane_goals, person_goals

def convert_pddl_to_json(path):
    text = open(path).read()
    pddl = remove_comments(text)

    aircraft, persons, cities = parse_objects(pddl)
    ai, pi, distances_flat   = parse_init(pddl, aircraft, persons, cities)
    num_cities               = len(cities)
    ag, pg                   = parse_goal(pddl, aircraft, persons, cities)

    # Build ordered lists
    airplanes_list = [None]*len(aircraft)
    for name, idx in aircraft.items():
        info = ai[name]
        airplanes_list[idx] = {
            "index":      idx,
            "slow_burn":  info["slow_burn"],
            "fast_burn":  info["fast_burn"],
            "capacity":   info["capacity"],
            "fuel":       info["fuel"],
            "location":   info["location"],
            "zoom_limit": info["zoom_limit"],
            "onboard":    info["onboard"]
        }

    persons_list = [None]*len(persons)
    for name, idx in persons.items():
        info = pi[name]
        persons_list[idx] = {
            "location":    info["location"],
            "on_airplane": info["on_airplane"]
        }

    # Group distances by origin city, **skip self‑distances** (i1 == i2)
    grouped = {}
    for key, dist in distances_flat.items():
        i1, i2 = key.split(",",1)
        if i1 == i2:
            continue
        grouped.setdefault(i1, []).append([int(i2), dist])

    return {
        "state": {
            "airplanes": airplanes_list,
            "persons":   persons_list,
        },
        "problem": {
            "goal":       { "airplanes": ag, "persons": pg },
            "num_cities": num_cities,
            "distances":  grouped
        }
    }

def main(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for fn in os.listdir(input_dir):
        if fn.lower().endswith(".pddl"):
            src = os.path.join(input_dir, fn)
            dst = os.path.join(output_dir, fn[:-5] + ".json")
            try:
                data = convert_pddl_to_json(src)
                with open(dst, "w") as f:
                    json.dump(data, f, indent=2)
                print(f"Converted {src} → {dst}")
            except Exception as e:
                print(f"Error processing {src}: {e}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("input_dir",  help="PDDL files folder")
    p.add_argument("output_dir", help="Directory for JSON output")
    args = p.parse_args()
    main(args.input_dir, args.output_dir)
