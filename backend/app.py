from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ================= QUESTIONS =================

questions = [

{
"question":"What is Python?",
"keywords":["programming","language"],
"correct_answer":"Python is a high level interpreted programming language used for AI web development automation and software development."
},

{
"question":"What is HTML?",
"keywords":["web","markup"],
"correct_answer":"HTML stands for HyperText Markup Language and is used to create web pages."
},

{
"question":"What is CSS?",
"keywords":["style","design"],
"correct_answer":"CSS is used for styling web pages."
},

{
"question":"What is JavaScript?",
"keywords":["interactive","web"],
"correct_answer":"JavaScript is used to make websites interactive."
},

{
"question":"What is SQL?",
"keywords":["database"],
"correct_answer":"SQL is used to manage databases."
},

{
"question":"What is OOP?",
"keywords":["object","class"],
"correct_answer":"OOP means Object Oriented Programming."
},

{
"question":"What is Inheritance?",
"keywords":["parent","child"],
"correct_answer":"Inheritance allows one class to acquire properties of another class."
},

{
"question":"What is Polymorphism?",
"keywords":["many","forms"],
"correct_answer":"Polymorphism means one method can perform different tasks."
},

{
"question":"What is Encapsulation?",
"keywords":["binding","data"],
"correct_answer":"Encapsulation binds data and methods together."
},

{
"question":"What is Abstraction?",
"keywords":["hide","details"],
"correct_answer":"Abstraction hides implementation details."
}

]

# MAKE 100 QUESTIONS
base_questions = questions.copy()

while len(questions) < 100:
    for q in base_questions:
        if len(questions) < 100:
            questions.append(q.copy())

# ================= VARIABLES =================

current_question = 0
score = 0
interview_started = False
interview_paused = False

# ================= CHAT API =================

@app.route('/chat', methods=['POST'])
def chat():

    global current_question
    global score
    global interview_started
    global interview_paused

    data = request.get_json()

    user_message = data['message'].lower()

    # ================= START =================

    if user_message == "start":

        current_question = 0
        score = 0
        interview_started = True
        interview_paused = False

        return jsonify({
            "reply":"Interview Started!\n\nQuestion 1:\n" + questions[current_question]["question"]
        })

    # ================= EXIT =================

    if user_message == "exit":

        interview_started = False
        interview_paused = True

        final_score = str(score) + "/100"

        return jsonify({
            "reply":"Interview Exited!\n\nCurrent Score: "
            + final_score
            + "\n\nType CONTINUE to resume interview."
        })

    # ================= CONTINUE =================

    if user_message == "continue":

        if interview_paused == True:

            interview_started = True
            interview_paused = False

            return jsonify({
                "reply":"Interview Continued!\n\nQuestion "
                + str(current_question + 1)
                + ":\n"
                + questions[current_question]["question"]
            })

        else:

            return jsonify({
                "reply":"No paused interview found."
            })

    # ================= NOT STARTED =================

    if interview_started == False:

        return jsonify({
            "reply":"Type START to begin interview."
        })

    # ================= CHECK ANSWER =================

    is_correct = False

    for word in questions[current_question]["keywords"]:

        if word in user_message:
            score += 1
            is_correct = True
            break

    actual_answer = questions[current_question]["correct_answer"]

    current_question += 1

    # ================= INTERVIEW COMPLETE =================

    if current_question >= len(questions):

        interview_started = False

        final_score = str(score) + "/100"

        return jsonify({
            "reply":"Interview Completed!\n\nActual Answer:\n"
            + actual_answer
            + "\n\nFinal Score: "
            + final_score
        })

    next_question = questions[current_question]["question"]

    # ================= CORRECT =================

    if is_correct:

        return jsonify({
            "reply":"✅ Your Answer is Correct\n\nActual Answer:\n"
            + actual_answer
            + "\n\nNext Question:\n"
            + next_question
        })

    # ================= WRONG =================

    else:

        return jsonify({
            "reply":"❌ Your Answer is Wrong\n\nActual Answer:\n"
            + actual_answer
            + "\n\nNext Question:\n"
            + next_question
        })


# ================= RUN =================

if __name__ == '__main__':
    app.run(debug=True)
