from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from enum import Enum
import re
import constants

class CourseStatus(Enum):
    NOT_OFFERED = 0
    CLOSED = 1
    FULL = 2
    AVAILABLE = 3
    INVALID_MAJOR = -1
    INVALID_COURSE_NAME = -2

class Checker(object):
    def __init__(self, url):
        self.lookup_url = url

    # this program will go to the class search website(link above) and check if a class is closed, not offered, no slot, or available
    # pre: a valid name for a course. Expected major coures_num garbage
    # post: return a CourseStatus enum
    def check(self, campus, term, course):
        # check if the course name is valid
        # the course will have the form major course_num garbage
        # major will be any characters except for numbers
        # coures_num can be anything, but it has to start with a number
        # garbage can be anything
        major = ""
        course_num = ""
        
        found = False
        for i in range(1, len(course)):
            if course[i].isdigit() and course[i-1] == ' ':
                major = course[0 : i - 1]
                next_space_idx = course.find(' ', i)
                temp = course.find('\t', i)
                if temp != -1 and temp < next_space_idx:
                    next_space_idx = temp

                if next_space_idx == -1:
                    # print('Yo')
                    course_num = course[i:] 
                else: 
                    # print(course)
                    # print(next_space_idx)
                    # print(i)
                    course_num = course[i:next_space_idx]

                found = True
                break
        if not found:
            return CourseStatus.INVALID_COURSE_NAME

            
        # print("Major: " + major)
        # print("Course num: " + course_num)   

        # technical constants 
        campus_id = "id_campus"
        term_name = "term"
        major_name = "dept"
        search_button_id = "Submit"
        first_campus_choice_id = "id_DA"

        # load the driver
        driver = webdriver.Chrome()
        # go to the class search web
        driver.get(self.lookup_url)

        # click on random campus to show the hidden stuff
        script = "document.getElementById('{}').click()".format(first_campus_choice_id)
        driver.execute_script(script)

        # select campus
        script = "document.getElementById('{}').setAttribute('value', '{}')".format(campus_id, campus)
        driver.execute_script(script)

        # select term
        term_elem = driver.find_element_by_name(term_name)
        for option in term_elem.find_elements_by_tag_name("option"):
            if option.text == term:
                option.click()
                break
        
        # select major
        found = False
        major_elem = driver.find_element_by_name(major_name)
        for option in major_elem.find_elements_by_tag_name("option"):
            if option.text == major:
                found = True
                option.click()
                break
        if not found: 
            return CourseStatus.INVALID_MAJOR

        # get to the page of all courses in the major offered in the defined semester
        search_button = driver.find_element_by_id(search_button_id)
        search_button.click()

        # the table containing all the courses
        table = driver.find_element_by_class_name("zebra-table")

        # checking if the courses are offered
        offered_right_courses = []
        # used to count the number of open right course
        count = 0
        for row in table.find_elements_by_tag_name("tr"):
            info_list = row.find_elements_by_tag_name("td")
            if len(info_list) < 17: 
                continue

            #print(info_list[3].text + " " + info_list[0].text + " " + str(info_list[3].text == course_num) + " " + course_num)
            if info_list[3].text != course_num:
                continue

            offered_right_courses.append(row)
            count += 1
        if count == 0:
            return CourseStatus.NOT_OFFERED

        # check if it is closed
        open_right_courses = []
        # used to count the number of open courses  
        count = 0  
        for row in offered_right_courses:
            info_list = row.find_elements_by_tag_name("td")
            if info_list[0].text == "Closed":
                continue

            open_right_courses.append(row)
            count += 1
        if count == 0:
            return CourseStatus.CLOSED

        # check if the course is full
        open_right_not_full_courses = []
        # used to count the number of open, not full, right courses
        count = 0
        #print(len(open_right_courses))
        for row in open_right_courses:
            info_list = row.find_elements_by_tag_name("td")
            try:
                if int(info_list[14].text) > 0:
                    open_right_not_full_courses.append(row)
                    count += 1  
            except ValueError:
                continue
        if count == 0:
            return CourseStatus.FULL

        # check if the course is available
        return CourseStatus.AVAILABLE

        # close after done checking
        driver.quit()

    # This function will return a string representing the status of the code
    # It will also return a string if the course name is valid, if the major exists.
    def checkCourse(self, campus, term, course):
        result = self.check(campus, term, course)
        if result == CourseStatus.AVAILABLE:
            return "Course is available"
        elif result == CourseStatus.NOT_OFFERED:
            return "Course is not offered"
        elif result == CourseStatus.FULL:
            return "Course is full"
        elif result == CourseStatus.CLOSED:
            return "Course is closed for registration"
        elif result == CourseStatus.INVALID_COURSE_NAME:
            return "Course name is invalid"
        elif result == CourseStatus.INVALID_MAJOR:
            return "No such major exists"
        elif result == CourseStatus.INVALID_COURSE_NUM:
            return "No such course number exists"
        else:
            return "Invalid enum"

# testing
if __name__ == "__main__":
    # choices variables
    checker = Checker("https://accounts.nmsu.edu/catalog/")
    campus = constants.LAS_CRUCES
    term = "2020 Fall"

    print("Testing the program using the classes offered in Fall 2020 NMSU\n")
    # class in the list, opened, and can be taken
    print("In the list, opened and can be taken: {}: ".format(checker.checkCourse(campus, term, "C S 111")))
    # class is not in the list
    print("Not in the list: {}: ".format(checker.checkCourse(campus, term, "C S 491")))
    # class in the list, but closed
    print("In the list, but closed: {}: ".format(checker.checkCourse(campus, term, "C S 464")))
    # class in the list but no more space
    print("In the list, but full: {}: ".format(checker.checkCourse(campus, term, "C S 464")))

    # check invalid names
    print("Invalid course: {}".format(checker.checkCourse(campus, term, "371")))

    # check invalid major
    print("Invalid major: {}".format(checker.checkCourse(campus, term, "a 371")))