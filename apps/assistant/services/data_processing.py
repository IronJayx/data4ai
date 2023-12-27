import os
import datetime


def split_into_files(url_text_dict, output_dir, source_name, max_files=19, max_size_mb=512):
    url_count = len(url_text_dict)
    current_file_num = 1
    current_file_size = 0
    current_data = []
    created_files = []  # List to store paths of created files

    current_date = datetime.datetime.now().strftime('%Y%m%d')

    def write_current_data():
        nonlocal current_file_num, current_file_size, current_data
        if current_data:
            filename = f'{current_date}-{source_name}-doc_{current_file_num}.txt'
            file_path = os.path.join(output_dir, filename)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write("\n--------------------------\n".join(current_data))
            created_files.append(file_path)  # Add file path to the list
            current_file_num += 1
            current_data = []
            current_file_size = 0

    # Calculate the minimum number of items per file
    min_items_per_file = max(1, url_count // max_files)
    # Items that would be left if we just distributed min_items_per_file
    extra_items = url_count % max_files

    for url, text in url_text_dict.items():
        entry = f"web_url: {url}\n\ncontent: {text}"
        entry_size = len(entry.encode('utf-8'))

        # Decide if we need to write current data to a file
        if (current_file_size + entry_size > max_size_mb * 1024 * 1024) or \
           (len(current_data) >= min_items_per_file and (extra_items == 0 or current_file_num <= extra_items)):
            write_current_data()

        current_data.append(entry)
        current_file_size += entry_size

    write_current_data()  # Write remaining data to file

    return set(created_files)


def analyze_dict(url_text_dict):
    """
    Takes a dictionary with keys and values.
    Returns the number of items and the total size in MB of all texts.
    """
    total_size_mb = 0
    num_items = len(url_text_dict.keys())

    for text in url_text_dict.values():
        # Compute the size in MB for each text
        size_mb = len(text.encode('utf-8')) / 1024 / 1024
        total_size_mb += size_mb

    return num_items, total_size_mb
