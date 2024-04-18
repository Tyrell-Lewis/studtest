import click, pytest, sys
import nltk
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.models import Student, Karma
from App.controllers import (
    create_student, create_staff, create_admin, get_all_users_json,
    get_all_users, get_transcript, get_student_by_UniId, setup_nltk,
    analyze_sentiment, get_total_As, get_total_courses_attempted,
    calculate_academic_score, create_review, create_incident_report,
    create_accomplishment, get_staff_by_id, get_student_by_id,
    create_recommendation, create_karma)

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)


# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
  db.drop_all()
  db.create_all()

  create_student(username="billy",
                 firstname="Billy",
                 lastname="John",
                 email="billy@example.com",
                 password="billypass",
                 faculty="FST",
                 admittedTerm="",
                 UniId='816031060',
                 degree="",
                 gpa="")
  create_student(username="alice",
                 firstname="Alice",
                 lastname="Smith",
                 email="alice@example.com",
                 password="alicepass",
                 faculty="FST",
                 admittedTerm="2023-09",
                 UniId='816031061',
                 degree="Bachelor of Science",
                 gpa="3.5")

  create_student(username="dian",
                 firstname="Dian",
                 lastname="Taylor",
                 email="diana@example.com",
                 password="dianapass",
                 faculty="FST",
                 admittedTerm="2024-01",
                 UniId='816031062',
                 degree="Bachelor of Arts",
                 gpa='2.1')

  #Creating staff
  create_staff(username="tim",
               firstname="Tim",
               lastname="Long",
               email="",
               password="timpass",
               faculty="")
  print('database intialized')

  create_admin(username="admin",
               firstname="Sanjeev",
               lastname="Praboo",
               email="andy@example.com",
               password="password",
               faculty="FST")
  create_student(username="brian",
                 firstname="Brian",
                 lastname="Saylor",
                 email="biana@example.com",
                 password="bianapass",
                 faculty="FST",
                 admittedTerm="2024-01",
                 UniId='816031063',
                 degree="Bachelor of Arts",
                 gpa='2.1')
  students = Student.query.all()

  for student in students:
    create_karma(student.ID)
    student.karmaID = Karma.query.filter_by(
        studentID=student.ID).first().karmaID

  # staff = get_staff_by_id(2)
  # student = get_student_by_id(1)
  # create_review(staff, student, 1, 1, "goodreviewsample")
  # #create_review(1, 1, -3, -3, "badreviewsample")
  # create_incident_report('billy', 'staff', "incident reportsample", 1)
  create_accomplishment(1, 0, "Tim Long", "Good Grades",
                        "accomplishmentdetails", 6, "None yet")
  create_accomplishment(2, 0, "Tim Long", "Good Grades",
                        "accomplishmentdetails", 5, "None yet")
  create_accomplishment(3, 0, "Tim Long", "Good Grades",
                        "accomplishmentdetails", 3, "None yet")
  create_accomplishment(6, 0, "Tim Long", "Good Grades",
                        "accomplishmentdetails", 2, "None yet")

  create_recommendation(1, 4, False, "Job", "I just want it", "None yet")


@app.cli.command("nltk_test", help="Tests nltk")
@click.argument("sentence", default="all")
def analyze(sentence):
  analyze_sentiment(sentence)
  return


# '''
# User Commands
# '''

# # Commands can be organized using groups

# # create a group, it would be the first argument of the comand
# # eg : flask user <command>
# # user_cli = AppGroup('user', help='User object commands')

# # # Then define the command and any parameters and annotate it with the group (@)
# @user_cli.command("create", help="Creates a user")
# @click.argument("username", default="rob")
# @click.argument("password", default="robpass")
# def create_user_command(id, username, firstname,lastname , password, email, faculty):
#     create_user(id, username, firstname,lastname , password, email, faculty)
#     print(f'{username} created!')

# # this command will be : flask user create bob bobpass

# @user_cli.command("list", help="Lists users in the database")
# @click.argument("format", default="string")
# def list_user_command(format):
#     if format == 'string':
#         print(get_all_users())
#     else:
#         print(get_all_users_json())

# app.cli.add_command(user_cli) # add the group to the cli
'''
Test Commands
'''

test = AppGroup('test', help='Testing commands')


@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "UserUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
  else:
    sys.exit(pytest.main(["-k", "App"]))


@test.command("student", help="Run Student tests")
@click.argument("type", default="all")
def student_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "StudentUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "StudentIntegrationTests"]))
  else:
    sys.exit(pytest.main(["-k", "App"]))


@test.command("staff", help="Run Staff tests")
@click.argument("type", default="all")
def staff_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "StaffUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "StaffIntegrationTests"]))
  else:
    sys.exit(pytest.main(["-k", "App"]))


@test.command("review", help="Run Review tests")
@click.argument("type", default="all")
def review_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "ReviewUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "ReviewIntegrationTests"]))
  else:
    sys.exit(pytest.main(["-k", "App"]))


@test.command("recommendation", help="Run Recommendation tests")
@click.argument("type", default="all")
def recommendation_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "RecommendationUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "RecommendationIntegrationTests"]))
  else:
    sys.exit(pytest.main(["-k", "App"]))


@test.command("karma", help="Run Karma tests")
@click.argument("type", default="all")
def karma_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "KarmaUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "KarmaIntegrationTests"]))
  else:
    sys.exit(pytest.main(["-k", "App"]))


@test.command("incidentreport", help="Run Incident Report tests")
@click.argument("type", default="all")
def incident_reports_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "IncidentReportUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "IncidentReportIntegrationTests"]))
  # else:
  #     sys.exit(pytest.main(["-k", "App"]))


@test.command("accomplishment", help="Run Accomplishment tests")
@click.argument("type", default="all")
def accomplishment_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "AccomplishmentUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "AccomplishmentIntegrationTests"]))
  # else:
  #     sys.exit(pytest.main(["-k", "App"]))


@test.command("grades", help="Run Grades tests")
@click.argument("type", default="all")
def grades_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "GradesUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "GradesIntegrationTests"]))
  # else:
  #     sys.exit(pytest.main(["-k", "App"]))


@test.command("admin", help="Run Admin tests")
@click.argument("type", default="all")
def admin_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "AdminUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "AdminIntegrationTests"]))
  # else:
  #     sys.exit(pytest.main(["-k", "App"]))


@test.command("nltk", help="Run NLTK tests")
@click.argument("type", default="all")
def nltk_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "NLTKUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "NLTKIntegrationTests"]))


@test.command("print", help="print get_transcript")
@click.argument("type", default="all")
def print_transcript(type):
  studentID = input("Enter student ID: ")  # Prompt user to enter student ID
  transcripts = get_transcript(
      studentID)  # Get transcript data for the student
  if transcripts:
    for transcript in transcripts:
      if type == "all":
        print(transcript.to_json())  # Print all transcript data as JSON
      # elif type == "id":
      #     print(transcript.studentID)  # Print student ID
      # elif type == "gpa":
      #     print(transcript.gpa)  # Print GPA
      # elif type == "fullname":
      #     print(transcript.fullname)  # Print full name
      # Add more options as needed
      else:
        print(
            "Invalid type. Please choose 'all', 'id', 'gpa', 'fullname', or add more options."
        )
  else:
    print("Transcript not found for student with ID:", studentID)


@test.command("printstu", help="print get_student")
@click.argument("type", default="all")
def print_student(type):
  UniId = input("Enter student ID: ")
  student = get_student_by_UniId(UniId)
  if student:
    if type == "all":
      print(student.to_json(0))
    # elif type == "id":
    #     print(student.UniId)
    # elif type == "gpa":
    #     print(student.gpa)
    # elif type == "fullname":
    #     print(student.fullname)
    else:
      print(
          "Invalid type. Please choose 'all', 'id', 'gpa', 'fullname', or add more options."
      )
  else:
    print("Student not found with ID:", UniId)


@test.command("printgradepointsandgpa_weight",
              help="print student grade points from transcript")
@click.argument("type", default="all")
def print_grade_points(type):
  UniId = input("Enter student ID: ")
  points = get_total_As(UniId)
  cources_attempted = get_total_courses_attempted(UniId)
  if points:
    print('points ', points)
    print('courses attepmtped:, ', cources_attempted)

  else:
    print("Student not found with ID:", UniId)


@test.command("printacademicscore", help="print student academic weight")
@click.argument("type", default="all")
def print_academic_weight(type):
  UniId = input("Enter student ID: ")
  points = get_total_As(UniId)
  cources_attempted = get_total_courses_attempted(UniId)
  academic_score = calculate_academic_score(UniId)
  if points:
    print('points ', points)
    print('courses attepmtped:, ', cources_attempted)
    print('Academic Score:, ', academic_score)

  else:
    print("Student not found with ID:", UniId)


app.cli.add_command(test)
