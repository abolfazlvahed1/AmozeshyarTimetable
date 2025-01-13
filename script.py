import os
from bs4 import BeautifulSoup
from collections import defaultdict

def parse_html_files(file_paths, course_codes):
    """
    Parse multiple HTML files to extract course data for specified course codes.

    Args:
        file_paths (list): List of paths to HTML files.
        course_codes (set): Set of course codes to filter data.

    Returns:
        dict: A dictionary representing the weekly schedule.
    """
    all_courses = []

    # Process each file
    for file_path in file_paths:
        with open(file_path, "rb") as file:  # Open in binary mode
            try:
                # Decode content to UTF-8, replacing invalid bytes
                content = file.read().decode("utf-8", errors="replace")
                soup = BeautifulSoup(content, "html.parser")

                # Locate the table inside the specified div
                table_container = soup.find("div", id="tableContainer")
                if not table_container:
                    print(f"No table container found in {file_path}")
                    continue

                table = table_container.find("table", id="scrollable")
                if not table:
                    print(f"No table found in {file_path}")
                    continue

                # Extract data from the table
                rows = table.find_all("tr")
                for row in rows:
                    cells = row.find_all(["td", "th"])
                    cell_values = [cell.get_text(strip=True) for cell in cells]
                    all_courses.append(cell_values)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                continue

    if not all_courses:
        print("No course data found.")
        return {}

    # Extract headers and filter valid rows
    headers = all_courses[0]
    data_rows = all_courses[1:]

    columns = {
        "course_code": headers.index("كد درس"),
        "course_name": headers.index("نام درس"),
        "day_time": headers.index("زمانبندي تشکيل کلاس"),
        "professor": headers.index("استاد"),
        "theory_units": headers.index("تعداد واحد نظري"),
        "practical_units": headers.index("تعداد واحد عملي"),
    }

    # Filter rows based on course codes and clean data
    filtered_courses = []
    for row in data_rows:
        if len(row) > max(columns.values()):
            course_code = row[columns["course_code"]]
            if course_code in course_codes:
                total_units = (
                    int(row[columns["theory_units"]] or 0) + int(row[columns["practical_units"]] or 0)
                )
                filtered_courses.append({
                    "course_code": course_code,
                    "course_name": row[columns["course_name"]],
                    "day_time": row[columns["day_time"]],
                    "professor": row[columns["professor"]],
                    "total_units": total_units,
                })

    # Organize courses by weekdays
    weekly_schedule = defaultdict(list)
    for course in filtered_courses:
        weekday = course["day_time"].split(" ")[0]
        weekly_schedule[weekday].append(course)

    return weekly_schedule
def pad_string(s, length):
    return s + ' ' * (length - len(unicodedata.normalize('NFC', s)))
def write_schedule_to_file(weekly_schedule, output_file):
    """
    Write the weekly schedule to a file.

    Args:
        weekly_schedule (dict): The weekly schedule.
        output_file (str): Path to the output file.
    """
    with open(output_file, "w", encoding="utf-8") as file:
        for day, courses in weekly_schedule.items():
            file.write(f"\n{day}:\n")
            for course in courses:
                file.write(
                    f"{course['course_name']}: {course['day_time']} ({course['professor']}) - {course['total_units']} واحد\n"
                )

if __name__ == "__main__":
    # Example usage

    # Paths to HTML files
    html_file_paths = ["سيستم آموزشیار - دانشجویی.html","سيستم آموزشیار - دانشجویی2.html"]  # Add more file paths as needed


    # Course codes to filter
    course_codes = {
        "4628101485", "4628101498", "4628103010", "4628105776", "4628119144",
        "4628130407", "4628135451", "4628137064", "4628164617", "4628148579",
        "4628164737", "4628153620", "4628155511"
    }

    # Parse HTML files and generate the schedule
    schedule = parse_html_files(html_file_paths, course_codes)

    # Write the schedule to a file
    output_file = "schedule_output.txt"
    write_schedule_to_file(schedule, output_file)

    print(f"Schedule written to {output_file}")
