# CRUD-api
CRUD API with basic authentication for scheduling one time Execution jobs on different workstations

# Prerequisites
To Run the server and test the CRUD operations run pip install requirements.txt in cmd/Terminal

# Running Test
To test the CRUD Operation run the flask app by running 
```
python app.py

```
This will run the flask app on the port 5000 by default. You can use Postman tool for testing the API or alternatively you can use the command line tool curl as well.

NOTE: use tuser as username and authpass as the password for basic authentication

### Schedule an Adhoc Job (CREATE)
To Schedule a job , POST the details in json body to the endpoint : http://localhost:5000/schedule (Assuming the app runs locally on the default port)
```
sample payload 
{
"jobName": "Run Service reoport",
"workstation" : "SCM200",
"startTime" : "2020-09-15 18:30:00"}


sample Response
{
"status" : "success",
"jobID" : 2
}
```
### Get the details for a Job (READ)
To get the detials for a particular job that is scheduled, send a GET request to the endpoint : http://localhost:5000/getSchedule/<job_id>
```
Sample Response 

{
    "createdBy": "tuser",
    "jobID": 6,
    "jobName": "Run Weekly validation",
    "jobStartTime": "2020-11-25 21:00:00",
    "workstation": "ECC-100"
}

```

### Get all schedules
To get all the schedules ,  send a GET request to : http://localhost:5000/getSchedule

```
Sample Response
{
    "1": {
        "createdBy": "tuser",
        "jobName": "Run service report",
        "jobStartTime": "2020-10-25 21:21:43.067300",
        "workstation": "Service now"
    },
    "2": {
        "createdBy": "tuser",
        "jobName": "Run service report2",
        "jobStartTime": "2020-10-26 12:16:38.868854",
        "workstation": "BMC remedy now"
    }

}

```
### Change a Schedule (UPDATE)
To update a particular job schedule or workstation for a scheduled job , Send a PATCH request to the endpoint: http://localhost:5000/updateSchedule/<job_id>
```
Sample Payload
{
    "workstation" : "ECC-100",
    "startTime" : "2020-11-25 21:00:00"
}
Sample Response
{
    "jobID": 2,
    "status": "success"
}

```
### Cancel a schedule(DELETE)
To cancel a scheduled job send a GET request to endpoint : http://localhost:5000/cancelSchedule/5
```
Sample Response
{
    "jobID": 5,
    "message": "Schedule Cancelled",
    "status": "success"
}

```
