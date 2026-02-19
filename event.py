from shared import *
import os
import time as T

def isLeapYear(year: int) -> bool:
  return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def parseTime(timeStr: str) -> tuple[int,int,int,int,int] | str:
  if(len(timeStr.strip().split(" ")) != 2):
    return "invalid date time format"
  date,time = timeStr.strip().split(" ")
  
  if(len(date.split(".")) != 3):
    return "invalid date format"
  if(len(time.split(".")) != 2):
    return "invalid time format"
  
  day,month,year = date.split(".")
  hour,minute = time.split(".")
  
  if not day.isdigit() or not month.isdigit() or not year.isdigit():
    return "date must be in format DD.MM.YYYY and consist must use numbers in place of DD, MM and YYYY"
  if not hour.isdigit() or not minute.isdigit():
    return "time must be in format HH.MM and consist must use numbers in place of HH and MM"
  
  if int(hour) < 0 or int(hour) > 23:
    return "hour must be between 0 and 23"
  if int(minute) < 0 or int(minute) > 59:
    return "minute must be between 0 and 59"
  if int(month) < 1 or int(month) > 12:
    return "month must be between 1 and 12"
  if int(month) in [4,6,9,11] and int(day) > 30:
    return "day must be between 1 and 30 for month {}".format(month)
  if int(month) == 2 and isLeapYear(int(year)) and int(day) > 29:
    return "day must be between 1 and 29 for month 2 in leap year"
  if int(month) == 2 and not isLeapYear(int(year)) and int(day) > 28:
    return "day must be between 1 and 28 for month 2 in non-leap year"
  
  # allow events up to 10 years in the future 
  #                    /ss/mm/hh/day + epoch+ yy
  t = T.time()
  in20Years = T.gmtime(t).tm_year + 20
  if int(year) < 2000 or int(year) > in20Years:
    return "year must be between 2000 and {}".format(in20Years)
  if int(day) < 1 or int(day) > 31:
    return "day must be between 1 and 31"
  
  return int(year), int(month), int(day), int(hour), int(minute)

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