from flask import Flask,request,Response,jsonify
from functools import wraps
from datetime import datetime
import logging,json
import sqlite3

logging.basicConfig(
    level = logging.INFO,
    filename='server_log.log',
    format="%(levelname)s: %(message)s - %(asctime)s"
)

app = Flask(__name__)

def authenticate(fn):
    @wraps(fn)
    def inner(*args,**kwargs):
        try:
            auth = request.authorization
            conn = sqlite3.connect('jobs.db')
            cur = conn.execute('''SELECT * FROM scheduler
            WHERE schedulerName = ?''',[auth.username])
            scheduler = cur.fetchone()
            if scheduler and scheduler[1] == auth.password:
                logging.info("request authenticated successfully")
            else:
                return jsonify({'error' : 'Authentication Failed'}),401
            conn.close()
            return fn(*args,**kwargs)
        except Exception as ex:
            logging.error(str(ex))
            return jsonify({'error' : 'Database Error'}),500
    return inner

@app.route("/schedule",methods=["POST"])
@authenticate
def shedule():
    data = request.get_json()
    print(data)
    try:
        conn = sqlite3.connect('jobs.db')
        cur = conn.execute('''INSERT INTO jobs (jobname,workstation,startTime,createdBy)
        VALUES (?,?,?,?)
        ''',[data.get('jobName'),data.get('workstation'),datetime.now(),request.authorization.username])
        conn.commit()
        return jsonify({"status" : "success"}),200
    except Exception as ex:
        print(str(ex))
        logging.error(str(ex))
        return jsonify({'error' : 'Database Error'}),500

if __name__ == "__main__":
    app.run(debug=True)