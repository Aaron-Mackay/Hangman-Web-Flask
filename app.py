from flask import Flask, flash, jsonify, redirect, render_template, request, session, send_file, abort
import csv
from glob import glob


app = Flask(__name__)


@app.route('/')
def hello_world():
    fileList = getFileList()
    return render_template("index.html", fileList=fileList)


@app.route('/api/<phraseList>.csv')
def csv_test(phraseList):
    try:
        return send_file(f"listFiles/{phraseList}.csv",
                         mimetype='text/csv',
                         attachment_filename=f"{phraseList}.csv",
                         as_attachment=True)
    except OSError:
        abort(404)


@app.route('/save', methods=['GET', 'POST'])
def save():
    if request.method == "POST":
        #todo if filename contains _, if filename used
        listName = request.form.get("listName").replace(" ", "_")
        list = request.form.get("phrases").strip().split("\r\n")
        print(list, listName)
        with open(f"listFiles/{listName}.csv", 'w+', newline='') as listFile:
            wr = csv.writer(listFile)
            for i in list:
                wr.writerow([i])


    else:
        return redirect("/")


def getFileList():
    csvDir = 'listFiles'
    filelist = glob(f'{csvDir}/*.csv')
    namedFileList = []
    for i in filelist:
        string = i.replace(f"{csvDir}\\", "").replace("_", " ").replace(".csv", "").lower().strip()

        namedFileList.append(string)
    print(filelist)
    print(namedFileList)
    return namedFileList

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
