"""
This is a simple trivia game for 
assignment #4.
Property of @Miguel Carvalho
"""

import requests
from random import randrange
import json

# -- globals
difficulty = 'hard'

# generated from the 'open trivia database' API
questionsUrl = 'https://opentdb.com/api.php?amount=10&category=9&difficulty=hard&type=multiple'
leaderboardUrl = 'https://programminginception.herokuapp.com/bamboozled/leaderboard'
# ----------


def fetchQuestions(url):
    """
    Get questions from
    the required the 'Open Trivia Db' API.
    """
    res = requests.get(url).json()
    if not res['response_code']:
        return [
            {
                'question': result['question'],
                'incorrect': result['incorrect_answers'],
                'correct': result['correct_answer']
            }
            for result in res['results']
        ]


def generateOptions(questions):
    """
    Randomizes
    position of the correct answer and
    updates 'questions' with an
    'options' key.
    """
    for q in questions:
        index = randrange(0, 3)
        q['options'] = q.get('incorrect')
        q['options'].insert(index, q.get('correct'))
    return questions


def displayOptions(question):
    """
    Display each question's
    answer options. 
    """
    print(question['question'])
    for i, option in enumerate(question['options']):
        print(f'{i + 1} - {option}')


def getUserInput(type='int'):
    """
    Receive input from the user.
    """
    if(type == 'int'):
        answer = None
        while((answer is None) or (answer < 0 and answer > 3)):
            try:
                answer = int(input('>> ')) - 1
            except ValueError:
                answer = -1
                print('Please select a valid answer!')
        return answer
    else:
        username = input('Insert your username: ')
        return username


def displayAnswer(userInput, question, userAnswers):
    """
    Displays if the answer is
    correct or wrong and always
    outputs the correct answer.
    Updates userAnswer list.
    """
    # compare answer with correct answer
    answer = question.get('options')[userInput]
    correctAnswer = question.get('correct')
    correctStr = f'The correct answer is {correctAnswer}'
    if answer == correctAnswer:
        print('\nCorrect\n' + correctStr + '\n')
        userAnswers += [1]
    else:
        print('\nWrong\n' + correctStr + '\n')
        userAnswers += [0]
    return userAnswers


def checkBamboozle(questionIndex, userAnswers):
    """
    Checks for 3 wrong answers in a row.
    If 'bamboozled', the user automatically
    loses the game and gets 0 points.
    """
    if questionIndex >= 3:
        if(sum(userAnswers[questionIndex - 2: questionIndex + 1]) == 0):
            return True
        else:
            return False
    return False


def getPoints(userAnswers):
    """
    Awards user with points
    based on his answers.
    """
    return sum(userAnswers * 10)


def postResult(gameData, score, username):
    """
    Updates gameData and 'POST's score
    to leaderboard.
    """
    gameData['score'] = score
    gameData['username'] = username

    # make json request, using 'POST' to leaderboardUrl
    return requests.post(leaderboardUrl, json.dumps(gameData))


def main():
    gameData = {'points': 0, 'category': 'General Knowledge', 'username': ''}
    questions = generateOptions(fetchQuestions(questionsUrl))
    bamboozled, i = False, 0
    userAnswers = []  # 1 = correct; 0 = wrong

    print("\nWelcome to 'Bamboozled'!")
    print("------------------------\n")
    while(not bamboozled and i < len(questions)):
        question = questions[i]
        print(f'Question {i+1}')
        displayOptions(question)
        print(question['correct'])
        user_ans = getUserInput()
        userAnswers = displayAnswer(user_ans, question, userAnswers)
        print(userAnswers)
        if checkBamboozle(i, userAnswers):
            print('You were Bamboozled.')
            bamboozled = True
        i += 1
    if not bamboozled:
        score = getPoints(userAnswers)
        username = getUserInput(type='str')

        print(f'Score: {score} points')
        response = postResult(gameData, score, username)
        print()


main()
