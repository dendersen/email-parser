from shared import *
import os

def parseTime(timeStr: str) -> tuple[int,int,int,int,int] | str:
  if(len(timeStr.strip().split(" ")) != 2):
    return "invalid date time format"
  date,time = timeStr.strip().split(" ")
  
  if(len(date.split(".")) != 3):
    return "invalid date format"
  if(len(time.split(".")) != 2):
    return "invalid time format"
  
  day,mont,year = date.split(".")
  hour,minute = time.split(".")
  
  if not day.isdigit() or not mont.isdigit() or not year.isdigit():
    return "date must be in format DD.MM.YYYY and consist must use numbers in place of DD, MM and YYYY"
  if not hour.isdigit() or not minute.isdigit():
    return "time must be in format HH.MM and consist must use numbers in place of HH and MM"
  
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
  
  startTime = parseTime(mail["start"])
  endTime = parseTime(mail["end"])
  if type(startTime) == str:
    print("invalid start time in email from {}".format(mail["sender"]))
    print("\t",startTime)
    return False
  
  if type(endTime) == str:
    print("invalid end time in email from {}".format(mail["sender"]))
    print("\t",endTime)
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
  
  if not "eventlink" in mail:
    mail["eventlink"] = ""
  
  if not "ticketlink" in mail:
    mail["ticketlink"] = ""
  
  os.makedirs("./validEvents/{}".format(mail["sender"]), exist_ok=True)
  stringValue = str(mail)
  fileName = str(hash(stringValue))[1:11]
  with open("./validEvents/{}/{}_parsed.email".format(mail["sender"], fileName), "w+") as f:
    f.write(stringValue)
    f.flush()
  
  return True