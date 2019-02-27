import sys
from flask import Flask, render_template, request
from quiz_func import initialize, populate

app = Flask(__name__)

try:
    with open('quiz.txt') as fhand:
        quiz = fhand.readlines()
except IOError:
    sys.exit('Error trying to open "quiz.txt"')

choices = initialize(quiz)
choices, questions, answers = populate(quiz, choices)

groups = ['group' + str(i) for i in range(len(questions))]


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html',
                               choices=choices,
                               questions=questions,
                               groups=groups)

    if len(request.form) < len(questions):
        return render_template('error.html')

    values = [request.form['group' + str(i)] for i in range(len(questions))]

    correct = 0
    for i in range(len(questions)):
        if values[i] == choices[i][answers[i]]:
            correct += 1

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
