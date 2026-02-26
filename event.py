from shared import *
import os
import time as T

eventDestination = "validEvents"

def isLeapYear(year: int) -> bool:
  return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def daysInMonth(month:int,year:int) -> int:
  if int(month) in [4,6,9,11]: 
    return 30 
  if int(month) == 2 and isLeapYear(int(year)):
    return 29
  if int(month) == 2 and not isLeapYear(int(year)):
    return 28
  return 31

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

class time:
  def __init__(self, year: int | str, month: int | str,day: int | str, hour: int | str,minute: int | str) -> None:
    self.year   = int(year)
    self.month  = int(month)
    self.day    = int(day)
    self.hour   = int(hour)
    self.minute = int(minute)
  
  def copy(self)->"time":
    t = time(self.year,self.month,self.day,self.hour,self.minute)
    return t
  
  def __sub__(self, other:"time") -> "time":
    t = time(0,0,0,0,0)
    
    t.minute = self.minute - other.minute
    t.hour   = self.hour   - other.hour
    t.day    = self.day    - other.day
    t.month  = self.month  - other.month
    t.year   = self.year   - other.year  
    
    if t.minute <= 0:
      t.minute += 60
      t.hour -= 1
    
    if t.hour <= 0:
      t.hour += 24
      t.day -= 1
    
    if t.day <= 0:
      t.month -= 1
      if t.month <= 0:
        t.month += 12
        t.year -= 1
      t.day += daysInMonth(t.month,t.year)
    
    return t
  
  def __bool__(self) -> bool:
    if self.year < 2000:
      return False
    if self.month <= 0:
      return False
    if self.month > 12:
      return False
    if self.day <= 0:
      return False
    if self.day > daysInMonth(self.month, self.year):
      return False
    if self.hour <= 0:
      return False
    if self.hour > 24:
      return False
    return True
  
  def __str__(self) -> str:
    out = ""
    out += str(self.day)   .ljust(2,"0") + "."
    out += str(self.month) .ljust(2,"0") + "."
    out += str(self.year)                + " "
    out += str(self.minute).ljust(2,"0") + "."
    out += str(self.hour)  .ljust(2,"0") + " "
    return out.strip()

class event:
  def __init__(self, description:str, startTime: time, endTime:time, name:str, location:str, host:str, eventLink:str | None = None, ticketLink: str | None = None) -> None:
    self.description = description
    self.startTime =   startTime
    self.endTime =     endTime
    self.name =        name
    self.location =   location
    self.host =        host
    self.eventLink =   eventLink
    self.ticketLink =  ticketLink
  
  def __str__(self) -> str:
    out = ""
    out += str(self.name)       .replace("\n","%\\n") + "\n"
    out += str(self.startTime)  .replace("\n","%\\n") + "\n"
    out += str(self.endTime)    .replace("\n","%\\n") + "\n"
    out += str(self.location)   .replace("\n","%\\n") + "\n"
    out += str(self.host)       .replace("\n","%\\n") + "\n"
    out += str(self.eventLink)  .replace("\n","%\\n") + "\n"
    out += str(self.ticketLink) .replace("\n","%\\n") + "\n"
    out += str(self.description).replace("\n","%\\n") + "\n"
    return out.strip()

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
  
  if not "eventlink" in mail:
    mail["eventlink"] = ""
  
  if not "ticketlink" in mail:
    mail["ticketlink"] = ""
  
  startTime_str = parseTime(mail["start"])
  if type(startTime_str) is str:
    print("invalid start time in email from {}".format(mail["sender"]))
    print("\t",startTime_str)
    return False
  else:
    startTime:time = time(*startTime_str)
  
  endTime_str = parseTime(mail["end"])
  if endTime_str is str:
    print("invalid end time in email from {}".format(mail["sender"]))
    print("\t",endTime_str)
    return False
  else:
    endTime:time = time(*endTime_str)
  
  event_obj = event(mail["description"],startTime,endTime,mail["name"],mail["location"],mail["sender"],mail["eventLink"],mail["ticketlink"])
  
  stringValue = str(event_obj)
  fileName = str(hash(stringValue))[1:11] + ".txt"
  
  savePath = os.path.join(saveDestination,eventDestination,mail["sender"], fileName)
  os.makedirs(savePath, exist_ok=True)
  
  with open(savePath, "w+") as f:
    f.write(stringValue)
    f.flush()
  
  return True
