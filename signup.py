from shared import *

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

def checkSignup(mail: emailFields) -> bool:
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
  for target in mail["target"]:
    targets.append(target)
  
  email = mail["sign"]
  
  signup_objs:list[signup] = []
  for target in targets:
    signup_objs.append(signup(email,name,target))
  
  for signup_obj in signup_objs:
    pass
  
  return True
