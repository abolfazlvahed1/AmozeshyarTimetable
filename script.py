import os
from bs4 import BeautifulSoup
from collections import defaultdict


# Mapping of abbreviated day names to full names for "سه" and "پنج"
day_mapping = {
    "سه": "سه شنبه",
    "پنج": "پنج شنبه"
}

def parse_html_files(folder_path, course_codes):
    """
    Parse all HTML files in the specified folder to extract course data.

    Args:
        folder_path (str): Path to the folder containing HTML files.
        course_codes (set): Set of course codes to filter data. If empty, include all courses.

    Returns:
        dict: A dictionary representing the weekly schedule.
    """
    all_courses = []
    file_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".html")]

    # Process each file
    for file_path in file_paths:
        with open(file_path, "rb") as file:  # Open in binary mode
            try:
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
    headers = all_courses[0]  # The first row is treated as headers
    data_rows = all_courses[1:]  # Skip the header row

    columns = {
        "course_code": headers.index("كد درس"),
        "course_name": headers.index("نام درس"),
        "day_time": headers.index("زمانبندي تشکيل کلاس"),
        "professor": headers.index("استاد"),
        "theory_units": headers.index("تعداد واحد نظري"),
        "practical_units": headers.index("تعداد واحد عملي"),
    }

    filtered_courses = []
    for row in data_rows:
        if len(row) > max(columns.values()):
            course_code = row[columns["course_code"]]
            if not course_codes or course_code in course_codes:  # Include all courses if course_codes is empty
                try:
                    total_units = (
                        float(row[columns["theory_units"]] or 0) + float(row[columns["practical_units"]] or 0)
                    )
                except ValueError:
                    # Handle invalid data gracefully by skipping the row
                    # print(f"Invalid unit data in row: {row}")
                    continue

                filtered_courses.append({
                    "course_code": course_code,
                    "course_name": row[columns["course_name"]],
                    "day_time": row[columns["day_time"]] or "زمان نامشخص",
                    "professor": row[columns["professor"]] or "خالی",
                    "total_units": total_units,
                })

    # Organize courses by weekdays
    weekly_schedule = defaultdict(list)
    for course in filtered_courses:
        day_time = course["day_time"]
        if day_time == "زمان نامشخص":
            weekly_schedule["نامشخص"].append(course)
        else:
            # Use the day mapping to get the full name of the day
            weekday = day_time.split(" ")[0]  # Get the first part, which is the day name (e.g., "سه")
            full_day_name = day_mapping.get(weekday, weekday)  # Keep the day name unchanged unless it's "سه" or "پنج"
            weekly_schedule[full_day_name].append(course)

    # Ensure the order of days in the schedule
    ordered_schedule = {
        "شنبه": [],
        "يكشنبه": [],
        "دوشنبه": [],
        "سه شنبه": [],
        "چهارشنبه": [],
        "پنج شنبه": [],
        "جمعه": [],
        "نامشخص": [],
    }

    # Sort courses into the correct day order
    for day in ordered_schedule:
        ordered_schedule[day] = weekly_schedule.get(day, [])

    return ordered_schedule


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
                    f"{course['course_name']}: {course['day_time']} ({course['professor']}) - ({course ['course_code']}) - {course['total_units']} واحد\n"
                )

if __name__ == "__main__":
    html_folder_path = "html-pages"
    # Course codes to filter
    course_codes = {
        "4628101485", "4628101498", "4628103010", "4628105776", "4628119144",
        "4628130407", "4628135451", "4628137064", "4628164617", "4628148579",
        "4628164737", "4628153620", "4628155511"
    }
    # Parse HTML files and generate the schedule
    schedule = parse_html_files(html_folder_path, course_codes)

    # Write the schedule to a file
    output_file = "schedule_output.txt"
    write_schedule_to_file(schedule, output_file)

    print(f"Schedule written to {output_file}")
