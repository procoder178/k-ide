import black
import isort


def format_code(code: str) -> str:
    try:
        sorted_code = isort.code(code)
        formatted_code = black.format_str(
            sorted_code, mode=black.FileMode(line_length=75)
        )
        return formatted_code
    except Exception:
        return code
