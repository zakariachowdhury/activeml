def find_index_from_list(columns, match):
    matches = [i for i, col in enumerate(columns) if match in col]
    return matches[0] if len(matches) else -1