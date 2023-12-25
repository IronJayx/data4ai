import json


def to_openai_finetune(system_message: str, messages: dict):
    json_list = []
    for discussion_id, messages in messages.items():
        # Prepend the system message to the discussion
        discussion_with_system_message = [
            {"role": "system", "content": system_message}] + messages

        # Create a JSON object for the discussion
        json_obj = {
            "messages": discussion_with_system_message
        }
        json_list.append(json_obj)

    return json_list


def to_json_l(json_list):
    jsonl_str = ''
    for obj in json_list:
        jsonl_str += json.dumps(obj) + '\n'
    return jsonl_str
