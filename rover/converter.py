import re
import os
import json
import argparse

def remove_comments(text):
    return "\n".join(line for line in text.splitlines() if not line.strip().startswith(";"))

def extract_objects(pddl_text, type_name):
    pattern = rf'([^\n]*?)\s+-\s+{type_name}(?=\s|\))'
    objects = set()
    for match in re.finditer(pattern, pddl_text):
        names = match.group(1).strip().split()
        for name in names:
            if name != type_name:
                objects.add(name)
    return objects

def parse_pddl(pddl_text):
    pddl_text = remove_comments(pddl_text)

    rovers = extract_objects(pddl_text, "rover")
    stores = extract_objects(pddl_text, "store")
    cameras = extract_objects(pddl_text, "camera")
    modes = extract_objects(pddl_text, "mode")
    waypoints = extract_objects(pddl_text, "waypoint")
    objectives = extract_objects(pddl_text, "objective")
    landers = extract_objects(pddl_text, "lander")

    # Extract init
    init_match = re.search(r':init\s*(.*?)\s*\(:goal', pddl_text, re.DOTALL)
    init_raw = init_match.group(1) if init_match else ""
    init_text = init_raw.replace("\n", " ").replace("\t", " ").strip()

    # Extract full goal block
    goal_match = re.search(r':goal\s*\(\s*and\s*((?:.|\n)*?)\)\s*(\(:metric|\)\s*$)', pddl_text, re.DOTALL)
    goal_text = goal_match.group(1) if goal_match else ""


    goal_text = goal_text.replace("\n", " ").replace("\t", " ").strip()
    goal_text = " ".join(goal_text.replace("\n", " ").replace("\t", " ").split())
    # print("Goal Text:", goal_text)

    goal = {"conditions": []}
    goal["conditions"] += [
        {"SoilDataCommunicated": {"waypoint": m.group(1)}}
        for m in re.finditer(r'\(communicated_soil_data (\S+)\)', goal_text)
    ]
    goal["conditions"] += [
        {"RockDataCommunicated": {"waypoint": m.group(1)}}
        for m in re.finditer(r'\(communicated_rock_data (\S+)\)', goal_text)
    ]
    goal["conditions"] += [
        {"ImageDataCommunicated": {"objective": m.group(1), "mode": m.group(2)}}
        for m in re.finditer(r'\(communicated_image_data (\S+) (\S+)\)', goal_text)
    ]

    state = {
        "rovers": {},
        "cameras": {},
        "waypoints": {},
        "landers": {},
        "soil_analysis": {},
        "rock_analysis": {},
        "images": {},
        "communicated_soil_data": [],
        "communicated_rock_data": [],
        "communicated_image_data": {},
        "recharges": 0
    }

    for rover in rovers:
        loc = re.search(rf'\(in {rover} (\S+)\)', init_text)
        energy = re.search(rf'\(= \(energy {rover}\) (\d+)\)', init_text)
        state["rovers"][rover] = {
            "id": rover,
            "location": loc.group(1) if loc else None,
            "energy": int(energy.group(1)) if energy else 0,
            "equipped_for_soil_analysis": f"(equipped_for_soil_analysis {rover})" in init_text,
            "equipped_for_rock_analysis": f"(equipped_for_rock_analysis {rover})" in init_text,
            "equipped_for_imaging": f"(equipped_for_imaging {rover})" in init_text,
            "available": f"(available {rover})" in init_text
        }

    for store in stores:
        r_id = re.search(rf'\(store_of {store} (\S+)\)', init_text)
        if r_id:
            rover_id = r_id.group(1)
            if rover_id in state["rovers"]:
                state["rovers"][rover_id]["store"] = {
                    "id": store,
                    "rover_id": rover_id,
                    "empty": f"(empty {store})" in init_text,
                    "full": f"(full {store})" in init_text
                }


    for camera in cameras:
        r_id = re.search(rf'\(on_board {camera} (\S+)\)', init_text)
        c_target = re.search(rf'\(calibration_target {camera} (\S+)\)', init_text)
        supported = sorted([m for m in modes if f"(supports {camera} {m})" in init_text])
        state["cameras"][camera] = {
            "id": camera,
            "rover_id": r_id.group(1) if r_id else None,
            "calibration_target": c_target.group(1) if c_target else None,
            "supported_modes": supported,
            "calibrated_objective": None
        }

    for wp in waypoints:
        state["waypoints"][wp] = {
            "id": wp,
            "has_soil_sample": f"(at_soil_sample {wp})" in init_text,
            "has_rock_sample": f"(at_rock_sample {wp})" in init_text,
            "in_sun": f"(in_sun {wp})" in init_text
        }

    for lander in landers:
        loc = re.search(rf'\(at_lander {lander} (\S+)\)', init_text)
        state["landers"][lander] = {
            "id": lander,
            "location": loc.group(1) if loc else None,
            "channel_free": f"(channel_free {lander})" in init_text
        }

    recharges = re.search(r'\(= \(recharges\) (\d+)\)', init_text)
    state["recharges"] = int(recharges.group(1)) if recharges else 0

    objectives_dict = {}
    for obj in objectives:
        visible_from = [wp for wp in waypoints if f"(visible_from {obj} {wp})" in init_text]
        objectives_dict[obj] = {"id": obj, "visible_from": visible_from}

    visible = {wp: [] for wp in waypoints}
    for wp1 in waypoints:
        for wp2 in waypoints:
            if f"(visible {wp1} {wp2})" in init_text:
                visible[wp1].append(wp2)

    can_traverse = {}
    for rover in rovers:
        can_traverse[rover] = {}
        for wp1 in waypoints:
            can_traverse[rover][wp1] = [
                wp2 for wp2 in waypoints if f"(can_traverse {rover} {wp1} {wp2})" in init_text
            ]

    return {
        "state": state,
        "problem": {
            "goal": goal,
            "objectives": objectives_dict,
            "can_traverse": can_traverse,
            "visible": visible
        }
    }

def convert_file(input_path, output_path):
    with open(input_path, 'r') as f:
        pddl_text = f.read()
    parsed = parse_pddl(pddl_text)
    with open(output_path, 'w') as out:
        json.dump(parsed, out, indent=2)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i')
    parser.add_argument('--output', '-o')
    args = parser.parse_args()

    if args.input and args.output:
        convert_file(args.input, args.output)
    else:
        input_dir = "problems_pddl"
        output_dir = "problems_json"
        os.makedirs(output_dir, exist_ok=True)
        for filename in os.listdir(input_dir):
            if filename.endswith('.pddl'):
                convert_file(os.path.join(input_dir, filename), os.path.join(output_dir, filename.replace(".pddl", ".json")))

if __name__ == "__main__":
    main()
