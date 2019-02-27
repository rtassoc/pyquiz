"""quiz_func.py by Rick Taylor (11-7-2017)

Functions used by quiz_app.py for online quiz.
Can be run directly to run the quiz in console.
"""


def initialize(quiz):
    """Read the quiz file to dimensionalize the 'choices' matrix"""

    current_choices = 0
    most_choices = 0
    total_questions = 0
    new_question = True

    for line in quiz:
        line = line.strip()
        if line == '':
            if current_choices > most_choices:
                most_choices = current_choices
            current_choices = 0
            new_question = True
            continue
        elif new_question:
            total_questions += 1
            new_question = False
        else:
            current_choices += 1

    return [[None] * most_choices for i in range(total_questions)]


def populate(quiz, choices):
    """Fill the lists with the quiz questions, choices, and answers"""

    questions = []
    answers = []

    question_num = 0
    choice_num = 0
    new_question = True

    for line in quiz:
        line = line.strip()
        if line == '':
            question_num += 1
            choice_num = 0
            new_question = True
            continue
        elif new_question:
            questions.append(line)
            new_question = False
        else:
            if line[0] == '*':
                answers.append(choice_num)
                line = line[1:]
            choices[question_num][choice_num] = line
            choice_num += 1

    return choices, questions, answers


def main():
    """Main control function"""

    with open('quiz.txt') as fhand:
        quiz = fhand.readlines()

    choices = initialize(quiz)
    choices, questions, answers = populate(quiz, choices)
    correct = 0
    num_questions = len(questions)

    for question_num in range(num_questions):
        print()
        print(questions[question_num])
        for choice_num in range(len(choices[question_num])):
            if choices[question_num][choice_num] is None:
                break
            print(choice_num + 1, choices[question_num][choice_num])
        ans = input('Choice: ')
        if ans.isdigit():
            if int(ans) - 1 == answers[question_num]:
                print('CORRECT!')
                correct += 1
            else:
                print('Incorrect.')
        else:
            break

    print('\nYour score is {}%'.format(int(correct / num_questions * 100)))

    print('\nThanks for playing!\n')


if __name__ == '__main__':
    main()
