import json


def parse_chunked_response(json_list_str: str) -> str:
    json_list = []
    for json_obj in json_list_str.split("}"):
        if json_obj:
            json_list.append(json.loads(json_obj + "}"))

    return "".join([val["content"] for val in json_list])
