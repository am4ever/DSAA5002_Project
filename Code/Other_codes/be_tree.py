import json
import os

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def print_tree(node, indent=0, file_out=None):
    node_info = f"{' ' * indent}- Depth: {node['depth']}, Type: {node['node_type']}, Child count: {node['child_count']}, Expand num: {node['expand_num']}\n"
    file_out.write(node_info)
    
    if node['child_count'] == 0 and 'observation' in node:
        observation = node['observation']
        if isinstance(observation, dict) and 'response' in observation:
            file_out.write(f"{' ' * (indent + 2)}Response: {observation['response']}\n")
        else:
            file_out.write(f"{' ' * (indent + 2)}Observation: {observation}\n")

    if 'children' in node:
        for child in node['children']:
            print_tree(child, indent + 2, file_out=file_out)

def generate_tree_visualization_from_json(file_path, output_dir):
    data = read_json_file(file_path)
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_file_path = os.path.join(output_dir, f"{base_name}.txt")
    
    with open(output_file_path, 'w') as file_out:
        if "answer_generation" in data and "query" in data["answer_generation"]:
            print(f"Query: {data['answer_generation']['query']}", file=file_out)
        
        if 'tree' in data and 'tree' in data['tree']:
            print("\nTree visualization:", file=file_out)
            print_tree(data['tree']['tree'], file_out=file_out)
        else:
            print("No proper tree structure found in the provided JSON data.", file=file_out)

def process_all_json_files(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        if filename.endswith(".json"):
            file_path = os.path.join(input_dir, filename)
            generate_tree_visualization_from_json(file_path, output_dir)

input_dir = '/hpc2hdd/home/ychen151/ToolBench/toolllama_dfs_inference_result/'
output_dir = '/hpc2hdd/home/ychen151/ToolBench/toolllama_dfs_inference_result_txt/'

process_all_json_files(input_dir, output_dir)