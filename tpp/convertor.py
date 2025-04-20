#!/usr/bin/env python3
import re
import json
import os
import sys

def convert_location(loc_str):
    """Converts a location string to a string value:
       - 'depotX' → "-1"
       - 'marketY' → str(Y‑1)
       Otherwise returns loc_str unchanged."""
    if loc_str.startswith("depot"):
        return "-1"
    elif loc_str.startswith("market"):
        m = re.search(r'\d+', loc_str)
        if m:
            return str(int(m.group(0)) - 1)
    return loc_str

def parse_objects(pddl_text):
    """Map each type ('truck', 'market', etc.) to its list of object names."""
    objects_by_type = {}
    m = re.search(r'\(:objects(.*?)\)', pddl_text, re.DOTALL)
    if m:
        block = m.group(1)
        for line in block.splitlines():
            line = line.strip()
            if '-' not in line or not line:
                continue
            names, typ = line.split('-',1)
            names = names.strip().split()
            typ   = typ.strip()
            objects_by_type.setdefault(typ, []).extend(names)
    return objects_by_type

def parse_truck_locations(init_section):
    """Return dict truck_name→converted_location."""
    truck_locations = {}
    for truck, loc in re.findall(r'\(loc\s+(\S+)\s+(\S+)\)', init_section, re.IGNORECASE):
        truck_locations[truck] = convert_location(loc)
    return truck_locations

def parse_market_items(init_section):
    """
    Return dict market_name→{ good_id: { 'price': float, 'on_sale': int } }
    """
    market_items = {}
    # price
    for good, market, price in re.findall(
        r'\(=\s*\(price\s+(\S+)\s+(\S+)\)\s+([\d\.]+)\)', init_section, re.IGNORECASE
    ):
        pid = re.search(r'\d+', good).group(0)
        market_items.setdefault(market,{})
        market_items[market].setdefault(pid,{})["price"] = float(price)
    # on_sale
    for good, market, on_sale in re.findall(
        r'\(=\s*\(on-sale\s+(\S+)\s+(\S+)\)\s+(\d+)\)', init_section, re.IGNORECASE
    ):
        pid = re.search(r'\d+', good).group(0)
        market_items.setdefault(market,{})
        entry = market_items[market].setdefault(pid,{})
        entry["on_sale"] = int(on_sale)
        if on_sale == "0" and "price" not in entry:
            entry["price"] = 0.0
    return market_items

def parse_pddl(pddl_text):
    # strip PDDL “;;” comments
    pddl_text = re.sub(r';;.*', '', pddl_text)
    # split out :init
    parts = re.split(r'\(:goal', pddl_text, flags=re.DOTALL)
    init_section = parts[0].replace("(:init","",1)
    
    # build baseline JSON structure
    output = {
        "state": {
            "trucks": [],
            "markets": [],
            "items_bought": {},
        },
        "problem": {
            "distances": {},
            "goal": { "goal_requests": {} }
        }
    }

    # parse objects
    objs = parse_objects(pddl_text)
    # trucks
    truck_locs = parse_truck_locations(init_section)
    for t in objs.get("truck",[]):
        output["state"]["trucks"].append({
            "name": t,
            "location": truck_locs.get(t,"-1")
        })
    # markets
    market_items = parse_market_items(init_section)

   

    for m in objs.get("market", []):
        raw = market_items.get(m, {})  
        # Keep only items whose 'on_sale' count > 0
        filtered = {
            item_id: props
            for item_id, props in raw.items()
            if isinstance(props, dict) and props.get("on_sale", 0) > 0
        }

        # Skip markets with no items left
        if not filtered:
            continue

        output["state"]["markets"].append({
            "location": convert_location(m),
            "items": filtered,
        })



    # items_bought
    for good, num in re.findall(r'\(=\s*\(bought\s+(\S+)\)\s+(\d+)\)', init_section, re.IGNORECASE):
        pid = re.search(r'\d+', good).group(0)
        output["state"]["items_bought"][pid] = int(num)

    # goal_requests
    for good, num in re.findall(r'\(=\s*\(request\s+(\S+)\)\s+(\d+)\)', init_section, re.IGNORECASE):
        pid = re.search(r'\d+', good).group(0)
        output["problem"]["goal"]["goal_requests"][pid] = int(num)

    # distances → nested map from→list of [to, cost]
    distances = {}
    for frm, to, cost in re.findall(
        r'\(=\s*\(drive-cost\s+(\S+)\s+(\S+)\)\s+([\d\.]+)\)',
        init_section, re.IGNORECASE
    ):
        f = convert_location(frm)
        t = convert_location(to)
        distances.setdefault(f, []).append([t, float(cost)])
    output["problem"]["distances"] = distances

    return output

def convert_pddl_directory_to_json(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for fn in os.listdir(input_dir):
        if fn.lower().endswith(".pddl"):
            txt = open(os.path.join(input_dir,fn)).read()
            j   = parse_pddl(txt)
            out = os.path.join(output_dir, fn[:-5]+".json")
            with open(out,"w") as f:
                json.dump(j, f, indent=4)
            print(f"Converted {fn} → {os.path.basename(out)}")

if __name__=="__main__":
    if len(sys.argv)!=3:
        print("Usage: pddl_to_json.py <input_dir> <output_dir>")
        sys.exit(1)
    convert_pddl_directory_to_json(sys.argv[1], sys.argv[2])
