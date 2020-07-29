from flask import Flask, flash, jsonify, redirect, render_template, request, session, send_file, abort, make_response
import csv, json, traceback
import sqlalchemy
import time
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect
from glob import glob
import traceback
import random

app = Flask(__name__)
app.secret_key = b'_5#y2L"F0Q8z\n\xec]/'

# =============== Database ===================
uri = 'mysql+pymysql://myadmin:l42e3@localhost:2501/scoreboards'
start = time.time()
engine = create_engine(uri, pool_recycle=3600)


@app.route('/')
def hello_world():
    print("\n =============== Home ===================")
    fileList = getFileList()
    return render_template("index.html", fileList=fileList)


@app.route('/game')
def play_game():
    print("\n =============== Game ===================")
    try:
        phraseList = request.args['list'].replace(" ","_").lower();
        print(f"listFiles/{phraseList}.json")
        with open(f"listFiles/{phraseList}.json") as listFile:
            loadedList = json.load(listFile)

        listWords = loadedList["list"]
        print("Loading list:", loadedList["list"])

        return render_template("game.html", phraseList=phraseList, listWords=listWords)
    except Exception as e:
        print(traceback.format_exc())
        return str(e)


@app.route('/background_process')
def background_process():
    try:
        listArg = request.args.get('list', 0, type=str)

        with engine.connect() as con:
            rs = con.execute(f'SELECT user, MAX(score) as highscore FROM scoreboard WHERE list LIKE "{listArg}" GROUP BY 1 ORDER BY MAX(score) desc LIMIT 10')

            jsonrtn = jsonify({'result': [dict(row) for row in rs]})
            print(jsonrtn)
            return jsonrtn

    except Exception as e:
        print(traceback.format_exc())
        return str(e)

@app.route('/setcookie', methods = ['POST', 'GET'])
def setcookie():
    if request.method == 'POST':
        user = request.form['username']
        print("Storing cookie for user: " + user)

        resp = make_response(redirect('/'))
        resp.set_cookie("user", user)

        return resp

@app.route('/getcookie')
def getcookie():
    try:
        if "user" in request.cookies:
            user = request.cookies.get("user")
            return user
        else:
            return "webUser"
    except Exception as e:
        print(traceback.format_exc())
        return str(e)


@app.route('/api/scoreboarddb')
def scoreboarddbfetch():
    try:
        with engine.connect() as con:
            rs = con.execute('SELECT list, user, score, UNIX_TIMESTAMP(datetime) as unixDatetime  FROM scoreboard')
            jsonrtn = jsonify({'result': [dict(row) for row in rs]})
            print(jsonrtn)
            return jsonrtn

    except Exception as e:
        print(traceback.format_exc())
        return str(e)


@app.route('/api/<phraseList>.json')
def csv_test(phraseList):
    try:
        print("\n =============== API Specific ===================")
        print(f"listFiles/{phraseList}.json")
        with open(f"listFiles/{phraseList}.json") as listFile:
            return json.load(listFile)
    except OSError:
        abort(404)


@app.route('/api')
def displayLists():
    print("\n =============== API Contents ===================")
    fileList = getFileList()
    return json.dumps(fileList)


@app.route('/api/scoreupload', methods=['POST'])
def scoreUpload():
    print("\n =============== API Score Upload ===================")
    list = request.form.get("list")
    user = request.form.get("user")
    score = request.form.get("score")
    datetime = request.form.get("datetime")
    print(list, user, score, datetime)

    with engine.connect() as con:
        rs = con.execute(f'SELECT list, user, score, datetime FROM scoreboard WHERE list LIKE "{list}" AND user LIKE "{user}" AND score = {score} AND datetime LIKE "{datetime}"')
        if len(rs._saved_cursor._result.rows) == 0:
            con.execute(f'INSERT INTO scoreboard (list, user, score, datetime) VALUES ("{list}", "{user}", {score}, "{datetime}")')
            print("Added new score to database -", list, user, score, datetime)

    return "Success"


@app.route('/save', methods=['GET', 'POST'])
def save():
    if request.method == "POST":
        print("\n =============== Saving Input ===================")
        listName = request.form.get("listName").replace(" ", "_").lower().strip()
        creator = request.form.get("creator").replace(" ", "_").lower()
        test = request.form.get('listVisibility')
        hidden = request.form.get('listVisibility') != "visible"

        phraseList = request.form.get("phrases").strip().split("\r\n")
        phraseList = list(dict.fromkeys(phraseList))  # remove duplicates
        hidden = False
        owner = "test"  # todo add owner field
        dataDict = {
            "listName": listName,
            "owner": creator,
            "hidden": hidden,
            "list": phraseList
        }

        print(list, listName)

        ## CSV save method
        # with open(f"listFiles/{listName}.csv", 'w+', newline='') as listFile:
        #    wr = csv.writer(listFile)
        #    for i in list:
        #        wr.writerow([i])

        # JSON save method
        with open(f"listFiles/{listName}.json", 'w+', newline='') as listFile:
            json.dump(dataDict, listFile)

        flash(f"Successfully saved {listName}")
        return redirect("/")

    else:
        return redirect("/")


def getFileList():
    jsonDir = 'listFiles'
    filelist = glob(f'{jsonDir}/*.json')
    namedFileList = []
    for i in filelist:
        string = i.replace(f"{jsonDir}", "") \
            .replace("_", " ") \
            .replace(".json", "") \
            .replace(r'/', '') \
            .replace('\\', '') \
            .lower().strip()

        namedFileList.append(string)
    return namedFileList


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
