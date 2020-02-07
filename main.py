from flask import Flask, render_template, request, make_response
import datetime
import json
import random

app = Flask(__name__)

#helper functions

#Get scores
def get_score_list():
    with open("score_list.txt", "r") as score_file:
        score_list = json.loads(score_file.read())
        return score_list


# Return top 3 scores
def get_top_scores():
    top_score_list = get_score_list()
    top_score_list = sorted(top_score_list, key=lambda k: k['attempts'])[:3]
    return top_score_list



top_scores = get_top_scores()
secret = None
user_attempts = None

@app.route("/game", methods=["GET", "POST"])

def game():
    if request.method == "GET":

        cookie_user_name = request.cookies.get("user_name").capitalize()
        return render_template("game.html", name=cookie_user_name)
    elif request.method == "POST":
        score_list = get_score_list()
        global user_attempts
        user_name = request.form.get("name").capitalize()

        while True:
            guess = int(request.form.get("secret_number"))
            print(guess)
            print(secret)


            if guess == secret:
                class ScoreResults():
                    def __init__(self, name, date, attempts):
                        self.name = name
                        self.attempts = attempts
                        self.date = date

                first_attempt = ScoreResults(name=user_name, date=str(datetime.datetime.now()), attempts=user_attempts)
                score_list.append(first_attempt.__dict__)
                with open("score_list.txt", "w") as score_file:
                    score_file.write(json.dumps(score_list))
                message = "You've guessed it - congratulations! It's number " + str(secret) + " Attempts needed: " + str(user_attempts)
                response = make_response(render_template("success.html", message=message, name=user_name))
                response.set_cookie("user_name", user_name)
                return response
            elif guess > secret:
                user_attempts += 1
                message = "Your guess is not correct... try something smaller" + str(secret)
                response = make_response(render_template("success.html", message=message, name=user_name))
                response.set_cookie("user_name", user_name)
                return response
            elif guess < secret:
                user_attempts += 1
                message = "Your guess is not correct... try something bigger" + str(secret)
                response = make_response(render_template("success.html", message=message, name=user_name))
                response.set_cookie("user_name", user_name)
                return response

def get_all_scores():
    best_scores = get_top_scores()
    date = []
    attempts = []
    name = []
    for item in best_scores:
        date.append(item["date"])
        name.append(item["name"])
        attempts.append(item["attempts"])
    return date, attempts, name


@app.route("/scores")
def scores():
    date, attempts, name = get_all_scores()
    cookie_user_name = request.cookies.get("user_name").capitalize()
    return render_template("scores.html", date=date, name=name, attempts=attempts, cookie_user_name=cookie_user_name)


@app.route("/", methods=["GET", "POST"])
def index():
    global secret
    global user_attempts
    user_attempts = 0
    secret = random.randint(1, 5)
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        selection = str(request.form.get("game_choice"))
        print(selection)
        if selection.upper() == "A":
            return render_template("game.html", secret=secret)
        elif selection.upper() == "B":
           date, attempts, name = get_all_scores()
           return render_template("scores.html", date=date, name=name, attempts=attempts)


if __name__ == '__main__':
    app.run()



