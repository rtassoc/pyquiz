"""quiz_app.py by Rick Taylor (11-7-2017)

Reads a user-defined text file and produces an online quiz.
"""
import sys
from flask import Flask, render_template, request
from quiz_func import initialize, populate

app = Flask(__name__)

try:
    with open('quiz.txt') as fhand:
        quiz = fhand.readlines()
except IOError:
    sys.exit('Error trying to open "quiz.txt" in current working directory.')

choices = initialize(quiz)
choices, questions, answers = populate(quiz, choices)

# build a list of group names for radio button groups
groups = ['group' + str(i) for i in range(len(questions))]


@app.route('/', methods=['GET', 'POST'])
def index():
    # GET method - render the quiz form
    if request.method == 'GET':
        return render_template('index.html',
                               questions=questions,
                               choices=choices,
                               groups=groups)

    # POST method - process the completed form
    if len(request.form) < len(questions):
        return render_template('error.html')

    # build a list containing the text of each actual answer
    values = [request.form['group' + str(i)] for i in range(len(questions))]

    # calculate the number of correct answers
    correct = 0
    for i in range(len(questions)):
        if values[i] == choices[i][answers[i]]:
            correct += 1

    # create a message string with the quiz results
    message = ('You answered {} out of {} questions correctly '
               '({}%).'.format(correct, len(questions),
                               int(correct / len(questions) * 100)))

    return render_template('results.html',
                           questions=questions,
                           choices=choices,
                           answers=answers,
                           values=values,
                           message=message)


if __name__ == '__main__':
    app.run()
