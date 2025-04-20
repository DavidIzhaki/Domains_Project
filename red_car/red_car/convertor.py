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

    # 3) EXTRACT CAR/TRUCK NAMES
    def extract_names(pattern):
        names = []
        for grp in re.findall(pattern, objects_text, re.MULTILINE):
            names.extend(grp.split())
        return names

    horizontal_car_names   = extract_names(r"^[ \t]*([\w-]+(?:[ \t]+[\w-]+)*)[ \t]*-[ \t]*horizontalCar\b")
    vertical_car_names     = extract_names(r"^[ \t]*([\w-]+(?:[ \t]+[\w-]+)*)[ \t]*-[ \t]*verticalCar\b")
    horizontal_truck_names = extract_names(r"^[ \t]*([\w-]+(?:[ \t]+[\w-]+)*)[ \t]*-[ \t]*horizontalTruck\b")
    vertical_truck_names   = extract_names(r"^[ \t]*([\w-]+(?:[ \t]+[\w-]+)*)[ \t]*-[ \t]*verticalTruck\b")

    # 4) EXTRACT INIT BLOCK
    init_start = content.find("(:init")
    if init_start == -1:
        raise ValueError(f"Missing (:init block in {filepath}")
    goal_start = content.find("(:goal", init_start)
    init_text = content[init_start : (goal_start if goal_start != -1 else None)]

    # 5) POSITIONS
    pos_x = {n: int(x) for n, x in re.findall(r"\(=\s*\(pos-x\s+([\w-]+)\)\s+(\d+)\)", init_text)}
    pos_y = {n: int(y) for n, y in re.findall(r"\(=\s*\(pos-y\s+([\w-]+)\)\s+(\d+)\)", init_text)}

    # 6) BUILD VEHICLE LISTS
    horizontalcars = [ {"name": n, "x": pos_x[n], "y": pos_y[n]} for n in horizontal_car_names if n in pos_x and n in pos_y ]
    verticalcars   = [ {"name": n, "x": pos_x[n], "y": pos_y[n]} for n in vertical_car_names   if n in pos_x and n in pos_y ]
    horizontaltrucks = [ {"name": n, "x": pos_x[n], "y": pos_y[n]} for n in horizontal_truck_names if n in pos_x and n in pos_y ]
    verticaltrucks   = [ {"name": n, "x": pos_x[n], "y": pos_y[n]} for n in vertical_truck_names   if n in pos_x and n in pos_y ]

    # 7) FILL GRID CELLS BASED ON VEHICLES
    cells = {}
    def mark(positions, name):
        for (x,y) in positions:
            key = f"({x},{y})"
            cells[key] = name

    for car in horizontalcars:
        x,y,name = car['x'], car['y'], car['name']
        mark([(x,y),(x+1,y)], name)
    for car in verticalcars:
        x,y,name = car['x'], car['y'], car['name']
        mark([(x,y),(x,y+1)], name)
    for tr in horizontaltrucks:
        x,y,name = tr['x'], tr['y'], tr['name']
        mark([(x,y),(x+1,y),(x+2,y)], name)
    for tr in verticaltrucks:
        x,y,name = tr['x'], tr['y'], tr['name']
        mark([(x,y),(x,y+1),(x,y+2)], name)

    # 8) FINAL JSON
    return {
        "state": {
            "grid": {"row_size": row_size, "col_size": col_size, "cells": cells},
            "horizontalcars": horizontalcars,
            "verticalcars": verticalcars,
            "horizontaltrucks": horizontaltrucks,
            "verticaltrucks": verticaltrucks
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
        description="Convert RedCar PDDL problems to JSON (horiz/vert cars)."
    )
    parser.add_argument('input_dir',  help='PDDL problem files directory')
    parser.add_argument('output_dir', help='Where to write JSON files')
    args = parser.parse_args()
    convert_directory(args.input_dir, args.output_dir)
