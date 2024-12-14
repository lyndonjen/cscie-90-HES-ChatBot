# HES_Categorizer.py
# by Lyndon Jen, for CSCI E-90 Final Project
#
# This is the code that ranks a given degree_name, coding_skills, writing_skills
# Used for debugging outside of AWS environment, but in the Visual Studio environment
# To be eventually incorporated into the AWS Lambda function for HES ChatBot

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
    showCourseName = True
    showShortenedCourseName = True
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

#
if True:
    degree_name = "ALM Cybersecurity"
else:
    degree_name = "ALM Systems Engineering"
coding_skills = 2
writing_skills = 7
json_data = {
  "degrees": [
    {
      "degree": "ALM Cybersecurity",
      "precapstone": "CSCI 597B",
      "capstone": "CSCI 599B",
      "need": 10,
      "categories": [
        {
          "category": "Introduction to Cybersecurity",
          "gate_keeper": 1,
          "need": 1,
          "courses": [
            "CSCI 159"
          ]
        },
        {
          "category": "Networks and Cloud Security",
          "gate_keeper": 1,
          "need": 1,
          "courses": [
            "CSCI 155"
          ]
        },
        {
          "category": "Application Development",
          "need": 1,
          "courses": [
            "CSCI 11",
            "CSCI 149A"
          ]
        },
        {
          "category": "Cloud Computing",
          "need": 1,
          "courses": [
            "CSCI 49B",
            "CSCI 90",
            "CSCI 94",
            "CSCI 117"
          ]
        },
        {
          "category": "Compliance and Controls",
          "need": 1,
          "courses": [
            "CSCI 125",
            "CSCI 147A"
          ]
        },
        {
          "category": "Cybersecurity Electives",
          "need": 8,
          "courses": [
            "CSCI 11",
            "CSCI 40",
            "CSCI 49",
            "CSCI 49B",
            "CSCI 61",
            "CSCI 90",
            "CSCI 94",
            "CSCI 117",
            "CSCI 125",
            "CSCI 138",
            "CSCI 140",
            "CSCI 142",
            "CSCI 144",
            "CSCI 145",
            "CSCI 147A",
            "CSCI 149A"
          ]
        },
        {
          "category": "Risk Assessment",
          "need": 1,
          "courses": [
            "CSCI 117",
            "CSCI 125",
            "CSCI 142",
            "CSCI 144"
          ]
        }
      ]
    },
    {
      "degree": "ALM Systems Engineering",
      "precapstone": "CSCI 597C",
      "capstone": "CSCI 599C",
      "need": 10,
      "categories": [
        {
          "category": "Cloud Communications",
          "gate_keeper": 1,
          "need": 1,
          "courses": [
            "CSCI 40",
            "CSCI 49",
            "CSCI 145",
            "CSCI 155"
          ]
        },
        {
          "category": "Database Management",
          "gate_keeper": 1,
          "need": 1,
          "courses": [
            "CSCI 59",
            "CSCI 66",
            "CSCI 88C",
            "CSCI 165",
            "CSCI 265"
          ]
        },
        {
          "category": "Business Analytics",
          "need": 1,
          "courses": [
            "CSCI 96",
            "CSCI 108",
            "CSCI 112",
            "CSCI 116",
            "CSCI 161",
            "CSCI 278",
            "MATH 116"
          ]
        },
        {
          "category": "Cloud Computing",
          "need": 1,
          "courses": [
            "CSCI 49B",
            "CSCI 90",
            "CSCI 94",
            "CSCI 117",
            "CSCI 125",
            "CSCI 149A",
            "CSCI 192"
          ]
        },
        {
          "category": "IT Management (On Campus)",
          "need": 1,
          "courses": [
            "CSCI 176"
          ]
        },
        {
          "category": "Security and Risk Assessment",
          "need": 1,
          "courses": [
            "CSCI 11",
            "CSCI 117",
            "CSCI 125",
            "CSCI 144",
            "CSCI 147A",
            "CSCI 149A",
            "CSCI 159"
          ]
        },
        {
          "category": "Systems Engineering Electives",
          "need": 8,
          "courses": [
            "CSCI 3",
            "CSCI 7",
            "CSCI 8B",
            "CSCI 11",
            "CSCI 12",
            "CSCI 15",
            "CSCI 25",
            "CSCI 40",
            "CSCI 49",
            "CSCI 49B",
            "CSCI 59",
            "CSCI 61",
            "CSCI 80",
            "CSCI 88C",
            "CSCI 90",
            "CSCI 94",
            "CSCI 96",
            "CSCI 101",
            "CSCI 102",
            "CSCI 104",
            "CSCI 106",
            "CSCI 108",
            "CSCI 109B",
            "CSCI 112",
            "CSCI 114",
            "CSCI 115",
            "CSCI 116",
            "CSCI 117",
            "CSCI 120",
            "CSCI 125",
            "CSCI 138",
            "CSCI 140",
            "CSCI 142",
            "CSCI 144",
            "CSCI 145",
            "CSCI 147A",
            "CSCI 149A",
            "CSCI 151",
            "CSCI 155",
            "CSCI 159",
            "CSCI 161",
            "CSCI 165",
            "CSCI 169",
            "CSCI 176",
            "CSCI 184",
            "CSCI 192"
          ]
        },
        {
          "category": "Web Principles",
          "need": 1,
          "courses": [
            "CSCI 3",
            "CSCI 12",
            "CSCI 15",
            "CSCI 33A",
            "CSCI 114",
            "DGMD 28"
          ]
        }
      ]
    }
  ],
  "courses": [
    {
      "code": "CSCI 1B",
      "title": "Computer Science for Business Professionals",
      "coding_skills": 0,
      "writing_skills": 1
    },
    {
      "code": "CSCI 3",
      "title": "Introduction to Web Programming Using JavaScript",
      "coding_skills": 0,
      "writing_skills": 3
    },
    {
      "code": "CSCI 7",
      "title": "Introduction to Computer Science with Python",
      "coding_skills": 0,
      "writing_skills": 7
    },
    {
      "code": "CSCI 8B",
      "title": "Mobile GIS",
      "coding_skills": 0,
      "writing_skills": 8
    },
    {
      "code": "CSCI 10B",
      "title": "Introduction to Computer Science Using Java II",
      "coding_skills": 1,
      "writing_skills": 0
    },
    {
      "code": "CSCI 11",
      "title": "Artificial Intelligence, the Internet-of-Things, and Cybersecurity",
      "coding_skills": 1,
      "writing_skills": 1
    },
    {
      "code": "CSCI 12",
      "title": "Fundamentals of Web Development",
      "coding_skills": 1,
      "writing_skills": 2
    },
    {
      "code": "CSCI 15",
      "title": "Web Programming with PHP",
      "coding_skills": 1,
      "writing_skills": 5
    },
    {
      "code": "CSCI 20",
      "title": "Discrete Mathematics for Computer Science",
      "coding_skills": 2,
      "writing_skills": 0
    },
    {
      "code": "CSCI 22",
      "title": "Data Structures",
      "coding_skills": 2,
      "writing_skills": 2
    },
    {
      "code": "CSCI 25",
      "title": "Computer Vision",
      "coding_skills": 2,
      "writing_skills": 5
    },
    {
      "code": "CSCI 28",
      "title": "Unix/Linux Systems Programming",
      "coding_skills": 2,
      "writing_skills": 8
    },
    {
      "code": "CSCI 31",
      "title": "Web Application Development Using Node.js",
      "coding_skills": 3,
      "writing_skills": 1
    },
    {
      "code": "CSCI 33A",
      "title": "Web Programming with Python and JavaScript",
      "coding_skills": 3,
      "writing_skills": 3
    },
    {
      "code": "CSCI 34",
      "title": "User Experience Engineering",
      "coding_skills": 3,
      "writing_skills": 4
    },
    {
      "code": "CSCI 40",
      "title": "Communication Protocols and Internet Architectures",
      "coding_skills": 4,
      "writing_skills": 0
    },
    {
      "code": "CSCI 49",
      "title": "Cloud Security",
      "coding_skills": 4,
      "writing_skills": 9
    },
    {
      "code": "CSCI 49B",
      "title": "Cloud Architectures, Security, and Governance",
      "coding_skills": 4,
      "writing_skills": 9
    },
    {
      "code": "CSCI 50",
      "title": "Intensive Introduction to Computer Science",
      "coding_skills": 5,
      "writing_skills": 0
    },
    {
      "code": "CSCI 59",
      "title": "Designing and Developing Relational and NoSQL Databases",
      "coding_skills": 5,
      "writing_skills": 9
    },
    {
      "code": "CSCI 61",
      "title": "Systems Programming and Machine Organization",
      "coding_skills": 6,
      "writing_skills": 1
    },
    {
      "code": "CSCI 63C",
      "title": "Elements of Data Science and Statistical Learning with R",
      "coding_skills": 6,
      "writing_skills": 3
    },
    {
      "code": "CSCI 80",
      "title": "Introduction to Artificial Intelligence with Python",
      "coding_skills": 8,
      "writing_skills": 0
    },
    {
      "code": "CSCI 90",
      "title": "Cloud Services, Infrastructure, and Computing",
      "coding_skills": 9,
      "writing_skills": 0
    },
    {
      "code": "CSCI 94",
      "title": "Fundamentals of Cloud Computing and OpenAI with Microsoft Azure",
      "coding_skills": 9,
      "writing_skills": 4
    },
    {
      "code": "CSCI 95",
      "title": "Compiler Design and Implementation",
      "coding_skills": 9,
      "writing_skills": 5
    },
    {
      "code": "CSCI 96",
      "title": "Data Mining for Business",
      "coding_skills": 9,
      "writing_skills": 6
    },
    {
      "code": "CSCI 101",
      "title": "Foundations of Data Science and Engineering",
      "coding_skills": 0,
      "writing_skills": 1
    },
    {
      "code": "CSCI 102",
      "title": "Econometrics and Causal Inference with R",
      "coding_skills": 0,
      "writing_skills": 2
    },
    {
      "code": "CSCI 104",
      "title": "Advanced Deep Learning",
      "coding_skills": 0,
      "writing_skills": 4
    },
    {
      "code": "CSCI 106",
      "title": "Data Modeling",
      "coding_skills": 0,
      "writing_skills": 6
    },
    {
      "code": "CSCI 108",
      "title": "Data Mining, Discovery, and Exploration",
      "coding_skills": 0,
      "writing_skills": 8
    },
    {
      "code": "CSCI 109B",
      "title": "Advanced Topics in Data Science",
      "coding_skills": 0,
      "writing_skills": 9
    },
    {
      "code": "CSCI 112",
      "title": "Advertising Analytics and Real-Time Technology",
      "coding_skills": 1,
      "writing_skills": 2
    },
    {
      "code": "CSCI 114",
      "title": "Web Application Development with Jamstack",
      "coding_skills": 1,
      "writing_skills": 4
    },
    {
      "code": "CSCI 115",
      "title": "Advanced Practical Data Science",
      "coding_skills": 1,
      "writing_skills": 5
    },
    {
      "code": "CSCI 116",
      "title": "Dynamic Modeling and Forecasting in Big Data",
      "coding_skills": 1,
      "writing_skills": 6
    },
    {
      "code": "CSCI 117",
      "title": "Secure Applications: Managing the Deployment Infrastructure",
      "coding_skills": 1,
      "writing_skills": 7
    },
    {
      "code": "CSCI 125",
      "title": "Crypto and Blockchain: Understanding the Technology and the Challenges It Presents",
      "coding_skills": 2,
      "writing_skills": 5
    },
    {
      "code": "CSCI 138",
      "title": "The Future of Humanity: A System Approach",
      "coding_skills": 3,
      "writing_skills": 8
    },
    {
      "code": "CSCI 142",
      "title": "Foundations of Technology Risk Management and Assessment",
      "coding_skills": 4,
      "writing_skills": 2
    },
    {
      "code": "CSCI 144",
      "title": "Information System Forensics",
      "coding_skills": 4,
      "writing_skills": 4
    },
    {
      "code": "CSCI 145",
      "title": "Networking at Scale",
      "coding_skills": 4,
      "writing_skills": 5
    },
    {
      "code": "CSCI 147A",
      "title": "Fundamentals of the Law and Cybersecurity",
      "coding_skills": 4,
      "writing_skills": 7
    },
    {
      "code": "CSCI 149A",
      "title": "Software Applications: Security Lifecycle Threats",
      "coding_skills": 4,
      "writing_skills": 9
    },
    {
      "code": "CSCI 151",
      "title": "Introduction to Databases with SQL",
      "coding_skills": 5,
      "writing_skills": 1
    },
    {
      "code": "CSCI 155",
      "title": "Networks and Cloud Security",
      "coding_skills": 5,
      "writing_skills": 5
    },
    {
      "code": "CSCI 158",
      "title": "Remote Sensing Data and Applications",
      "coding_skills": 5,
      "writing_skills": 8
    },
    {
      "code": "CSCI 159",
      "title": "Introduction to Cybersecurity",
      "coding_skills": 5,
      "writing_skills": 9
    },
    {
      "code": "CSCI 161",
      "title": "Computational Bayesian Inference",
      "coding_skills": 6,
      "writing_skills": 1
    },
    {
      "code": "CSCI 165",
      "title": "Data Systems",
      "coding_skills": 6,
      "writing_skills": 5
    },
    {
      "code": "CSCI 169",
      "title": "Creating and Maintaining Scalable Design Systems",
      "coding_skills": 6,
      "writing_skills": 9
    },
    {
      "code": "CSCI 176",
      "title": "Advanced Cloud Technology Management: Strategies for Successful Enterprise Deployment",
      "coding_skills": 7,
      "writing_skills": 6
    },
    {
      "code": "CSCI 184",
      "title": "Data Science and Artificial Intelligence: Ethics, Governance, and Laws",
      "coding_skills": 8,
      "writing_skills": 4
    },
    {
      "code": "CSCI 192",
      "title": "Modern Data Analytics",
      "coding_skills": 9,
      "writing_skills": 2
    },
    {
      "code": "CSCI 210",
      "title": "Algorithms at the Ends of the Wire",
      "coding_skills": 1,
      "writing_skills": 0
    },
    {
      "code": "CSCI 265",
      "title": "Big Data Systems",
      "coding_skills": 6,
      "writing_skills": 5
    },
    {
      "code": "CSCI 278",
      "title": "Applied Quantitative Finance and Machine Learning",
      "coding_skills": 7,
      "writing_skills": 8
    },
    {
      "code": "CSCI 497",
      "title": "Crafting the Thesis Proposal in Software Engineering Tutorial",
      "coding_skills": 9,
      "writing_skills": 7
    },
    {
      "code": "CSCI 499AB",
      "title": "ALM Thesis in Software Engineering",
      "coding_skills": 9,
      "writing_skills": 9
    },
    {
      "code": "CSCI 599",
      "title": "Software Engineering Capstone",
      "coding_skills": 9,
      "writing_skills": 9
    },
    {
      "code": "CSCI 597A",
      "title": "Precapstone in Data Science",
      "coding_skills": 9,
      "writing_skills": 7
    },
    {
      "code": "CSCI 599A",
      "title": "Data Science Capstone",
      "coding_skills": 9,
      "writing_skills": 9
    },
    {
      "code": "CSCI 597B",
      "title": "Precapstone in Cybersecurity",
      "coding_skills": 9,
      "writing_skills": 7
    },
    {
      "code": "CSCI 599B",
      "title": "Cybersecurity Capstone",
      "coding_skills": 9,
      "writing_skills": 9
    },
    {
      "code": "CSCI 597C",
      "title": "Precapstone in Systems Engineering",
      "coding_skills": 9,
      "writing_skills": 7
    },
    {
      "code": "CSCI 599C",
      "title": "Systems Engineering Capstone",
      "coding_skills": 9,
      "writing_skills": 9
    },
    {
      "code": "MATH 116",
      "title": "Mathematical Modeling",
      "coding_skills": 1,
      "writing_skills": 6
    },
    {
      "code": "DGMD 28",
      "title": "Developing Single-Page Web Applications",
      "coding_skills": 2,
      "writing_skills": 8
    }
  ]
}

msgText = rank_courses_by_difficulty(degree_name, coding_skills, writing_skills, json_data)
print(msgText)
