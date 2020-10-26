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
    try:
        conn = sqlite3.connect('jobs.db')
        cur = conn.execute('''INSERT INTO jobs (jobname,workstation,startTime,createdBy)
        VALUES (?,?,?,?)
        ''',[data.get('jobName'),data.get('workstation'),data.get('startTime'),request.authorization.username])
        conn.commit()
        conn.close()
        return jsonify({"status" : "success","jobID" : cur.lastrowid}),201
    except Exception as ex:
        logging.error(str(ex))
        conn.close()
        return jsonify({'error' : 'Database Error'}),500

@app.route('/getSchedule/<int:job_id>',methods=["GET"])
@authenticate
def get_job(job_id):
    try:
        conn = sqlite3.connect('jobs.db')
        cur = conn.execute("SELECT * FROM jobs WHERE jobID = ?",[str(job_id)])
        job_schedule = cur.fetchone()
        if not job_schedule:
            return jsonify({"message":"jobID Not found"}),200
        return jsonify({
            'jobID' : job_schedule[0],
            'jobName' : job_schedule[1],
            'workstation' : job_schedule[2],
            'jobStartTime' : job_schedule[3],
            'createdBy' : job_schedule[4]
        }),200
    except Exception as ex:
        logging.error(str(ex))
        return jsonify({'error' : 'Database error'}),500

@app.route('/getSchedule',methods=["GET"])
@authenticate
def get_jobs():
    try:
        conn = sqlite3.connect('jobs.db')
        cur = conn.execute("SELECT * FROM jobs")
        job_schedule = cur.fetchall()
        schedule_dict = dict()
        for job in job_schedule:
            schedule_dict[job[0]]= {
                'jobName' : job[1],
                'workstation' : job[2],
                'jobStartTime' : job[3],
                'createdBy' : job[4]
            }
        conn.close()
        return jsonify(schedule_dict),200
    except Exception as ex:
        logging.error(str(ex))
        return jsonify({'error' : 'Database error'}),500

@app.route('/updateSchedule/<int:job_id>',methods=["PATCH"])
@authenticate
def update_schedule(job_id):
    try:
        updated_data = request.get_json()
        conn = sqlite3.connect('jobs.db')
        cur = conn.execute("""UPDATE jobs
        SET workstation = ?, startTime = ? 
        WHERE jobID = ? """,[updated_data.get('workstation'),updated_data.get('startTime'),str(job_id)])
        conn.commit()
        conn.close()
        if cur.rowcount:
            return jsonify({"status" : "success","jobID":job_id}),200
        return jsonify({"message":"jobID not found"}),200
    except Exception as ex:
        logging.error(str(ex))
        conn.close()
        return jsonify({"error" : "Database error"}),500

@app.route("/cancelSchedule/<int:job_id>",methods=["GET"])
@authenticate
def cancel_schedule(job_id):
    try:
        conn = sqlite3.connect("jobs.db")
        cur = conn.execute("DELETE FROM jobs WHERE jobID = ?",[job_id])
        conn.commit()
        conn.close()
        if cur.rowcount:
            return jsonify({"jobID":job_id,"message":"Schedule Cancelled","status":"success"}),200
        return jsonify({"message":"jobID not found"}),200
    except Exception as ex:
        logging.error(str(ex))
        return jsonify({"error":"Database error"}),500

if __name__ == "__main__":
    app.run(debug=True)