#!/usr/bin/env python3
import os
import re
import json
import argparse
from collections import defaultdict

def parse_objects(pddl_str):
    object_section = re.search(r"\(:objects(.*?)\)", pddl_str, re.DOTALL)
    foods, pleasures, pains = [], [], []

    if object_section:
        lines = object_section.group(1).strip().splitlines()
        for line in lines:
            parts = line.strip().split(" - ")
            if len(parts) == 2:
                names = parts[0].strip().split()
                type_ = parts[1].strip()
                if type_ == "food":
                    foods.extend(names)
                elif type_ == "pleasure":
                    pleasures.extend(names)
                elif type_ == "pain":
                    pains.extend(names)
    return foods, pleasures, pains

def parse_init(pddl_str):
    harmony = {}
    locale = {}
    eats = defaultdict(list)
    craves = defaultdict(list)

    init_section = re.search(r"\(:init(.*?)\)\s*\(:goal", pddl_str, re.DOTALL)
    if init_section:
        init_text = init_section.group(1)
        for match in re.finditer(r"\(= \(locale (\w+)\) (\d+)\)", init_text):
            locale[match.group(1)] = int(match.group(2))
        for match in re.finditer(r"\(= \(harmony (\w+)\) (\d+)\)", init_text):
            harmony[match.group(1)] = int(match.group(2))
        for match in re.finditer(r"\(eats (\w+) (\w+)\)", init_text):
            eats[match.group(1)].append(match.group(2))
        for match in re.finditer(r"\(craves (\w+) (\w+)\)", init_text):
            craves[match.group(1)].append(match.group(2))

    return harmony, locale, eats, craves

def parse_goal(pddl_str):
    goal_conditions = []

    # Match (and (craves ...) ...) or just one (craves ...)
    goal_block = re.search(r"\(:goal\s+\(and\s*((?:\s*\(craves\s+\w+\s+\w+\)\s*)+)\)", pddl_str, re.DOTALL)
    if goal_block:
        for match in re.finditer(r"\(craves\s+(\w+)\s+(\w+)\)", goal_block.group(1)):
            goal_conditions.append({"emotion": match.group(1), "food": match.group(2)})
        return goal_conditions

    # Fallback: single craves
    single_crave = re.search(r"\(:goal\s+\(craves\s+(\w+)\s+(\w+)\)\)", pddl_str)
    if single_crave:
        goal_conditions.append({"emotion": single_crave.group(1), "food": single_crave.group(2)})

    return goal_conditions

def parse_pddl_problem(pddl_str):
    foods, pleasures, pains = parse_objects(pddl_str)
    harmony_map, locale_map, eats_map, craves_map = parse_init(pddl_str)
    goal_conditions = parse_goal(pddl_str)

    state = {
        "pleasures": [
            {
                "name": p,
                "harmony": harmony_map.get(p, 0),
                "craves": craves_map.get(p, [])
            } for p in pleasures
        ],
        "pains": [
            {
                "name": p,
                "harmony": harmony_map.get(p, 0),
                "craves": craves_map.get(p, []),
                "fears": []
            } for p in pains
        ],
        "foods": [
            {
                "name": f,
                "locale": locale_map.get(f, 0)
            } for f in foods
        ]
    }

    return {
        "state": state,
        "problem": {
            "eats": dict(eats_map),
            "goal": {
                "conditions": goal_conditions
            }
        }
    }

def convert_directory(pddl_dir, json_dir):
    os.makedirs(json_dir, exist_ok=True)
    for filename in os.listdir(pddl_dir):
        if filename.endswith(".pddl"):
            path = os.path.join(pddl_dir, filename)
            with open(path, "r") as f:
                pddl_str = f.read()

            json_data = parse_pddl_problem(pddl_str)
            json_path = os.path.join(json_dir, filename.replace(".pddl", ".json"))
            with open(json_path, "w") as out:
                json.dump(json_data, out, indent=2)

            print(f"✅ Converted {filename} → {json_path}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pddl_dir", required=True, help="Directory with .pddl files")
    parser.add_argument("--json_dir", required=True, help="Directory to write .json files")
    args = parser.parse_args()
    convert_directory(args.pddl_dir, args.json_dir)

if __name__ == "__main__":
    main()
