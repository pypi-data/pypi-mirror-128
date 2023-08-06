import json

def load_json_file(filename):
    with open(filename) as f:
        tmp_data = f.read()
        while not (tmp_data[0].startswith('[') or tmp_data[0].startswith('{')):
            tmp_data = tmp_data[1:]
    return json.loads(tmp_data)

def write_json_file(filename, data):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file)