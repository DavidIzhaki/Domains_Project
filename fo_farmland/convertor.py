import os
import re
import json
import argparse
from collections import defaultdict


def parse_pddl(file_path):
    with open(file_path, "r") as f:
        content = f.read()

    # === 1. Extract farm names ===
    objects_match = re.search(r"\(:objects\s+(.*?)\)", content, re.DOTALL)
    farms = re.findall(r"(\w+)", objects_match.group(1).split('-')[0]) if objects_match else []

    # === 2. Extract initial values ===
    init_matches = re.findall(r"\(= \(x (\w+)\) ([\d.]+)\)", content)
    state_farms = [{"name": name, "value": int(float(val))} for name, val in init_matches]

    # === 3. Extract adjacency ===
    adj = defaultdict(list)
    for match in re.findall(r"\(adj (\w+) (\w+)\)", content):
        adj[match[0]].append(match[1])

    # === 4. Extract all (* weight (x farm)) terms ===
    farm_exprs = re.findall(r"\(\*\s*([\d.]+)\s*\(x\s+(\w+)\)\)", content)
    if not farm_exprs:
        raise ValueError("❌ Could not find any weighted expressions")

    farm_terms = [
        {
            "farm_name": farm,
            "farm_constant": float(weight)
        }
        for weight, farm in farm_exprs
    ]


     # === 5. Extract RHS even when wrapped in (- (...sum...) (cost))
    rhs = None

    # Try to match the subtraction structure: (>= (- (...sum...) (cost)) <rhs>)
    subtracted_match = re.search(
        r"\(>=\s*\(-\s*\(.*?\)\s*\(cost\)\)\s*([\d.]+)\)", content, re.DOTALL
    )

    if subtracted_match:
        rhs = int(float(subtracted_match.group(1)))
        
    else:
        # fallback for older-style goals
        for line in content.splitlines():
            if "(*" in line and "(x " in line and ")" in line:
                number_matches = re.findall(r"([\d.]+)\)?\s*$", line.strip())
                if number_matches:
                    rhs = int(float(number_matches[-1]))

    if rhs is None:
        raise ValueError("❌ Could not locate goal RHS")



    # === 6. Build goal ===
    goal = {
        "farms": farm_terms,
        "operator": ">=",
        "value": rhs
    }

    # === 7. Return full result with number_of_cars ===
    return {
        "state": {
            "farms": state_farms,
            "number_of_cars": 0,
            "cost": 0
        },
        "problem": {
            "adj": dict(adj),
            "goal": goal
        }
    }



def convert_folder(pddl_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(pddl_dir):
        if filename.endswith(".pddl"):
            full_path = os.path.join(pddl_dir, filename)
            json_data = parse_pddl(full_path)

            out_filename = filename.replace(".pddl", ".json")
            with open(os.path.join(output_dir, out_filename), "w") as f:
                json.dump(json_data, f, indent=2)
            print(f"✔ Converted {filename} → {out_filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("pddl_dir", help="Directory with .pddl problem files")
    parser.add_argument("output_dir", help="Where to save .json files")
    args = parser.parse_args()

    convert_folder(args.pddl_dir, args.output_dir)

