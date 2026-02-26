from email_service.emailLib import emailHandler
from shared import *
import os

signupDestination = "signups"

class signup:
  def __init__(self,emailTo:str, nameOfPerson:str, emailFrom:str) -> None:
    self.emailTo:str = emailTo
    self.name:str = nameOfPerson
    self.emailFrom:str = emailFrom
  
  def __str__(self) -> str:
    out = ""
    out += self.emailTo + "\n"
    out += self.name    + "\n"
    out += self.emailFrom
    return out.strip()

def checkSignup(mail: emailFields, emailService: emailHandler) -> bool:
  if not mail["subject"].lower().startswith("signup"):
    return False
  
  if not "sign" in mail:
    return False
  
  if mail["sender"].lower() != mail["sign"]:
    return False
  
  if not "target" in mail:
    return False
  
  if mail.finalKey == "target":
    for item in mail.final:
      if not item in existingUsers:
        return False
  else:
    if not mail["target"]:
      return False
  
  name = ""
  if mail["subject"].count("_") > 0:
    name = mail["subject"].lower().split("_",1)[1]
    if not name:
      name = ""
  if name is "":
    name = mail["sender"].split("@",1)[0]
  
  targets:list[str] = []
  for internal_user in mail["target"]:
    targets.append(internal_user)
  
  email = mail["sign"]
  
  signup_objs:list[signup] = []
  for internal_user in targets:
    signup_objs.append(signup(email,name,internal_user))
  
  generalPath = os.path.join(saveDestination,signupDestination)
  
  newSignup = False
  for signup_obj in signup_objs:
    path = os.path.join(generalPath,signup_obj.emailFrom)
    fileName = signup_obj.emailTo + "_" + signup_obj.name + ".txt"
    os.makedirs(path, exist_ok=True)
    fullPath = os.path.join(path,fileName)
    if not os.path.isfile(fullPath):
      with open(fullPath,"w") as f:
        f.write(str(signup_obj))
    # send email on successful signup
      
      emailService.sendEmails(
        "Signup Confirmation",
        "Hello {},\n\nYou have been signed up for emails from {}. If you did not request this, please respond immediately to this email. I will manually review this, as this is a beta system and does not have a unsubscribe feature\n\nBest,\n{}".format(signup_obj.name,signup_obj.emailFrom,teamName),
        signup_obj.emailTo
        )
      newSignup = True
    else:
      # send email if signup already exists
      emailService.sendEmails(
        "Signup already exists",
        "Hello {},\n\nYou have already been signed up for emails from {}. If you did not request this, please respond immediately to this email. I will manually review this, as this is a beta system and does not have a unsubscribe feature\n\nBest,\n{}".format(signup_obj.name,signup_obj.emailFrom,teamName),
        signup_obj.emailTo
        )
  
  return newSignup
