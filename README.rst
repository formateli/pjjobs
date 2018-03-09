PJJobs
========

**PJJobs** (Python + Json Jobs) is a configurable a easy to use jobs gateway.

It works as a daemon waiting for instruction for jobs execution.

Clients send data for a specific jobs in Json format, The PJJobs server then  determines what to do with this job according to its configuration file. It may call a Class for its execution or may route the job to another PJJobs server.


Features
--------

- Written in pure Python.
- Jobs are executed in an asynchronous mode.
- Job marked as 'Queued' wait until jobs of same kind have finished. Useful when a resource must be used by just one process at a time.
- Set a Job easily in the configurable file pjjobs.xml.
- Jobs can be:
    - Routed to another PJJobs server.
    - Executed by a class derived from pjjobs.PJJob class.
- Uses simple sockets connections.
- Uses the well known Json data format for communication.
