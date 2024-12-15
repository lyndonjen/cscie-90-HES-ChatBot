import json
import boto3

def lambda_handler(event, context):
    # Get intent, eg "ALM Cybersecurity"
    try:
        intent_name = event['sessionState']['intent']['name']
    except:
        intent_name = 'Unknown'

    # S3 client
    s3 = boto3.client('s3')
    
    # S3 bucket and object key
    bucket_name = 'hescourses'
    object_key = 'HES_Courses.json'

    try:
        # Retrieve the JSON file from S3
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        content = response['Body'].read().decode('utf-8')
        json_data = json.loads(content)
        
        # Parse parameters
        intent_name = event['sessionState']['intent']['name']
        intent_name_lower = intent_name.lower()
        if 'cybersecurity' in intent_name_lower:
            degree_name = "ALM Cybersecurity"
        elif ('systems' in intent_name_lower) and ('engineering' in intent_name_lower):
            degree_name = "ALM Systems Engineering"
        else:
            msgText = "Sorry, I only have info for ALM Cybersecurity or ALM Systems Engineering."
            return {
                "sessionState": {
                    "dialogAction": {
                        "type": "Close"
                    },
                    "intent": {
                        "name": intent_name,
                        "state": "Fulfilled"
                    }
                },
                "messages": [
                    {
                        "contentType": "PlainText",
                        "content": msgText
                    }
                ]
            }

        try:
            coding_skills = int(event['sessionState']['intent']['slots'].get('coding_skills', {}).get('value', {}).get('interpretedValue', '0'))
        except:
            coding_skills = 0
        try:
            writing_skills = int(event['sessionState']['intent']['slots'].get('writing_skills', {}).get('value', {}).get('interpretedValue', '0'))
        except:
            writing_skills = 0

        # Do ranking
        msgText = rank_courses_by_difficulty(degree_name, coding_skills, writing_skills, json_data)
        
        # Return the values for logging purposes
        return {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": intent_name,
                    "state": "Fulfilled"
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": msgText
                }
            ]
        }
    except Exception as e:
        msgText = f"Error: {str(e)}"
        return {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": intent_name,
                    "state": "Fulfilled"
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": msgText
                }
            ]
        }


def calculate_difficulty(coding_skills, writing_skills, course_coding_skills, course_writing_skills):
    difficulty = 0.0
    if coding_skills < course_coding_skills:
        difficulty += (course_coding_skills - coding_skills)
    else:
        difficulty += 0.1 * (course_coding_skills - coding_skills)
    if writing_skills < course_writing_skills:
        difficulty += (course_writing_skills - writing_skills)
    else:
        difficulty += 0.1 * (course_writing_skills - writing_skills)
    return difficulty

def rank_courses_by_difficulty(degree_name, coding_skills, writing_skills, json_data):
    showOnlyDifficulty = True
    showCourseName = False
    showShortenedCourseName = False
    shortCourseNameLength = 20
    # Get the specific degree categories
    msgText = ""
    electives = ""
    for degree in json_data['degrees']:
        if isinstance(degree, dict) and (degree.get('degree', '')==degree_name):
            msgText = f"Degree: {degree_name}\n"
            for category in degree['categories']:
                category_name = category['category']
                category_need = category.get('need', 1)
                gate_keeper = category.get('gate_keeper', 0)
                need = category.get('need', 1)
                isElectives = "electives" in category_name.lower()
                if isElectives:
                    electives += f"\nCategory (need {need}): {category_name}\n"
                else:
                    msgText += f"\nCategory (need {need}): {category_name}\n"
                # Calculate difficulty and rank courses within this category
                ranked_courses = []
                for course_code in category['courses']:
                    for course in json_data['courses']:
                        if course['code'] == course_code:
                            course_coding_skills = course.get('coding_skills', 0)
                            course_writing_skills = course.get('writing_skills', 0)
                            difficulty = calculate_difficulty( \
                                coding_skills, writing_skills, \
                                course_coding_skills, course_writing_skills)
                            ranked_courses.append((course['code'], course['title'], \
                                course_coding_skills, course_writing_skills, difficulty))
                # Sort courses by difficulty
                ranked_courses.sort(key=lambda x: x[4])
                # Add ranked courses to msgText
                for course_code, course_title, \
                    course_coding_skills, course_writing_skills, difficulty in ranked_courses:
                    if showCourseName:
                        if showShortenedCourseName and len(course_title)>shortCourseNameLength:
                            course_text = f" {course_code}: {course_title[:shortCourseNameLength]}..."
                        else:
                            course_text = f" {course_code}: {course_title}"
                    else:
                        course_text = f" {course_code}"
                    if showOnlyDifficulty:
                        course_text += f" (Difficulty:{difficulty:.1f})\n"
                    else:
                        course_text += f" (C:{course_coding_skills},"
                        course_text += f"W:{course_writing_skills},"
                        course_text += f"Difficulty:{difficulty:.1f})\n"
                    if isElectives:
                        electives += course_text
                    else:
                        msgText += course_text
            # Show Electives before PreCapstone and Capstone
            if electives != "":
                msgText += electives
            # Show PreCapstone and Capstone last
            precapstone = degree.get('precapstone', None)
            capstone = degree.get('capstone', None)
            if precapstone or capstone:
                msgText += "\n"
                if precapstone is not None:
                    msgText += f"Pre-Capstone: {precapstone}\n"
                if capstone is not None:
                    msgText += f"Capstone: {capstone}\n"
            break
    if msgText == "":
        msgText = "Degree Not Found\n"
    return msgText
