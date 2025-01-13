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

## Usage

To use this script, follow these steps:

1. **Download HTML Files**: First, download the HTML files of the courses offered from Amozeshyar. You can access it at `https://eserv.iau.ir/EServices/pSearchAction.do`. Search for your group's offered courses and download the HTML files. If there are multiple pages, download all of them.

2. **Specify HTML File Paths**: Add the paths to your downloaded HTML files in the `html_file_paths` list. For example:
    ```python
    # Paths to HTML files
    html_file_paths = ["page1.html", "page2.html"]
    ```

    I've included `page1.html` and `page2.html` for the computer engineering group in the repository, but you can change these to your own paths.

3. **Define Course Codes**: Add the course codes you want to filter in the `course_codes` set. For example:
    ```python
    # Course codes to filter
    course_codes = {
        "4628101485", "4628101498", "4628103010", "4628105776", "4628119144",
        "4628130407", "4628135451", "4628137064", "4628164617", "4628148579",
        "4628164737", "4628153620", "4628155511"
    }
    ```

4. **Run the Script**: Execute the script by running the following command:
    ```sh
    python \path\to\script.py
    ```

    This will generate a file named `schedule_output.txt` in the current directory, containing the weekly schedule.

Example of `schedule_output.txt`:
```
چهارشنبه:
تعامل انسان و کامپیوتر: چهارشنبه  از 15:40 تا 16:10 (محمد مهدی متولی) - 3 واحد
هوش مصنوعی و سیستم های خبره: چهارشنبه  از 09:45 تا 12:15 (محمدامین بنی ادم) - 3 واحد
طراحی کامپیوتری سیستمهای دیجیتال: چهارشنبه  از 07:15 تا 09:45 (محمد صادقی) - 3 واحد

شنبه:
هوش مصنوعی و سیستم های خبره: شنبه  از 13:00 تا 15:40 (رامین رهنمون) - 3 واحد
طراحی الگوریتم‌ها: شنبه  از 07:15 تا 09:45 (سید مهرداد تناوش) - 3 واحد

پنج:
آزمایشگاه پایگاه داده: پنج شنبه  از 14:40 تا 16:10 (سيدفريد سيف السادات) - 1 واحد
هوش مصنوعی و سیستم های خبره: پنج شنبه  از 13:00 تا 15:40 (حسین علیزاده) - 3 واحد

دوشنبه:
آزمایشگاه شبکه ‌های‌ کامپیوتری‌: دوشنبه  از 16:20 تا 17:50 (تورج بنی رستم) - 1 واحد
مهندسی نرم افزار: دوشنبه  از 07:15 تا 09:45 (مهرشید جوانبخت) - 3 واحد

يكشنبه:
آزمایشگاه شبکه ‌های‌ کامپیوتری‌: يكشنبه  از 16:20 تا 17:50 (نجمه ترابیان) - 1 واحد
مدیریت پروژه های فناوری اطلاعات: يكشنبه  از 13:00 تا 15:40 (محمدعلی یوسفی) - 3 واحد
نظریه زبان‌ها و ماشین‌ها: يكشنبه  از 09:45 تا 12:15 (مهرشید جوانبخت) - 3 واحد
نظریه زبان‌ها و ماشین‌ها: يكشنبه  از 07:15 تا 09:45 (مهرشید جوانبخت) - 3 واحد

سه:
آزمایشگاه پایگاه داده: سه شنبه  از 14:40 تا 16:10 (اعظم شکاری شهرک) - 1 واحد
مهندسی نرم افزار: سه شنبه  از 07:15 تا 09:45 (مهرشید جوانبخت) - 3 واحد
```

## Notes

- This script does not guarantee that it will contain all courses if the structure of the HTML files in Amozeshyar changes or if there are any problems with the HTML files.