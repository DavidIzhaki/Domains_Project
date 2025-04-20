#!/usr/bin/env python3
import os
import re
import json
import argparse

def parse_pddl_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # 1) GRID BOUNDARIES (from the init block)
    def find_int(var):
        m = re.search(r"\(=\s*\(" + re.escape(var) + r"\)\s+(\d+)\)", content)
        return int(m.group(1)) if m else None

    min_x = find_int("min_x"); max_x = find_int("max_x")
    min_y = find_int("min_y"); max_y = find_int("max_y")
    if None in (min_x, max_x, min_y, max_y):
        raise ValueError(f"Missing grid bounds in {filepath}")
    col_size = max_x - min_x + 1
    row_size = max_y - min_y + 1

    # 2) OBJECTS SECTION (between "(:objects" and "(:init")
    start = content.find("(:objects")
    end   = content.find("(:init", start)
    objects_text = content[start:end] if start != -1 and end != -1 else ""

    # 3) EXTRACT VEHICLE NAMES by type
    def extract_names(pattern):
        names = []
        for grp in re.findall(pattern, objects_text, re.MULTILINE):
            names.extend(grp.split())
        return names

    horizontal_car_names = extract_names(r"^[ \t]*([\w-]+(?:[ \t]+[\w-]+)*)[ \t]*-[ \t]*horizontalCar\b")
    vertical_car_names   = extract_names(r"^[ \t]*([\w-]+(?:[ \t]+[\w-]+)*)[ \t]*-[ \t]*verticalCar\b")
    horizontal_truck_names = extract_names(r"^[ \t]*([\w-]+(?:[ \t]+[\w-]+)*)[ \t]*-[ \t]*horizontalTruck\b")
    vertical_truck_names   = extract_names(r"^[ \t]*([\w-]+(?:[ \t]+[\w-]+)*)[ \t]*-[ \t]*verticalTruck\b")

    # 4) EXTRACT INIT BLOCK (up to (:goal))
    init_start = content.find("(:init")
    if init_start == -1:
        raise ValueError(f"Missing (:init block in {filepath}")
    goal_start = content.find("(:goal", init_start)
    init_text = content[init_start : (goal_start if goal_start != -1 else None)]

    # 5) POSITIONS
    pos_x = {n: int(x) for n, x in re.findall(r"\(=\s*\(pos-x\s+([\w-]+)\)\s+(\d+)\)", init_text)}
    pos_y = {n: int(y) for n, y in re.findall(r"\(=\s*\(pos-y\s+([\w-]+)\)\s+(\d+)\)", init_text)}

    # 6) BUILD VEHICLES LIST with type tag
    vehicles = []
    def add_vehicles(names, vtype):
        for n in names:
            if n in pos_x and n in pos_y:
                vehicles.append({
                    "vehicle_type": vtype,
                    "name": n,
                    "x": pos_x[n],
                    "y": pos_y[n]
                })
    add_vehicles(horizontal_car_names,   "horizontal_car")
    add_vehicles(vertical_car_names,     "vertical_car")
    add_vehicles(horizontal_truck_names, "horizontal_truck")
    add_vehicles(vertical_truck_names,   "vertical_truck")
        # 7) FILL GRID CELLS DIRECTLY
    cells = {}   # will become: HashMap<(i32,i32), String>
    for v in vehicles:
        x, y = v["x"], v["y"]
        name = v["name"]
        typ  = v["vehicle_type"]
        # determine all occupied positions
        if typ == "horizontal_car":
            positions = [(x, y), (x+1, y)]
        elif typ == "vertical_car":
            positions = [(x, y), (x, y+1)]
        elif typ == "horizontal_truck":
            positions = [(x, y), (x+1, y), (x+2, y)]
        elif typ == "vertical_truck":
            positions = [(x, y), (x, y+1), (x, y+2)]
        else:
            positions = []

        for (cx, cy) in positions:
            # JSON keys must be strings; Serde will parse "(x, y)" into (i32,i32)
            cells[f"({cx},{cy})"] = name


    # 7) FINAL JSON with both state and problem
    return {
        "state": {
            "grid": {"row_size": row_size, "col_size": col_size,  "cells": cells  },
            "vehicles": vehicles
        },
        "problem": {}
    }


def convert_directory(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for fn in os.listdir(input_dir):
        if not fn.endswith('.pddl'):
            continue
        inpath  = os.path.join(input_dir, fn)
        outpath = os.path.join(output_dir, fn[:-5] + '.json')
        try:
            j = parse_pddl_file(inpath)
            with open(outpath, 'w') as f:
                json.dump(j, f, indent=4)
            print(f"Converted {fn} → {os.path.basename(outpath)}")
        except Exception as e:
            print(f"❌ {fn}: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Convert RedCar PDDL problems to JSON (vehicles list)."
    )
    parser.add_argument('input_dir',  help='PDDL problem files directory')
    parser.add_argument('output_dir', help='Where to write JSON files')
    args = parser.parse_args()
    convert_directory(args.input_dir, args.output_dir)
