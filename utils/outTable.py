import json
from http.client import *
from time import *

def print_table(json_string):
    try:
        json_data = json.loads(json_string)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return

    if not json_data:
        print("No data to display.")
        return

    # Get all unique keys to use as headers
    headers = list(json_data[0].keys())
    for item in json_data:
        for key in item.keys():
            if key not in headers:
                headers.append(key)

    # Calculate maximum column widths
    column_widths = {header: len(header) for header in headers}
    for item in json_data:
        for header in headers:
            column_widths[header] = max(
                column_widths[header], len(str(item.get(header, "")))
            )

    # Print header row
    header_row = " | ".join(
        [header.ljust(column_widths[header]) for header in headers]
    )
    print(header_row)
    print("-" * len(header_row))

    # Print data rows
    for item in json_data:
        row = " | ".join(
            [
                str(item.get(header, "")).ljust(column_widths[header])
                for header in headers
            ]
        )
        print(row)

def print_table_framed(json_string, padding=2):
    try:
        json_data = json.loads(json_string)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return

    if not json_data:
        print("No data to display.")
        return

    # Get all unique keys to use as headers
    headers = list(json_data[0].keys())
    for item in json_data:
        for key in item.keys():
            if key not in headers:
                headers.append(key)

    # Calculate maximum content width for each column
    column_content_widths = {header: len(header) for header in headers}
    for item in json_data:
        for header in headers:
            column_content_widths[header] = max(
                column_content_widths[header], len(str(item.get(header, "")))
            )

    # Calculate final padded width for each column
    padded_column_widths = {
        header: width + 2 * padding
        for header, width in column_content_widths.items()
    }

    # Calculate the width of the content area *inside* the frame
    # Sum of all padded column widths + (number of columns - 1) * 3 for " | " or " │ " separators
    inner_content_width = (
        sum(padded_column_widths.values()) + (len(headers) - 1) * 3
    )

    # The total line length including the outer frame characters and spaces
    # 2 for the ' ╔' and '╗ ' (or similar) on the outside
    # 2 for the '║ ' and ' ║' within the rows
    total_line_length = inner_content_width + 4

    # Top border
    print(" " + "╔" + "═" * (total_line_length - 2) + "╗" + " ")

    # Print header row
    header_parts = []
    for header in headers:
        header_parts.append(header.center(padded_column_widths[header]))
    header_row_content = " | ".join(header_parts)
    print(" ║ " + header_row_content.ljust(inner_content_width - 2) + " ║ ")

    # Separator line
    separator_parts = []
    for header in headers:
        separator_parts.append("═" * padded_column_widths[header])
    separator_line_content = "═╧═".join(separator_parts)
    print(" ╠" + "═" + separator_line_content.ljust(total_line_length - 4) + "═" + "╣" + " ")

    # Print data rows
    for item in json_data:
        row_parts = []
        for header in headers:
            value = str(item.get(header, ""))
            # You changed this to center, keeping it consistent with headers
            row_parts.append(value.center(padded_column_widths[header]))
        row_content = " │ ".join(row_parts)
        print(" ║ " + row_content.ljust(inner_content_width) + " ║ ")

    # Bottom border
    print(" " + "╚" + "═" * (total_line_length - 2) + "╝" + " ")


while True:
    conn = HTTPConnection(host='localhost', port=5000, timeout=10)
    conn.request("GET", "/i_venture_forth_to_hunt?*", headers={"Host": "localhost:5000",  "Content-Type": "application/json"})
    
    data = conn.getresponse().read().decode("utf-8")

    print("\033[1J")
    print_table_framed(data,2)

    sleep(4.5)