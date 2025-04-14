import re
import json
import os
import argparse

def extract_time_objects(pddl_string):
    """
    Extracts time objects from the :objects block.
    Looks for a line ending with '- time' and splits the tokens.
    """
    time_objects = []
    objects_match = re.search(r'\(:objects(.*?)\)', pddl_string, re.DOTALL | re.IGNORECASE)
    if objects_match:
        objects_text = objects_match.group(1)
        # Process each line in the objects block
        for line in objects_text.splitlines():
            line = line.strip()
            # Look for the line defining time objects (ends with "- time")
            if line.endswith("- time"):
                # Split the line on " -", taking the tokens before the type
                parts = line.rsplit(" -", 1)
                if parts:
                    tokens = parts[0].strip().split()
                    time_objects.extend(tokens)
    return time_objects

def pddl_to_json(pddl_string):
    flags = re.IGNORECASE

    # 1. Build a mapping from node name (e.g., n7) to its numeric value.
    node_mapping = {}
    for match in re.findall(r'\(=\s+\(value\s+(n\d+)\)\s+(\d+)\)', pddl_string, flags):
        node, value = match
        node_mapping[node] = int(value)
    
    # 2. Extract initial funds, e.g. (= (funds) 1000)
    funds_match = re.search(r'\(=\s+\(funds\)\s+(\d+)\)', pddl_string, flags)
    funds = int(funds_match.group(1)) if funds_match else None

    # 3. Extract stored capacity, e.g. (= (stored_capacity) 3)
    capacity_match = re.search(r'\(=\s+\(stored_capacity\)\s+(\d+)\)', pddl_string, flags)
    capacity = int(capacity_match.group(1)) if capacity_match else None

    # 4. Extract goal funds from the goal section: (>= (funds) 1060)
    goal_match = re.search(r'\(\>=\s+\(funds\)\s+(\d+)\)', pddl_string, flags)
    goal_funds = int(goal_match.group(1)) if goal_match else None

    # 5. Extract the list of time objects and create a mapping from time symbol to sequential index.
    time_objects = extract_time_objects(pddl_string)
    time_index_map = { time_sym: idx for idx, time_sym in enumerate(time_objects) }
    time_end = len(time_objects)  # planning horizon is the number of time points

    # 6. Extract demand predicates: (demand tXXXX nX)
    demands = []
    for time_sym, node_sym in re.findall(r'\(demand\s+(t\d+)\s+(n\d+)\)', pddl_string, flags):
        if time_sym in time_index_map and node_sym in node_mapping:
            demands.append({
                "time": time_sym,
                "node": node_sym,
                "value": node_mapping[node_sym]
            })

    # 7. Extract before predicates: (before tXXXX tYYYY)
    before = []
    for t1, t2 in re.findall(r'\(before\s+(t\d+)\s+(t\d+)\)', pddl_string, flags):
        before.append({
            "from": t1,
            "to": t2
        })

    # Create the JSON structure in state-problem format
    return {
        "state": {
            "funds": funds,
            "stored_capacity": capacity,
            "time_end": time_end
        },
        "problem": {
            "goal_funds": goal_funds,
            "demands": demands,
            "before": before
        }
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', required=True, help='Input directory containing PDDL files')
    parser.add_argument('--output_dir', required=True, help='Output directory for JSON files')
    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Process all PDDL files in the input directory
    for filename in os.listdir(args.input_dir):
        if filename.endswith('.pddl'):
            input_path = os.path.join(args.input_dir, filename)
            output_filename = f"{filename[:-5]}.json"
            output_path = os.path.join(args.output_dir, output_filename)

            with open(input_path, 'r', encoding='utf-8') as f:
                pddl_content = f.read()

            json_data = pddl_to_json(pddl_content)

            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=4)

            print(f"Converted {filename} to {output_filename}")

if __name__ == "__main__":
    main()