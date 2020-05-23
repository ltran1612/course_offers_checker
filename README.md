# Course Offers Checker

## Purpose
The purpose of this program is to check through the terminal/command line if a course is offered in New Mexico State University at a specific campus in a semester automatically using Python with Selinium librarby for web automation. The program will check if a course is either available to be taken, closed, full or not offered.

## Files
### checker.py
Contain a class for the course checker which contains two functions:
+ check: return an enum value representing one of the availability of the courses: available, closed, full, or not offered
+ checkCourse: Return a string representing the availability

It will also contain the enumeration class for the availability as well as the variable to the link of the chrome driver needed for the program to run. 

### check.py
This is the main program which will prompt for the campus and ask you to type in the semester as in the website. Then, it will prompt for the courses that you want to check, and give out the answers for each course.

### constants.py
Contain the constants of strings corresponding to the campuses in the website. The strings are found by observing the html of the website. 

## Requirements to run the program
### Python requirements
+ Python 3
+ Selenium librabry (using pip)

### Other requirements
+ Google Chrome browser
+ ChromeDriver corresponding to the version of Google Chrome browser (download [here](https://chromedriver.chromium.org/))

## Installation
1. Clone this repository
2. Make sure you have all of the requirements above. The version of ChromeDriver must match the version of the Google Chrome browser. You can also use other browsers but you will need a different driver for different browser and change one part in checker.py (see the code snippet below) to match your browser:

        chrome_options = ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu") 
        driver = webdriver.Chrome(options = chrome_options, executable_path=PATH_TO_CHROME_DRIVER)
        
3. Change the variable PATH_TO_CHROME_DRIVER in checker.py file with the path to ChromeDriver on your computer.  
4. After that, you can run using the command below in the folder of the cloned repository

        python3 check.py
