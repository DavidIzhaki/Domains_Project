#!/usr/bin/env python3
import re
import json
import os
import argparse

def map_rooms(pddl_text):
    """Create a map of room names to indices."""
    room_names = set(re.findall(r'(room\w+)', pddl_text))
    return {name: index for index, name in enumerate(sorted(room_names))}

def extract_init_section(pddl_text):
    """Extract the init section from the PDDL text."""
    match = re.search(r'\(:init(.*?)\(:goal', pddl_text, re.DOTALL)
    return match.group(1) if match else ""

def parse_bots(pddl_text, room_map):
    """Parse bot properties including location and load."""
    bots = []
    bot_matches = re.finditer(r'\(at-bot (\w+) (room\w+)\)', pddl_text)
    load_limit_matches = re.finditer(r'\(= \(load_limit (\w+)\) (\d+)\)', pddl_text)
    current_load_matches = re.finditer(r'\(= \(current_load (\w+)\) (\d+)\)', pddl_text)

    bot_dict = {}
    for match in bot_matches:
        bot_id, room_id = match.groups()
        # Determine index by extracting trailing number, or fallback to order
        match_number = re.search(r'(\d+)$', bot_id)
        index = int(match_number.group(1)) if match_number else len(bot_dict) + 1
        bot_dict[bot_id] = {
            "location": room_map[room_id],
            "load_limit": 0,
            "current_load": 0,
            "index": index,
            "arms": [{"is_free": True, "side": idx} for idx in range(2)]
        }

    for match in load_limit_matches:
        bot_id, load_limit = match.groups()
        if bot_id in bot_dict:
            bot_dict[bot_id]["load_limit"] = int(load_limit)

    for match in current_load_matches:
        bot_id, current_load = match.groups()
        if bot_id in bot_dict:
            bot_dict[bot_id]["current_load"] = int(current_load)

    return list(bot_dict.values())

def parse_items(init_section, room_map):
    """Parse items and their properties."""
    items = []
    item_location_matches = re.finditer(r'\(at (item\d+) (room\w+)\)', init_section)
    item_weight_matches = re.finditer(r'\(= \(weight (item\d+)\) (\d+)\)', init_section)

    item_dict = {}
    for match in item_location_matches:
        item_id, room_id = match.groups()
        item_dict[item_id] = {
            "location": room_map[room_id],
            "weight": 0,
            "in_arm": -1,
            "in_tray": -1,
            "index": int(item_id[4:])
        }

    for match in item_weight_matches:
        item_id, weight = match.groups()
        if item_id in item_dict:
            item_dict[item_id]["weight"] = int(weight)

    return list(item_dict.values())

def parse_rooms_and_goals(pddl_text, room_map):
    """Parse room connections and goal locations."""
    connections = {}
    goal_locations = {}
    room_connection_matches = re.finditer(r'\(door (room\w+) (room\w+)\)', pddl_text)
    goal_matches = re.finditer(r'\(at (item\d+) (room\w+)\)', pddl_text)

    for room_name, index in room_map.items():
        connections[f"room{index}"] = []

    for match in room_connection_matches:
        room1, room2 = match.groups()
        index1 = room_map[room1]
        index2 = room_map[room2]
        connections[f"room{index1}"].append(index2)
        connections[f"room{index2}"].append(index1)

    for room_key in connections.keys():
        connections[room_key] = list(set(connections[room_key]))

    for match in goal_matches:
        item_id, room_id = match.groups()
        goal_locations[int(item_id[4:])] = room_map[room_id]

    return connections, goal_locations

def convert_pddl_to_json(pddl_text):
    """Convert PDDL to JSON structure."""
    room_map = map_rooms(pddl_text)
    init_section = extract_init_section(pddl_text)
    bots = parse_bots(pddl_text, room_map)
    items = parse_items(init_section, room_map)
    connections, goal_locations = parse_rooms_and_goals(pddl_text, room_map)

    json_data = {
        "state": {
            "bots": bots,
            "items": items,
            "cost": 0
        },
        "problem": {
            "goal_locations": goal_locations,
            "room_connections": connections
        }
    }

    return json_data

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', default='problems_pddl', help='Input directory (default: problems_pddl)')
    parser.add_argument('--output_dir', default='problems_json', help='Output directory (default: problems_json)')
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

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
