import os
from bs4 import BeautifulSoup
from collections import defaultdict


# Mapping of abbreviated day names to full names for "سه" and "پنج"
day_mapping = {
    "سه": "سه شنبه",
    "پنج": "پنج شنبه"
}

def parse_html_files(folder_path):
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
    Write the weekly schedule to HTML file with advanced features.
    """

    # Create all-courses view (sorted by name)
    all_courses = []
    for courses in weekly_schedule.values():
        all_courses.extend(courses)
    
    # Sort all courses by name
    all_courses.sort(key=lambda x: x['course_name'])

    # HTML content
    html_content = """
    <!DOCTYPE html>
    <html dir="rtl" lang="fa">
    <head>
        <meta charset="UTF-8">
        <title>برنامه کلاس‌ها</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #f5f5f5;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .controls {
                margin-bottom: 20px;
                padding: 15px;
                background-color: #f8f9fa;
                border-radius: 5px;
            }
            .view-controls {
                margin-bottom: 15px;
            }
            .filter-controls {
                margin-bottom: 15px;
            }
            input[type="text"] {
                width: 100%;
                padding: 8px;
                margin-bottom: 10px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            .button {
                padding: 8px 15px;
                margin-right: 10px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                background-color: #007bff;
                color: white;
            }
            .button:hover {
                background-color: #0056b3;
            }
            .button.active {
                background-color: #0056b3;
            }
            table {
                border-collapse: collapse;
                width: 100%;
                margin: 20px 0;
                background-color: white;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 12px 8px;
                text-align: right;
            }
            th {
                background-color: #f2f2f2;
                position: sticky;
                top: 0;
            }
            tr:nth-child(even) {
                background-color: #f9f9f9;
            }
            .view {
                display: none;
            }
            .view.active {
                display: block;
            }
            h2 {
                color: #333;
                margin-top: 20px;
                border-bottom: 2px solid #007bff;
                padding-bottom: 5px;
            }
            .help-text {
                color: #666;
                font-size: 0.9em;
                margin-bottom: 10px;
            }
            .course-group {
                margin-bottom: 30px;
            }
            .hidden {
                display: none !important;
            }
        </style>
    </head>
    <body>
    <div class="container">
        <div class="controls">
            <div class="view-controls">
                <button class="button active" onclick="switchView('weekly')">نمایش هفتگی</button>
                <button class="button" onclick="switchView('all')">نمایش همه دروس</button>
            </div>
            <div class="filter-controls">
                <div class="help-text">
                    برای فیلتر کردن، کد درس یا نام درس را وارد کنید. برای چندین مورد از خط تیره (-) استفاده کنید.
                    <br>
                    مثال: 4628101485 - ریاضی
                </div>
                <input type="text" id="filterInput" placeholder="فیلتر بر اساس کد یا نام درس..." oninput="filterCourses()">
            </div>
        </div>

        <div id="weeklyView" class="view active">
    """

    # Add weekly view content
    for day, courses in weekly_schedule.items():
        if courses:
            html_content += f"<h2>{day}</h2>\n"
            html_content += create_table(courses)

    # Add all courses view
    html_content += """
        </div>
        <div id="allView" class="view">
            <h2>تمام دروس</h2>
            <table>
                <thead>
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
                </thead>
                <tbody>
    """

    # Add all courses in one table
    for course in all_courses:
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

    html_content += """
                </tbody>
            </table>
        </div>
    """




    # Add JavaScript for functionality
    html_content += """
        </div>
    </div>
<script>
    function switchView(viewName) {
        // Update buttons
        document.querySelectorAll('.view-controls .button').forEach(btn => {
            btn.classList.remove('active');
        });
        event.target.classList.add('active');
        
        // Update views
        document.querySelectorAll('.view').forEach(view => {
            view.classList.remove('active');
        });
        document.getElementById(viewName + 'View').classList.add('active');
        
        // Reapply current filter
        filterCourses();
    }

    function filterCourses() {
        const filterValue = document.getElementById('filterInput').value.trim();
        const filters = filterValue.split('-').map(f => f.trim()).filter(f => f);
        
        // Function to check if course matches any filter
        const matchesCourse = (courseRow) => {
            if (filters.length === 0) return true;
            const text = courseRow.textContent.toLowerCase();
            return filters.some(filter => 
                text.includes(filter.toLowerCase())
            );
        };

        // Apply filter to active view
        const activeView = document.querySelector('.view.active');
        
        if (activeView.id === 'weeklyView') {
            // Filter weekly view
            activeView.querySelectorAll('tr:not(:first-child)').forEach(row => {
                row.classList.toggle('hidden', !matchesCourse(row));
            });
            
            // Hide empty day sections
            activeView.querySelectorAll('h2').forEach(header => {
                const table = header.nextElementSibling;
                const visibleRows = table.querySelectorAll('tr:not(.hidden)').length - 1; // -1 for header row
                header.style.display = visibleRows > 0 ? '' : 'none';
                table.style.display = visibleRows > 0 ? '' : 'none';
            });
        } else if (activeView.id === 'allView') {
            // Filter all courses view
            const rows = activeView.querySelectorAll('table tbody tr');
            rows.forEach(row => {
                row.classList.toggle('hidden', !matchesCourse(row));
            });
        }
    }
</script>

    </body>
    </html>
    """

    with open(f"{output_file}.html", "w", encoding="utf-8") as file:
        file.write(html_content)

def create_table(courses):
    """Helper function to create HTML table for courses."""
    return f"""
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
        {''.join(f"""
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
        """ for course in courses)}
    </table>
    """

if __name__ == "__main__":
    html_folder_path = "html-pages"
    
    # Parse HTML files and generate the schedule
    schedule = parse_html_files(html_folder_path)

    # Write the schedule to a file
    output_file = "schedule_output"
    write_schedule_to_file(schedule, output_file)

    print(f"Schedule written to {output_file}")