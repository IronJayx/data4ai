import json

def to_json(system_message, input_list, output_list):
    json_list = []
    for inp, out in zip(input_list, output_list):
        json_obj = {
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": inp},
                {"role": "assistant", "content": out}
            ]
        }
        json_list.append(json_obj)
    return json_list

def to_json_l(json_list):
    jsonl_str = ''
    for obj in json_list:
        jsonl_str += json.dumps(obj) + '\n'
    return jsonl_str
