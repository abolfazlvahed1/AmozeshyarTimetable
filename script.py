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
    headers = None  # Initialize headers as None
    data_rows = []  # Store all data rows

    file_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".html")]

    # Process each file
    for file_path in file_paths:
        with open(file_path, "rb") as file:  # Open in binary mode
            try:
                content = file.read().decode("utf-8", errors="replace")
                soup = BeautifulSoup(content, "html.parser")


                table = soup.find("table", id="scrollable")
                if not table:
                    print(f"No table found in {file_path}")
                    continue

                # Extract data from the table
                rows = table.find_all("tr")
                for i, row in enumerate(rows):
                    cells = row.find_all(["td", "th"])
                    cell_values = [cell.get_text(strip=True) for cell in cells]
                    
                    if i == 0:  # First row contains headers
                        if headers is None:  # Only set headers if not already set
                            headers = cell_values
                    else:
                        if len(cell_values) == len(headers):  # Only add rows with correct number of columns
                            data_rows.append(cell_values)

            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                continue

    if not headers or not data_rows:
        print("No course data found.")
        return {}

    # Create column index mapping
    try:
        columns = {
            "course_code": headers.index("كد درس"),
            "course_name": headers.index("نام درس"),
            "day_time": headers.index("زمانبندي تشکيل کلاس"),
            "professor": headers.index("استاد"),
            "theory_units": headers.index("تعداد واحد نظري"),
            "practical_units": headers.index("تعداد واحد عملي"),
            "class_name": headers.index("نام كلاس درس"),
            "section": headers.index("مقطع ارائه درس"),
            "class_code": headers.index("كد ارائه کلاس درس"),
            "exam": headers.index("زمان امتحان"),
            "place": headers.index("مكان برگزاري"),
        }
    except ValueError as e:
        print(f"Required column not found in headers: {e}")
        return {}

    filtered_courses = []
    for row in data_rows:
        if len(row) > max(columns.values()):
            course_code = row[columns["course_code"]]
            if not course_codes or course_code in course_codes:
                try:
                    theory_units = float(row[columns["theory_units"]] or 0)
                    practical_units = float(row[columns["practical_units"]] or 0)
                    total_units = theory_units + practical_units
                except ValueError:
                    print(f"Invalid unit data for course {course_code}")
                    continue

                filtered_courses.append({
                    "course_code": course_code,
                    "course_name": row[columns["course_name"]],
                    "day_time": row[columns["day_time"]] or "زمان نامشخص",
                    "professor": row[columns["professor"]] or "  ",
                    "total_units": total_units,
                    "class_name": row[columns["class_name"]] or "  ",
                    "section": row[columns["section"]] or "  ",
                    "class_code": row[columns["class_code"]] or "  ",
                    "exam": row[columns["exam"]] or "  ",
                    "place": row[columns["place"]] or "  ",
                })

    # Organize courses by weekdays
    weekly_schedule = defaultdict(list)
    for course in filtered_courses:
        day_time = course["day_time"]
        if day_time == "زمان نامشخص":
            weekly_schedule["نامشخص"].append(course)
        else:
            try:
                weekday = day_time.split(" ")[0]  # Get the first part (day name)
                full_day_name = day_mapping.get(weekday, weekday)
                weekly_schedule[full_day_name].append(course)
            except IndexError:
                weekly_schedule["نامشخص"].append(course)

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
    Write the weekly schedule to both text and HTML files.

    Args:
        weekly_schedule (dict): The weekly schedule.
        output_file (str): Path to the output file (without extension).
    """
    # Write text file
    with open(f"{output_file}.txt", "w", encoding="utf-8") as file:
        for day, courses in weekly_schedule.items():
            if courses:  # Only write days that have courses
                file.write(f"\n{day}:\n")
                for course in courses:
                    file.write(
                        f"{course['course_name']}: {course['day_time']} ({course['professor']}) - "
                        f"{course['course_code']} - {course['total_units']} واحد - "
                        f"{course['class_name']} - {course['section']}\n"
                    )

    # Write HTML file
    html_content = """
    <!DOCTYPE html>
    <html dir="rtl" lang="fa">
    <head>
        <meta charset="UTF-8">
        <title>برنامه هفتگی</title>
        <style>
            table {
                border-collapse: collapse;
                width: 100%;
                margin: 20px 0;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: right;
            }
            th {
                background-color: #f2f2f2;
            }
            tr:nth-child(even) {
                background-color: #f9f9f9;
            }
            h2 {
                color: #333;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
    """

    for day, courses in weekly_schedule.items():
        if courses:  # Only write days that have courses
            html_content += f"<h2>{day}</h2>\n"
            html_content += """
            <table>
                <tr>
                    <th>نام درس</th>
                    <th>کد درس</th>
                    <th>زمان کلاس</th>
                    <th>استاد</th>
                    <th>تعداد واحد</th>
                    <th>نام کلاس</th>
                    <th>مقطع</th>
                    <th>کد ارائه</th>
                    <th>زمان امتحان</th>
                    <th>مکان برگزاری</th>
                </tr>
            """

            for course in courses:
                html_content += f"""
                <tr>
                    <td>{course['course_name']}</td>
                    <td>{course['course_code']}</td>
                    <td>{course['day_time']}</td>
                    <td>{course['professor']}</td>
                    <td>{course['total_units']}</td>
                    <td>{course['class_name']}</td>
                    <td>{course['section']}</td>
                    <td>{course['class_code']}</td>
                    <td>{course['exam']}</td>
                    <td>{course['place']}</td>
                </tr>
                """

            html_content += "</table>\n"

    html_content += """
    </body>
    </html>
    """

    with open(f"{output_file}.html", "w", encoding="utf-8") as file:
        file.write(html_content)

if __name__ == "__main__":
    html_folder_path = "html-pages"
    # Course codes to filter
    course_codes = {
        "4628101485", "4628101498", "4628103010", "4628105776", "4628119144",
        "4628130407", "4628135451", "4628137064", "4628164617", "4628148579",
        "4628164737", "4628153620", "4628155511","90763","90610","99079","90881",
        "90763","99083"
    }
    
    # Parse HTML files and generate the schedule
    schedule = parse_html_files(html_folder_path, course_codes)

    # Write the schedule to a file
    output_file = "schedule_output.txt"
    write_schedule_to_file(schedule, output_file)

    print(f"Schedule written to {output_file}")