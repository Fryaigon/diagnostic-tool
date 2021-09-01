from flask import Flask, render_template, redirect, request, session
import sqlite3
app = Flask(__name__)
app.secret_key = "SUNABACO"

#サイトに入ったらルーム作成者か参加者を選択させる
@app.route('/')
def select():
    return render_template('start.html')

#選択した結果によってページ遷移＆id付与
@app.route('/', methods=["POST"])
def addId():
    if request.form.get('host') == "ルーム作成者":
        connect = sqlite3.connect('icebreak.db')
        cursor = connect.cursor()
        cursor.execute("INSERT INTO user VALUES (null, null, null, null)")
        connect.commit()
        connect.close()
        return redirect('/host')
    else:
        connect = sqlite3.connect('icebreak.db')
        cursor = connect.cursor()
        cursor.execute("INSERT INTO user VALUES (null, null, null, null)")
        connect.commit()
        connect.close()
        return redirect('/join')

#ルームホストの設定
@app.route('/host')
def build():
    return render_template('home.html')

#部屋の情報をDBに格納
@app.route('/host', methods=["POST"])
def home_post():
    capacity = request.form.get('capacity')
    roomname = request.form.get('roomname')
    passcode = request.form.get('pass')
    connect = sqlite3.connect('icebreak.db')
    cursor = connect.cursor()
    cursor.execute("INSERT INTO room VALUES (null, ?, ?, ?, 0, 1)", (capacity, roomname, passcode))
    cursor.execute("UPDATE user SET roomId = (SELECT roomId FROM room ORDER BY roomId DESC LIMIT 1) WHERE id = (SELECT id FROM user ORDER BY id DESC LIMIT 1)")
    connect.commit()
    connect.close()
    return redirect('/checker')

#立てられている部屋の情報を表示
@app.route('/join')
def join():
    connect = sqlite3.connect('icebreak.db')
    cursor = connect.cursor()
    cursor.execute("SELECT roomName,roomCapacity,numberOfUsers FROM room WHERE openFlg = 0")
    room_data = cursor.fetchall()
    room_list =[]
    for row in room_data:
        room_list.append({"name":row[0],"capacity":row[1],"users":row[2]})
    connect.close()
    return render_template('select.html', html_info = room_list)

#部屋名を選択したら表示を切り替え
@app.route('/join',methods={"POST"})
def enter():
    return redirect('/checker')


@app.route('/checker')
def checker():
    return render_template('checker.html')


if __name__  == "__main__":
    app.run(debug=True)