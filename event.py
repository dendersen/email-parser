from shared import *
import os

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
  
  if not "id" in mail:
    print("missing event id in email from {}".format(mail["sender"]))
    return False
  
  if not "sender" in mail:
    print("missing sender in email from {}".format(mail["sender"]))
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
  
  if not "eventLink" in mail:
    mail["eventLink"] = ""
  
  if not "ticketLink" in mail:
    mail["ticketLink"] = ""
  
  os.makedirs("./events/{}".format(mail["sender"]), exist_ok=True)
  fileName = str(hash(str(mail)))[0:10]
  with open("./events/{}/{}_parsed.email".format(mail["sender"], fileName), "w") as f:
    f.write(str(mail))
  
  return True