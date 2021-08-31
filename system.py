from flask import Flask, render_template, redirect, request,session
import sqlite3
app = Flask(__name__)
app.secret_key = "SUNABACO"

#サイトに入ったらルーム作成者か参加者を選択させる
@app.route('/')
def select():
    return redirect('/home')

#立てられている部屋の情報を表示
@app.route('/home')
def roominfo():
    connect = sqlite3.connect('icebreak.db')
    cursor = connect.cursor()
    cursor.execute("SELECT roomName FROM room WHERE openFlg = 0")
    room_data = cursor.fetchall()
    room_list =[]
    for row in room_data:
        room_list.append({"name":row[0]})
    connect.close()
    return render_template('home.html', html_info = room_list)


#部屋の情報をDBに格納
@app.route('/home', methods=["POST"])
def home_post():
    capacity = request.form.get('capacity')
    roomname = request.form.get('roomname')
    passcode = request.form.get('pass')
    connect = sqlite3.connect('icebreak.db')
    cursor = connect.cursor()
    cursor.execute("INSERT INTO room VALUES (null, ?, ?, ?, 0)", (capacity, roomname, passcode))
    connect.commit()
    connect.close()
    return render_template('checker.html')


@app.route('/checker/<int:roomId>')
def checker():
    return render_template('/checker.html')



if __name__  == "__main__":
    app.run(debug=True)