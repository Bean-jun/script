from datetime import datetime
from flask import Flask
from flask import render_template, request, url_for, redirect
from utils import SQLiteDB

app = Flask(__name__)

app.debug = True
app.secret_key = "asdfasdfasdf"
db = SQLiteDB("todoList.db")


@app.route('/', methods=["GET", "POST"], endpoint='index')
def index():
    if request.method == "GET":
        top = db.fetch_all('main', is_delete=0)
        down = db.fetch_all('main', is_delete=1)

        context = {
            'top': top,
            'down': down,
        }
        return render_template("index.html", **context)

    if request.method == "POST":
        print(request.form)
        try:
            todo = request.form.get("todo")
        except Exception as e:
            todo = None

        if todo:
            db.insert('main', todo, False)

        return redirect(url_for('index'))


@app.route('/over/', methods=["GET"], endpoint='close')
def close():
    origin_num = request.args.get("origin_num", None)

    if origin_num:
        try:
            flag = db.fetch_one('main', origin_num)[0]
        except Exception as e:
            flag = False

        _ = not flag
        db.update('main', origin_num, _)

    return redirect(url_for('index'))


@app.route('/detail/<int:id>/', methods=["GET", "POST"], endpoint='detail')
def detail(id):
    """
    todo详细
    """
    if request.method == "GET":
        title = db.raw("select content from main where id={}".format(id))
        detail = db.raw("select content, create_time from detail where m_id={}".format(id))
        context = {
            'title': title[0],
            'detail': list(detail),
        }
        print(context)
        return render_template("detail.html", **context)

    if request.method == "POST":

        if request.method == "POST":
            print(request.form)
            try:
                detail = request.form.get("detail")
            except Exception as e:
                detail = None

            if detail:
                db.raw(
                    """insert into detail (content, is_delete, create_time, m_id) values ('{}',{}, '{}',{})"""
                        .format(detail, False, datetime.now(), id))

            return redirect(url_for('detail', id=id))


if __name__ == '__main__':
    app.run()
