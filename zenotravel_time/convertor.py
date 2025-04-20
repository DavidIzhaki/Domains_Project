#!/usr/bin/env python3
import os
import re
import json
import argparse

def remove_comments(text: str) -> str:
    """Strip out PDDL ‘;’ comments."""
    return "\n".join(
        line for line in text.splitlines()
        if not line.strip().startswith(";")
    )

def parse_objects(pddl: str):
    """Return maps name→index for aircraft, persons, and cities."""
    m = re.search(r"\(:objects(.*?)\(:init", pddl, re.DOTALL | re.IGNORECASE)
    if not m:
        raise RuntimeError("No :objects block found")
    block = m.group(1).strip().rstrip(")")
    aircraft = {}; persons = {}; cities = {}
    for line in block.splitlines():
        line = line.strip().rstrip(")")
        if "-" not in line:
            continue
        names, kind = line.split("-",1)
        idx_map = (
            aircraft if   kind.strip().lower()=="aircraft" else
            persons  if   kind.strip().lower()=="person"   else
            cities
        )
        for name in names.split():
            if name not in idx_map:
                idx_map[name] = len(idx_map)
    return aircraft, persons, cities

def parse_init(pddl: str, aircraft, persons, cities):
    """
    Parse the :init block and return:
      - aircraft_info: dict plane→{capacity, fuel, slow_burn, slow_speed,
                                   fast_burn, fast_speed, onboard, zoom_limit, location}
      - persons_info:  dict person→{location, on_airplane=-1}
      - distances_flat: dict "i,j"→distance (including self‑distances)
    """
    m = re.search(r"\(:init(.*?)\(:goal", pddl, re.DOTALL | re.IGNORECASE)
    if not m:
        raise RuntimeError("No :init block found")
    init = m.group(1)

    # prepare defaults
    aircraft_info = {p: {} for p in aircraft}
    persons_info = {p: {} for p in persons}
    distances_flat = {}

    # located
    for obj, loc in re.findall(r"\(located\s+(\S+)\s+(\S+)\)", init, re.IGNORECASE):
        if obj in aircraft and loc in cities:
            aircraft_info[obj]["location"] = cities[loc]
        if obj in persons and loc in cities:
            persons_info[obj]["location"] = cities[loc]

    # numeric aircraft attributes
    for pred, key in [
        ("capacity",    "capacity"),
        ("fuel",        "fuel"),
        ("slow-burn",   "slow_burn"),
        ("fast-burn",   "fast_burn"),
        ("slow-speed",  "slow_speed"),
        ("fast-speed",  "fast_speed"),
        ("onboard",     "onboard"),
        ("zoom-limit",  "zoom_limit"),
    ]:
        regex = re.compile(rf"\(=\s*\({pred}\s+(\S+)\)\s+(\d+)\)", re.IGNORECASE)
        for plane, val in regex.findall(init):
            if plane in aircraft_info:
                aircraft_info[plane][key] = int(val)

    # distances
    for c1, c2, dist in re.findall(
        r"\(=\s*\(distance\s+(\S+)\s+(\S+)\)\s+(\d+)\)",
        init, re.IGNORECASE
    ):
        if c1 in cities and c2 in cities:
            i1, i2 = cities[c1], cities[c2]
            distances_flat[f"{i1},{i2}"] = int(dist)

    # defaults for missing values
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
    Parse the :goal block, return:
      airplane_goals: [[plane_idx, city_idx],…]
      person_goals:   [[person_idx, city_idx],…]
    """
    # strip off any metric
    goal_section = re.split(r"\(:metric", pddl, flags=re.IGNORECASE)[0]
    gm = re.search(r"\(:goal\s+\(and(.*)\)\s*\)", goal_section,
                   re.DOTALL | re.IGNORECASE)
    if not gm:
        raise RuntimeError("No :goal block found")
    text = gm.group(1)
    ag = []; pg = []
    for obj, loc in re.findall(r"\(located\s+(\S+)\s+(\S+)\)", text, re.IGNORECASE):
        if loc not in cities:
            continue
        ci = cities[loc]
        if obj in aircraft:
            ag.append([ aircraft[obj], ci ])
        elif obj in persons:
            pg.append([ persons[obj], ci ])
    return ag, pg

def convert_pddl_to_json(path: str):
    pddl = remove_comments(open(path).read())
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
            "slow_speed": info["slow_speed"],
            "fast_burn":  info["fast_burn"],
            "fast_speed": info["fast_speed"],
            "capacity":   info["capacity"],
            "fuel":       info["fuel"],
            "location":   info["location"],
            "zoom_limit": info["zoom_limit"],
            "onboard":    info["onboard"],
        }

    persons_list = [None]*len(persons)
    for name, idx in persons.items():
        info = pi[name]
        persons_list[idx] = {
            "location":    info["location"],
            "on_airplane": info["on_airplane"],
        }

    # Group distances by origin, skip self-distances
    grouped = {}
    for key, d in distances_flat.items():
        i1, i2 = key.split(",",1)
        if i1 == i2:
            continue
        grouped.setdefault(i1, []).append([int(i2), d])

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

def main(input_dir: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    for fn in os.listdir(input_dir):
        if fn.lower().endswith(".pddl"):
            src = os.path.join(input_dir, fn)
            dst = os.path.join(output_dir, fn[:-5] + ".json")
            try:
                out = convert_pddl_to_json(src)
                with open(dst, "w") as f:
                    json.dump(out, f, indent=2)
                print(f"Converted {src} → {dst}")
            except Exception as e:
                print(f"Error processing {src}: {e}")

if __name__ == "__main__":
    p = argparse.ArgumentParser(
        description="Convert ZenoTravel PDDL (time‐minimization) to JSON"
    )
    p.add_argument("input_dir",  help="directory of .pddl files")
    p.add_argument("output_dir", help="directory for .json output")
    args = p.parse_args()
    main(args.input_dir, args.output_dir)
