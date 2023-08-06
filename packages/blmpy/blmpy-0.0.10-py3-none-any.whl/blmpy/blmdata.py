def list_2_dict(list, key_index):
    dict = {}
    for row in list:
        if key_index in row:
            dict[row[key_index]] = row
    return dict 