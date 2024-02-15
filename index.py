from flask import Flask, request, jsonify
import mysql.connector

api = Flask(__name__)


@api.route("/adduser", methods=['Post'])
def adduser():
    conn = mysql.connector.connect(
        host="localhost",
        user="testuser",
        database="lernen"
    )

    curser = conn.cursor()
    data = request.json

    if not data.get("vorname") or not data.get("nachname")  or not data.get("snueslis_täglich"):
        return jsonify({'status': 'Not all arguments were passed!', 'httpcode': 400}), 400

    try:
        query = "Insert Into `snuskonsum` (`uid`, `vorname`, `nachname`, `snueslis_täglich`) Values (NULL, %s, %s, %s)"
        curser.execute(
            query, (data["vorname"], data["nachname"], data["snueslis_täglich"]))
        conn.commit()
        conn.close()
        return jsonify({'status': 'User and number of snueslis have been added successfully', 'httpcode': 201}), 201
    except Exception as a:
        print("Error:", a)
        conn.close()
        return {'error': str(a)}, 500


@api.route("/delete", methods=['Post'])
def delete():
    conn = mysql.connector.connect(
        host="localhost",
        user="testuser",
        database="lernen"
    )
    curser = conn.cursor()
    data = request.json



    if not data.get("uid"):
        return jsonify({'status': 'Not all arguments were passed!', 'httpcode': 400}), 400

    try:
        query = "SELECT * FROM promille WHERE uid = '%s'"
        curser.execute(
            query, (int(data["uid"]),))
        user = curser.fetchone()
        if not user:
            return jsonify({'status': 'User does not exist', 'httpcode': 404}), 404
        



        query = "DELETE FROM promille WHERE uid = '%s'"
        curser.execute(
            query, (int(data["uid"]),))
        conn.commit()
        conn.close()
        return jsonify({'status': 'User was deleted', 'httpcode': 204}), 204
        

    except Exception as a:
        print("Error:", a)
        conn.close()
        return {'error': str(a)}, 500


if __name__ == '__main__':
    api.run(debug="true", port=5000)
