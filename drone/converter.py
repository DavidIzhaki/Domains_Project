#!/usr/bin/env python3
import re
import json
import os
import argparse

def parse_bounds(pddl_text):
    bounds = {}
    patterns = {
        'min_x': r'\(=\s*\(min_x\)\s*(\d+)\)',
        'max_x': r'\(=\s*\(max_x\)\s*(\d+)\)',
        'min_y': r'\(=\s*\(min_y\)\s*(\d+)\)',
        'max_y': r'\(=\s*\(max_y\)\s*(\d+)\)',
        'min_z': r'\(=\s*\(min_z\)\s*(\d+)\)',
        'max_z': r'\(=\s*\(max_z\)\s*(\d+)\)'
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, pddl_text)
        if match:
            bounds[key] = int(match.group(1))
    return bounds

def parse_battery(pddl_text):
    level_match = re.search(r'\(=\s*\(battery-level\)\s*(\d+)\)', pddl_text)
    capacity_match = re.search(r'\(=\s*\(battery-level-full\)\s*(\d+)\)', pddl_text)
    return {
        'battery_level': int(level_match.group(1)) if level_match else 0,
        'battery_capacity': int(capacity_match.group(1)) if capacity_match else 0
    }

def parse_locations(pddl_text):
    locations = {}
    location_pattern = r'\(=\s*\(xl\s+(x\d+y\d+z\d+)\)\s*(\d+)\).*?' + \
                       r'\(=\s*\(yl\s+\1\)\s*(\d+)\).*?' + \
                       r'\(=\s*\(zl\s+\1\)\s*(\d+)\)'
    matches = re.finditer(location_pattern, pddl_text, re.DOTALL)
    for match in matches:
        loc_name, x, y, z = match.groups()
        locations[loc_name] = [int(x), int(y), int(z)]
    return locations

def parse_goal(pddl_text):
    goal_match = re.search(r'\(:goal\s*\(and\s*(.*?)\)\s*\)', pddl_text, re.DOTALL)
    if not goal_match:
        return {}

    goal_text = goal_match.group(1)
    visited = re.findall(r'\(visited\s+(x\d+y\d+z\d+)\)', goal_text)
    position_match = re.search(r'\(=\s*\(x\)\s*(\d+)\)\s*\(=\s*\(y\)\s*(\d+)\)\s*\(=\s*\(z\)\s*(\d+)\)', goal_text)

    return {
        "visited": visited,
        "position": [int(position_match.group(1)), int(position_match.group(2)), int(position_match.group(3))] if position_match else [0, 0, 0]
    }

def convert_pddl_to_json(pddl_text):
    bounds = parse_bounds(pddl_text)
    battery_info = parse_battery(pddl_text)
    locations = parse_locations(pddl_text)
    visited = {loc: False for loc in locations.keys()}
    goal = parse_goal(pddl_text)

    json_data = {
        "state": {
            "battery_level": battery_info["battery_level"],
            "x": 0,
            "y": 0,
            "z": 0,
            "visited": visited
        },
        "problem": {
            "battery_capacity": battery_info["battery_capacity"],
            "bounds": [
                [bounds['min_x'], bounds['max_x']],
                [bounds['min_y'], bounds['max_y']],
                [bounds['min_z'], bounds['max_z']]
            ],
            "locations": locations,
            **goal
        }
    }

    return json_data

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', help='Optional input directory (default: problems_pddl)')
    parser.add_argument('--output', '-o', help='Optional output directory (default: problems_json)')
    args = parser.parse_args()

    input_dir = args.input if args.input else "problems_pddl"
    output_dir = args.output if args.output else "problems_json"

    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith('.pddl'):
            input_path = os.path.join(input_dir, filename)
            output_filename = f"problem{filename[5:-5]}.json"
            output_path = os.path.join(output_dir, output_filename)

            with open(input_path, 'r') as f:
                pddl_text = f.read()

            json_data = convert_pddl_to_json(pddl_text)

            with open(output_path, 'w') as f:
                json.dump(json_data, f, indent=4)

            print(f"Converted {filename} to {output_filename}")


if __name__ == '__main__':
    main()
