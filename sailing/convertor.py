#!/usr/bin/env python3
import re
import json
import os
import argparse

def parse_boats_and_persons(pddl_text):
    """Parse boats and persons from the PDDL text."""
    boats = []
    persons = []
    
    boat_matches = re.finditer(r'\(= \(x (\w+)\) ([\d\-.]+)\)\s*\(= \(y \1\) ([\d\-.]+)\)', pddl_text)
    person_matches = re.finditer(r'\(= \(d (\w+)\) ([\d\-.]+)\)', pddl_text)
    
    for index, match in enumerate(boat_matches):
        boat_id, x, y = match.groups()
        boats.append({
            "id": boat_id,
            "x": float(x),
            "y": float(y),
            "index": index
        })
    
    for index, match in enumerate(person_matches):
        person_id, d = match.groups()
        persons.append({
            "id": person_id,
            "d": float(d),
            "saved": False,
            "index": index
        })
    
    return boats, persons

def parse_goal(pddl_text):
    """Parse goal information from the PDDL text."""
    saved_persons = []
    goal_matches = re.finditer(r'\(saved (\w+)\)', pddl_text)
    
    for match in goal_matches:
        person_id = match.group(1)
        saved_persons.append(person_id)
    
    return saved_persons

def convert_pddl_to_json(pddl_text):
    """Convert PDDL to JSON structure."""
    boats, persons = parse_boats_and_persons(pddl_text)
    saved_persons = parse_goal(pddl_text)
    
    json_data = {
        "state": {
            "boats": boats,
            "persons": persons,
            "cost": 0  # Assuming initial cost is always zero
        },
        "problem": {
            "goal": {
                "saved_persons": saved_persons
            }
        }
    }
    
    return json_data

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', required=True, help='Input directory containing PDDL files')
    parser.add_argument('--output_dir', required=True, help='Output directory for JSON files')
    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Process all PDDL files in input directory
    for filename in os.listdir(args.input_dir):
        if filename.endswith('.pddl'):
            input_path = os.path.join(args.input_dir, filename)
            output_filename = f"{filename[:-5]}.json"
            output_path = os.path.join(args.output_dir, output_filename)

            with open(input_path, 'r') as f:
                pddl_text = f.read()

            json_data = convert_pddl_to_json(pddl_text)

            with open(output_path, 'w') as f:
                json.dump(json_data, f, indent=4)

            print(f"Converted {filename} to {output_filename}")

if __name__ == '__main__':
    main()