import constants
import sys
from checker import Checker



if __name__ == "__main__":
    
    campus_choice = input("Choose one of the campuses:\n1. Donna Anna\n2. Las Cruces\n3. Grants\n4. Alamogordo\n5. Carlsbad\n6. Online\n")
    campus = constants.LAS_CRUCES
    if campus_choice == 1:
        campus = constants.DONNA_ANNA
    elif campus_choice == 2:
        campus = constants.LAS_CRUCES
    elif campus_choice == 3:
        campus = constants.ALAMOGORDO
    elif campus_choice == 4:
        campus = constants.CARLSBAD
    elif campus_choice == 5:
        campus = constants.ONLINE

    term = input("Enter the name of the campus as on the website: ") 
    

    in_stream = sys.stdin
    lines = in_stream.readlines()
    checker = Checker(constants.class_lookup_url)

    print("\nThe result\n")
    for line in lines:
        print("+ {}   -> {}\n".format(line, checker.checkCourse(campus, term, line)))


