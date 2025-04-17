import re
import os
import json
import argparse

def remove_comments(text):
    return "\n".join(line for line in text.splitlines() if not line.strip().startswith(";"))

def parse_pddl(pddl_text):
    pddl_text = remove_comments(pddl_text)

    problem_match = re.search(r'\(define\s+\(problem\s+([^)]+)\)', pddl_text)
    problem_name = problem_match.group(1) if problem_match else "unknown"

    domain_match = re.search(r'\(:domain\s+([^)]+)\)', pddl_text)
    domain_name = domain_match.group(1) if domain_match else "unknown"

    objects_section = re.search(r'\(:objects(.*?)\)', pddl_text, re.DOTALL)
    objects_text = objects_section.group(1) if objects_section else ""

    places = {}
    vehicles = {}

    place_pattern = re.compile(r'([^\s]+)\s+-\s+place', re.IGNORECASE)
    vehicle_pattern = re.compile(r'([^\s]+)\s+-\s+vehicle', re.IGNORECASE)

    for place_id in place_pattern.findall(objects_text):
        places[place_id] = {
            "id": place_id,
            "available_resources": {
                "wood": 0, "timber": 0, "ore": 0, "stone": 0, "iron": 0, "coal": 0
            },
            "carts": 0,
            "housing": 0,
            "has_cabin": False,
            "has_coal_stack": False,
            "has_quarry": False,
            "has_mine": False,
            "has_sawmill": False,
            "has_ironworks": False,
            "has_docks": False,
            "has_wharf": False,
            "is_woodland": False,
            "is_mountain": False,
            "is_metalliferous": False,
            "is_by_coast": False
        }

    for vehicle_id in vehicle_pattern.findall(objects_text):
        vehicles[vehicle_id] = {
            "id": vehicle_id,
            "is_train": False,
            "is_ship": False,
            "space_in": 0,
            "available_resources": {
                "wood": 0, "timber": 0, "ore": 0, "stone": 0, "iron": 0, "coal": 0
            },
            "location": "",
            "potential": True  # default to True unless overridden
        }

    init_section = re.search(r'\(:init(.*?)\)\s*\(:goal', pddl_text, re.DOTALL)
    init_text = init_section.group(1) if init_section else ""

    connections_by_land = {}
    connections_by_sea = {}
    connections_by_rail = {}

    def parse_connections(pattern, target_dict):
        for match in pattern.findall(init_text):
            p1, p2 = match
            if p1 not in target_dict:
                target_dict[p1] = []
            target_dict[p1].append(p2)

    parse_connections(re.compile(r'\(connected-by-land\s+(\S+)\s+(\S+)\)'), connections_by_land)
    parse_connections(re.compile(r'\(connected-by-sea\s+(\S+)\s+(\S+)\)'), connections_by_sea)
    parse_connections(re.compile(r'\(connected-by-rail\s+(\S+)\s+(\S+)\)'), connections_by_rail)

    for place_id in places:
        for attr in [
            ("is_woodland", "woodland"), ("is_mountain", "mountain"),
            ("is_metalliferous", "metalliferous"), ("is_by_coast", "by-coast"),
            ("has_cabin", "has-cabin"), ("has_coal_stack", "has-coal-stack"),
            ("has_quarry", "has-quarry"), ("has_mine", "has-mine"),
            ("has_sawmill", "has-sawmill"), ("has_ironworks", "has-ironworks"),
            ("has_docks", "has-docks"), ("has_wharf", "has-wharf")
        ]:
            if re.search(rf'\({attr[1]}\s+{place_id}\)', init_text):
                places[place_id][attr[0]] = True

        if (m := re.search(rf'\(=\s+\(housing\s+{place_id}\)\s+(\d+)\)', init_text)):
            places[place_id]["housing"] = int(m.group(1))
        if (m := re.search(rf'\(=\s+\(carts-at\s+{place_id}\)\s+(\d+)\)', init_text)):
            places[place_id]["carts"] = int(m.group(1))
        for r in places[place_id]["available_resources"]:
            if (m := re.search(rf'\(=\s+\(available\s+{r}\s+{place_id}\)\s+(\d+)\)', init_text)):
                places[place_id]["available_resources"][r] = int(m.group(1))

    for vehicle_id in vehicles:
        if re.search(rf'\(is-train\s+{vehicle_id}\)', init_text):
            vehicles[vehicle_id]["is_train"] = True
        if re.search(rf'\(is-ship\s+{vehicle_id}\)', init_text):
            vehicles[vehicle_id]["is_ship"] = True
        if re.search(rf'\(potential\s+{vehicle_id}\)', init_text):
            vehicles[vehicle_id]["potential"] = True
        if (m := re.search(rf'\(is-at\s+{vehicle_id}\s+(\S+)\)', init_text)):
            vehicles[vehicle_id]["location"] = m.group(1)
        if (m := re.search(rf'\(=\s+\(space-in\s+{vehicle_id}\)\s+(\d+)\)', init_text)):
            vehicles[vehicle_id]["space_in"] = int(m.group(1))
        for r in vehicles[vehicle_id]["available_resources"]:
            if (m := re.search(rf'\(=\s+\(available\s+{r}\s+{vehicle_id}\)\s+(\d+)\)', init_text)):
                vehicles[vehicle_id]["available_resources"][r] = int(m.group(1))

    labour = int(re.search(r'\(=\s+\(labour\)\s+(\d+)\)', init_text).group(1)) if "labour" in init_text else 0
    resource_use = int(re.search(r'\(=\s+\(resource-use\)\s+(\d+)\)', init_text).group(1)) if "resource-use" in init_text else 0
    pollution = int(re.search(r'\(=\s+\(pollution\)\s+(\d+)\)', init_text).group(1)) if "pollution" in init_text else 0

    # Extract goal section
    goal_section = re.search(r'\(:goal\s+(.*?)\s*(?:\(:|\)$)', pddl_text, re.DOTALL)
    goal_text = goal_section.group(1).strip() if goal_section else ""
    
    # If goal is wrapped in (and ...), extract the inner content
    if goal_text.startswith("(and"):
        goal_text = goal_text[4:-1].strip()
    
    # Parse goal conditions
    goal_conditions = []
    
    # Define a function to extract nested expressions with balanced parentheses
    def extract_expressions(text):
        expressions = []
        paren_level = 0
        current_expr = ""
        
        for char in text:
            if char == '(':
                paren_level += 1
                current_expr += char
            elif char == ')':
                paren_level -= 1
                current_expr += char
                if paren_level == 0:
                    expressions.append(current_expr.strip())
                    current_expr = ""
            elif paren_level > 0:
                current_expr += char
            elif not char.isspace() and paren_level == 0:
                # Start a new expression
                current_expr = char
                
        return [expr for expr in expressions if expr]
    
    # Extract all goal expressions
    goal_expressions = extract_expressions(goal_text)
    
    # Process each goal expression
    for expr in goal_expressions:
        # Handle numeric goals like (>= (housing location1) 2)
        housing_match = re.match(r'\(>=\s*\(\s*housing\s+(\S+)\s*\)\s*(\d+)\s*\)', expr)
        if housing_match:
            place_id, amount = housing_match.groups()
            goal_conditions.append({
                "attribute": "housing",
                "place_id": place_id,
                "required_amount": int(amount)
            })
            continue
        
        # Handle resource goals like (>= (available timber location1) 1)
        resource_match = re.match(r'\(>=\s*\(\s*available\s+(\S+)\s+(\S+)\s*\)\s*(\d+)\s*\)', expr)
        if resource_match:
            resource, place_id, amount = resource_match.groups()
            goal_conditions.append({
                "place_id": place_id,
                "resource": resource,
                "required_amount": int(amount)
            })
            continue
        
        # Handle carts goals like (>= (carts-at location1) 2)
        carts_match = re.match(r'\(>=\s*\(\s*carts-at\s+(\S+)\s*\)\s*(\d+)\s*\)', expr)
        if carts_match:
            place_id, amount = carts_match.groups()
            goal_conditions.append({
                "attribute": "carts-at",
                "place_id": place_id,
                "required_amount": int(amount)
            })
            continue
        
        # Handle connection goals like (connected-by-rail location1 location2)
        connection_match = re.match(r'\((\S+-by-\S+)\s+(\S+)\s+(\S+)\)', expr)
        if connection_match:
            predicate, from_loc, to_loc = connection_match.groups()
            goal_conditions.append({
                "predicate": predicate,
                "from": from_loc,
                "to": to_loc
            })
            continue
        
        # Handle predicate goals like (has-sawmill location1)
        predicate_match = re.match(r'\((\S+)\s+(\S+)\)', expr)
        if predicate_match:
            predicate, arg = predicate_match.groups()
            # Skip if this is part of a more complex expression we've already handled
            if predicate not in [">=", "and", "or", "not"] and predicate != "housing":
                goal_conditions.append({
                    "predicate": predicate,
                    "argument": arg
                })
    
    # If no goals were found, try a more direct approach
    if not goal_conditions and goal_section:
        # Try to find all housing goals
        housing_pattern = re.compile(r'\(>=\s*\(\s*housing\s+(\S+)\s*\)\s*(\d+)\s*\)')
        for place_id, amount in housing_pattern.findall(goal_section.group(0)):
            goal_conditions.append({
                "attribute": "housing",
                "place_id": place_id,
                "required_amount": int(amount)
            })
        
        # Try to find all resource goals
        resource_pattern = re.compile(r'\(>=\s*\(\s*available\s+(\S+)\s+(\S+)\s*\)\s*(\d+)\s*\)')
        for resource, place_id, amount in resource_pattern.findall(goal_section.group(0)):
            goal_conditions.append({
                "place_id": place_id,
                "resource": resource,
                "required_amount": int(amount)
            })
        
        # Try to find all predicate goals
        predicate_pattern = re.compile(r'\((\S+)\s+(\S+)\)')
        for predicate, arg in predicate_pattern.findall(goal_section.group(0)):
            if predicate not in [">=", "and", "or", "not", "housing"] and not any(
                c.get("predicate") == predicate and c.get("argument") == arg 
                for c in goal_conditions
            ):
                goal_conditions.append({
                    "predicate": predicate,
                    "argument": arg
                })
    
    return {
        "state": {
            "places": places,
            "vehicles": vehicles,
            "labour": labour,
            "resource_use": resource_use,
            "pollution": pollution,
            "connections_by_rail": connections_by_rail
        },
        "problem": {
            "goal": { "conditions": goal_conditions },
            "connections_by_land": connections_by_land,
            "connections_by_sea": connections_by_sea
        }
    }

def process_directory(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".pddl") and not filename.lower().startswith("domain"):
            with open(os.path.join(input_dir, filename), "r") as infile:
                parsed = parse_pddl(infile.read())
            out_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".json")
            with open(out_path, "w") as outfile:
                json.dump(parsed, outfile, indent=2)
            print(f"Converted {filename} to {out_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', default='problems_pddl')
    parser.add_argument('--output_dir', default='problems_json')
    args = parser.parse_args()
    process_directory(args.input_dir, args.output_dir)
