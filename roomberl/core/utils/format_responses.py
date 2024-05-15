from typing import Dict


def get_status_message(status_code: int) -> str:
    if status_code < 400:
        return "success"
    else:
        return "failed"


def format_response_data(data: Dict, status_code: int = None) -> Dict:
    return {
        "status": get_status_message(status_code) if status_code else "",
        "data": data,
    }


def add_space_after_capital(input_string):
    result = ""
    for char in input_string:
        if char.isupper():
            result += " " + char
        else:
            result += char
    return result.strip()
