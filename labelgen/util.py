import json


def append_dict_to_df(df, dict_list):
    for col in set(k for d in dict_list for k in d):
        df[col] = [d.get(col, None) for d in dict_list]
    return df


def extract_json_from_string(input_string):
    # fix bug with anyscale/mixtral
    input_string = input_string.replace("\\", "")
    start_index = input_string.find('{')

    if start_index != -1:
        substring = input_string[start_index:]
        end_index = substring.find('}')
        if end_index > 0:
            json_string = substring[:end_index + 1]
            return json.loads(json_string)
        else:
            raise json.JSONDecodeError("No closing brace found")
    else:
        raise json.JSONDecodeError("No opening brace found")
