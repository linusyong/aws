
import boto3
import datetime
import logging
import string
import time

def inOpDays(op_days):
  start_day = string.split(op_days, "-")[0]
  stop_day = string.split(op_days, "-")[1]
  return int(start_day) <= datetime.datetime.today().isoweekday() <= int(stop_day)

def inOpHours(op_hours):
  start_hour = string.split(op_hours, "-")[0]
  stop_hour = string.split(op_hours, "-")[1]
  return int(start_hour) <= int(time.strftime("%H%M", time.localtime())) <= int(stop_hour)

ec2 = boto3.resource('ec2')

filters = [{'Name':'tag-key', 
            'Values':['op_hours']}, 
           {'Name':'instance-state-name',
            'Values':['running','shutting-down','stopping','stopped']}]

instances = ec2.instances.filter(Filters=filters)

for instance in instances:
  op_string = [ tag['Value'] for tag in instance.tags if tag['Key'] == "op_hours" ][0]

  op_days = string.split(op_string, ":")[0]
  op_hours = string.split(op_string, ":")[1]

  if (inOpDays(op_days) and inOpHours(op_hours)):
    if (instance.state['Name'] != "running"):
      print "Starting " + instance.instance_id
      instance.start()
    else:
      print instance.instance_id + " is already " + instance.state['Name']
  else:
    if (instance.state['Name'] not in ["stopped", "stopping"]):
      print "Stopping " + instance.instance_id
      instance.stop()
    else:
      print instance.instance_id + " is already " + instance.state['Name']
