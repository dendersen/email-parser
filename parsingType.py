from email_service.emailReader import email

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

def createEvent(mail: email) -> bool:
  if(not mail.subject.lower().startswith("event creation")):
    return False
  if(not mail.body.strip()):
    return False
  
  emailContent = mail.body.strip().split("\n")
  if(len(emailContent) < 4):
    return False
  
  start = emailContent[0].strip()
  end = emailContent[1].strip()
  title = emailContent[2].strip()
  eventLink = emailContent[3].strip()
  ticketLink = "ticketLink:"
  description = [line for line in emailContent[4:] if line.strip()]
  
  if(description[0].startswith("ticketLink:")):
    ticketLink = description[0].strip()
    description = description[1:]
  
  if(not start.startswith("start:")):
    return False
  if(not end.startswith("end:")):
    return False
  if(not title.startswith("name:")):
    return False
  if(not eventLink.startswith("eventLink:")):
    return False
  if(not ticketLink.startswith("ticketLink:")):
    return False
  if(not description):
    return False
  
  startTime = parseTime(start[len("start:"):].strip())
  endTime = parseTime(end[len("end:"):].strip())
  if(type(startTime) is str):
    print("failed to parse start time: {}".format(startTime))
    return False
  if(type(endTime) is str):
    print("failed to parse end time: {}".format(endTime))
    return False
  
  
  
  return True