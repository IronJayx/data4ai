def save_jsonl(jsonl_str, filename):
    with open(filename, 'w') as f:
        f.write(jsonl_str)
    return filename
