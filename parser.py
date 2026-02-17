from email_service.emailLib import emailHandler 
from email_service.emailReader import email
from enum import Enum
userName,password,service_in,service_out = (line.strip() for line in open(".secret.key").readlines())

emailService = emailHandler(userName, password, service_in, service_out)

getPassPhrases:list[email] = emailService.specific("secrets", "calender@dendersen.dk")

passphrases = {}

class UserProfile:
  def __init__(self, name: str, passphrase: str):
    self.name = name
    self.passphrase = passphrase

class Target_enum(Enum):
  keyChange = 0
  eventCreation = 1
  eventDeletion = 2
  eventEdit = 3
  promotion = 4
  importantNotification = 5

for mail in getPassPhrases:
  if("_passphrase_" in mail.subject.lower()):
    passphrase, user = mail.body.strip().split("\n")
    passphrase = passphrase.strip()
    user = user.strip()
    if(passphrase and user):
      print("valid passphrase from {}".format(user))
      passphrases[user] = passphrase
    elif(user):
      print("missing passphrase from {}".format(user))
    elif(passphrase):
      print("missing user with passphrase: {}".format(passphrase))
    else:
      print("missing user and passphrase in email:")
      print("subject: {}".format(mail.subject))
      print("body: {}".format(mail.body))

def validateUser(user: str, passphrase: str) -> bool:
  return user in passphrases and passphrases[user] == passphrase

def parseEmail(email: email) -> tuple[UserProfile,Target_enum, str] | None:
  user = UserProfile(email.sender, email.body.strip().split("\n")[0].strip())
  email.body = "\n".join(email.body.strip().split("\n")[1:]).strip()
  subject = email.subject.lower()
  if("key change" in subject):
    return user, Target_enum.keyChange, email.body.strip()
  elif("event creation" in subject):
    return user, Target_enum.eventCreation, email.body.strip()
  elif("event deletion" in subject):
    return user, Target_enum.eventDeletion, email.body.strip()
  elif("event edit" in subject):
    return user, Target_enum.eventEdit, email.body.strip()
  elif("promotion" in subject):
    return user, Target_enum.promotion, email.body.strip()
  elif("important notification" in subject):
    return user, Target_enum.importantNotification, email.body.strip()
  else:
    print("unknown target for email with subject: {}".format(email.subject))
    return None

def handleEmail(email: email):
  parseResult = parseEmail(email)
  if(parseResult is None):
    return
  user, target, content = parseResult
  
  if(target == Target_enum.keyChange):
    print("handling key change request for user: {}".format(user.name))
    # handle key change
  elif(target == Target_enum.eventCreation):
    print("handling event creation for user: {}".format(user.name))
    # handle event creation
  elif(target == Target_enum.eventDeletion):
    print("handling event deletion for user: {}".format(user.name))
    # handle event deletion
  elif(target == Target_enum.eventEdit):
    print("handling event edit for user: {}".format(user.name))
    # handle event edit
  elif(target == Target_enum.promotion):
    print("handling promotion for user: {}".format(user.name))
    # handle promotion
  elif(target == Target_enum.importantNotification):
    print("handling important notification from user: {}".format(user.name))
    # handle important notification