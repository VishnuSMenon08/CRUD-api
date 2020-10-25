CREATE TABLE jobs(
jobID Integer primary key autoincrement,
jobname varchar,
workstation varchar,
startTime datetime,
createdBy varchar

);

CREATE TABLE scheduler(
schedulerName varchar primary key,
password text
);
