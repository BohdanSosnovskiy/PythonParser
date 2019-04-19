from flask import Flask, render_template, request, url_for, jsonify
import time
import os.path
import urllib.request
app = Flask(__name__)


LINK = 'https://www.google.com'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
id_process = -1
fifo = []

@app.route("/")
def hello():

    return 'Welcome'

@app.route('/result/<int:id_task>')
def show_task(id_task):
    if fifo[id_task]:
        return 'True'
    else:
        req = urllib.request.Request(
            LINK,
            data=None,
            headers={
                'User-Agent': USER_AGENT
            }
        )
        fp = urllib.request.urlopen(req)
        mybytes = fp.read()

        mystr = mybytes.decode("utf8")
        fp.close()
        fifo[id_task] = True
        return 'False'



@app.route('/new', methods=['POST'])
def new_task():
    if request.method == 'POST':
        fifo.append(False)
        url_for('show_task',id_task = len(fifo) - 1)
        id_process = len(fifo)

        return str(len(fifo)-1)


if __name__ == "__main__":
    app.run()
