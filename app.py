from flask import Flask, flash, jsonify, redirect, render_template, request, session, send_file, abort
import csv, json, traceback
from glob import glob


app = Flask(__name__)
app.secret_key = b'_5#y2L"F0Q8z\n\xec]/'

@app.route('/')
def hello_world():
    print("\n =============== Home ===================")
    fileList = getFileList()
    return render_template("index.html", fileList=fileList)


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


@app.route('/save', methods=['GET', 'POST'])
def save():
    if request.method == "POST":
        print("\n =============== Saving Input ===================")
        listName = request.form.get("listName").replace(" ", "_").lower()
        creator = request.form.get("creator").replace(" ", "_").lower()
        test = request.form.get('listVisibility')
        hidden = request.form.get('listVisibility') != "visible"

        phraseList = request.form.get("phrases").strip().split("\r\n")
        phraseList = list(dict.fromkeys(phraseList))  # remove duplicates
        hidden = False
        owner = "test" #todo add owner field
        dataDict = {
            "listName": listName,
            "owner": creator,
            "hidden": hidden,
            "list": phraseList
        }

        print(list, listName)

        ## CSV save method
        #with open(f"listFiles/{listName}.csv", 'w+', newline='') as listFile:
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
        string = i.replace(f"{jsonDir}", "")\
            .replace("_", " ")\
            .replace(".json", "")\
            .replace(r'/', '')\
            .replace('\\', '')\
            .lower().strip()

        namedFileList.append(string)
    return namedFileList


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
