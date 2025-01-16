# AmozeshyarTimetable

## Prerequisites

- Python 3.x
- BeautifulSoup 4

To install BeautifulSoup, you need pip. If you don't have pip installed, you can install it using:
```sh
python -m ensurepip --upgrade
```

Once pip is installed, you can install BeautifulSoup using:
```sh
pip install beautifulsoup4
```

---

## Usage

To use this script, follow these steps:

1. **Clone this repository**:
```sh
git clone https://github.com/abolfazlvahed1/AmozeshyarTimetable.git
```
2. **Download HTML Files**: 
   If you are part of the computer group of Tehran Markaz, all offered courses have already been downloaded for you, so you can skip this step.

   For others, visit https://eserv.iau.ir/EServices/pSearchAction.do, search for your group's offered courses, and download all HTML files. If there are multiple pages, ensure you download all of them.
  
   Alternatively, if you prefer to automate the process of downloading all the necessary HTML files, I've created another project that crawls Amozeshyar and fetches all HTML files for you. You can find the repository for that project [here](https://github.com/abolfazlvahed1/AmozeshyarCourseScraper). This tool will automatically retrieve all HTML pages you need for this script.

3. **Specify HTML Folder Path**: 
   Place all the downloaded HTML files in a folder (e.g., `html-pages/`). You do not need to specify individual file paths. The script will automatically process all `.html` files in the folder.

4. **Define Course Codes** (Optional): 
   If you only want to filter specific courses by their course codes, define the course codes in the `course_codes` set. For example:
    ```python
    # Course codes to filter
    course_codes = {
        "4628101485", "4628101498", "4628103010", "4628105776", "4628119144",
        "4628130407", "4628135451", "4628137064", "4628164617", "4628148579",
        "4628164737", "4628153620", "4628155511"
    }
    ```
   If the `course_codes` set is empty, the script will include all courses available in the HTML files.

4. **Run the Script**: 
   Execute the script by running the following command:
    ```sh
    python /path/to/script.py
    ```

   This will generate a file named `schedule_output.txt` in the current directory, containing the weekly schedule.

Example of `schedule_output.txt`:
```
شنبه:
هوش مصنوعی و سیستم های خبره: شنبه  از 13:00 تا 15:40 (رامین رهنمون) - 3.0 واحد
طراحی الگوریتم‌ها: شنبه  از 07:15 تا 09:45 (سید مهرداد تناوش) - 3.0 واحد

يكشنبه:
زبان‌ تخصصی‌: يكشنبه  از 15:40 تا 18:10 (سیدرضا وزیری یزدی) - 2.0 واحد
نظریه زبان‌ها و ماشین‌ها: يكشنبه  از 07:15 تا 09:45 (مهرشید جوانبخت) - 3.0 واحد

دوشنبه:
آزمایشگاه شبکه ‌های‌ کامپیوتری‌: دوشنبه  از 16:20 تا 17:50 (تورج بنی رستم) - 1.0 واحد
آزمایشگاه شبکه ‌های‌ کامپیوتری‌: دوشنبه  از 14:40 تا 16:10 (تورج بنی رستم) - 1.0 واحد
آزمایشگاه شبکه ‌های‌ کامپیوتری‌: دوشنبه  از 13:00 تا 14:30 (تورج بنی رستم) - 1.0 واحد
مهندسی نرم افزار: دوشنبه  از 07:15 تا 09:45 (مهرشید جوانبخت) - 3.0 واحد

سه شنبه:
مهندسی نرم افزار: سه شنبه  از 07:15 تا 09:45 (مهرشید جوانبخت) - 3.0 واحد

چهارشنبه:
تعامل انسان و کامپیوتر: چهارشنبه  از 15:40 تا 16:10 (محمد مهدی متولی) - 3.0 واحد

پنج شنبه:
آزمایشگاه پایگاه داده: پنج شنبه  از 14:40 تا 16:10 (سيدفريد سيف السادات) - 1.0 واحد
هوش مصنوعی و سیستم های خبره: پنج شنبه  از 13:00 تا 15:40 (حسین علیزاده) - 3.0 واحد
```

## Notes

- This script processes all `.html` files in the specified folder. Ensure all the course HTML files are placed within that folder.
- If no course codes are provided, the script will include all available courses.
- If the structure of the HTML files in Amozeshyar changes, or if there are issues with the HTML files, the script may not work as expected.