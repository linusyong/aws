# Introduction
This is a Python 2.7 script to start / stop AWS EC2 instances depending 
on the `tag`: `op_hours`.

# Requirements
*  python 2.7
*  virtualenv
*  pip
*  awscli setup properly

# Tagging
Currently the supported tag is simply:
```
Key: op_hours
Value: <start-day-of-week>-<stop-day-of-week>:<start-hour-of-day>-<stop-hour-of-day>
```

e.g. `Value: 1-5:0800-1800` will ensure that the instance runs
Monday to Friday, 8:00am to 6:00pm.  It will shutdown / startup
the instance depending on the `op_hours` tag.

# Setup
```
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```
If you have more than 1 version of python (i.e. python 2.7 and python 3 installed) and 
want to specify which Python version you can use `virtualenv --python=/usr/bin/python2.7 venv`.

# Run
```
$ python start-stop-ec2-instances.py
```

# cli
In the cli directory, the bash script is used to generate a session token
since my AWS account is setup to enforce MFA and only allow resources
with token session, I need to run `cli/aws-get-session.sh <token-code> <userid>`
first (and follow the instruction to set the shell variables).

This is a test with signing