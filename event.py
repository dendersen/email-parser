from email_service.emailReader import email
from shared import *

def parseTime(timeStr: str) -> tuple[int,int,int,int,int] | str:
  if(len(timeStr.strip().split(" ")) != 2):
    return "invalid date time format"
  date,time = timeStr.strip().split(" ")
  
  if(len(date.split(".")) != 3):
    return "invalid date format"
  if(len(time.split(".")) != 3):
    return "invalid time format"
  
  day,mont,year = date.split(".")
  hour,minute = time.split(".")
  
  return int(year), int(mont), int(day), int(hour), int(minute)

def createEvent(mail: emailFields) -> bool:
  if not mail["subject"].lower().startswith("event"):
    return False
  
  if not "start" in mail or not "end" in mail:
    print("missing start or end time in email from {}".format(mail["sender"]))
    return False
  
  if not "name" in mail:
    print("missing event name in email from {}".format(mail["sender"]))
    return False
  
  if not "location" in mail:
    print("missing event location in email from {}".format(mail["sender"]))
    return False
  
  if not "description" in mail:
    print("missing event description in email from {}".format(mail["sender"]))
    return False
  
  
  
  return True