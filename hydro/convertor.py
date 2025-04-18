import re
import json
import os
import argparse


def extract_time_objects(pddl_string):
    time_objects = []
    objects_match = re.search(r'\(:objects(.*?)\)', pddl_string, re.DOTALL | re.IGNORECASE)
    if objects_match:
        objects_text = objects_match.group(1)
        for line in objects_text.splitlines():
            line = line.strip()
            if line.endswith("- time"):
                parts = line.rsplit(" -", 1)
                if parts:
                    tokens = parts[0].strip().split()
                    time_objects.extend(tokens)
    return time_objects

def extract_current_time(pddl_string):
    match = re.search(r'\(timenow\s+(t\d+)\)', pddl_string, re.IGNORECASE)
    if match:
        return match.group(1)
    return None

def pddl_to_json(pddl_string):
    """Convert PDDL text to structured JSON with demand and before as vectors."""
    flags = re.IGNORECASE

    node_mapping = {}
    for match in re.findall(r'\(=\s+\(value\s+(n\d+)\)\s+(\d+)\)', pddl_string, flags):
        node, value = match
        node_mapping[node] = int(value)

    funds_match = re.search(r'\(=\s+\(funds\)\s+(\d+)\)', pddl_string, flags)
    funds = int(funds_match.group(1)) if funds_match else None

    capacity_match = re.search(r'\(=\s+\(stored_capacity\)\s+(\d+)\)', pddl_string, flags)
    capacity = int(capacity_match.group(1)) if capacity_match else None

    goal_match = re.search(r'\(\>=\s+\(funds\)\s+(\d+)\)', pddl_string, flags)
    goal_funds = int(goal_match.group(1)) if goal_match else None

    time_objects = extract_time_objects(pddl_string)
    time_index_map = { time_sym: idx for idx, time_sym in enumerate(time_objects) }

    current_time = extract_current_time(pddl_string)
    current_time_index = time_index_map.get(current_time, 0)

    # Determine length for the vectors
    time_len = len(time_index_map)
    demands = [0] * time_len
    before = [None] * time_len

    for time_sym, node_sym in re.findall(r'\(demand\s+(t\d+)\s+(n\d+)\)', pddl_string, flags):
        if time_sym in time_index_map and node_sym in node_mapping:
            t_idx = time_index_map[time_sym]
            demands[t_idx] = node_mapping[node_sym]

    for t1, t2 in re.findall(r'\(before\s+(t\d+)\s+(t\d+)\)', pddl_string, flags):
        if t1 in time_index_map and t2 in time_index_map:
            from_idx = time_index_map[t1]
            to_idx = time_index_map[t2]
            before[from_idx] = to_idx

    return {
        "state": {
            "current_time": current_time_index,
            "funds": funds,
            "stored_capacity": capacity,
            "stored_units": 0
        },
        "problem": {
            "goal_funds": goal_funds,
            "demand": demands,
            "before": before
        }
    }

def convert_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        pddl_content = f.read()
    json_data = pddl_to_json(pddl_content)

    # Trim trailing nulls from "before"
    while json_data["problem"]["before"] and json_data["problem"]["before"][-1] is None:
        json_data["problem"]["before"].pop()

    # Trim trailing zeros from "demand"
    while json_data["problem"]["demand"] and json_data["problem"]["demand"][-1] == 0:
        json_data["problem"]["demand"].pop()

    # Use custom encoder for compact demand & before
    class CompactVectorEncoder(json.JSONEncoder):
        def encode(self, o):
            import re

            pretty = super().encode(o)

            pretty = re.sub(
                r'"demand": \[\s*([^\]]+?)\s*\]',
                lambda m: f'"demand": [{",".join(x.strip() for x in m.group(1).split(","))}]',
                pretty,
                flags=re.DOTALL
            )
            pretty = re.sub(
                r'"before": \[\s*([^\]]+?)\s*\]',
                lambda m: f'"before": [{",".join(x.strip() for x in m.group(1).split(","))}]',
                pretty,
                flags=re.DOTALL
            )

            return pretty


    # Step 1: Write normal pretty JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=4)

    # Step 2: Post-process to compact demand & before arrays
    with open(output_path, 'r', encoding='utf-8') as f:
        content = f.read()

    import re

    def compact_array_field(field_name, content):
        return re.sub(
            rf'"{field_name}": \[\s*((?:\s*\d+,?\s*)+?)\s*\]',
            lambda m: f'"{field_name}": [{",".join(x.strip() for x in m.group(1).split(","))}]',
            content,
            flags=re.DOTALL
        )

    content = compact_array_field("demand", content)
    content = compact_array_field("before", content)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

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
                convert_file(
                    os.path.join(input_dir, filename),
                    os.path.join(output_dir, filename.replace(".pddl", ".json"))
                )

if __name__ == '__main__':
    main()
