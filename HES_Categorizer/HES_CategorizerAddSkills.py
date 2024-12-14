# HES_CategorizerAddSkills.py
# by Lyndon Jen, for CSCI E-90 Final Project
#
# This is the code that strips off all HES Courses fields, leaving only
# "code" and "title" fields, and adds: coding_skills, writing_skills fields
# according to the course "code", eg "CSCI 90"-->9/0
# Used for in the Visual Studio environment only,
# Used to generate a new HES_Courses.json, with Courses only,
# will not have Degrees listings at all, to be added manually,
# to create final HES_Courses.json
# Note, the initial JSON file only has courses for Spring 2025,
# so does not have all courses, including some Pre-Capstone and Capstone

import json

# Function to add skills to each course
def add_skills_to_courses(courses):
    for course in courses:
        code = course["code"]
        digits = [int(d) for d in code if d.isdigit()]
        coding_skills = digits[-2] if len(digits) > 1 else 0  # 10's digit or 0 if not available
        writing_skills = digits[-1] if digits else 0  # 1's digit or 0 if not available

        course["coding_skills"] = coding_skills
        course["writing_skills"] = writing_skills

    return courses

# Load JSON data from file
with open("HES_Courses.json", "r") as file:
    data = json.load(file)

# Process courses
data["courses"] = add_skills_to_courses(data["courses"])

# Write updated data to a new JSON file
with open("HES_Courses2.json", "w") as file:
    json.dump(data, file, indent=4)

print("Updated courses JSON file has been created.")
