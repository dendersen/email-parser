from email_service.emailLib import emailHandler 
from email_service.emailReader import email
from event import createEvent
from shared import *

userName,password,service_in,service_out = (line.strip() for line in open(".key.secret").readlines())
emailService = emailHandler(userName, password, service_in, service_out)
getPassPhrases:list[email] = emailService.specific("secrets", userName)
passphrases = {"dendersen@endersen.dk": "dendersen123"} #test passphrase, should be replaced with actual passphrases from getPassPhrases
reserved_keys = ["subject", "sender", "errors"]

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

def parseEmail(email: email) -> emailFields:
  emailContent = emailFields()
  final = None
  emailContent["subject"] = email.subject.strip().lower()
  emailContent["sender"] = email.sender.strip().lower()
  emailContent["errors"] = []
  for line in email.body.strip().split("\n"):
    if(final is not None):
      emailContent[final] = line.strip()
    elif(":" in line):
      key, value = line.split(":", 1)
      if key.strip().lower() == "":
        print("invalid key in line: {}".format(line))
        emailContent["errors"] = "invalid key in line: {}".format(line)
        continue
      if key.strip().lower() in emailContent:
        print("duplicate key in line: {}".format(line))
        emailContent["errors"] = "duplicate key in line: {}".format(line)
        continue
      if key.strip().lower() in reserved_keys:
        print("reserved key used in line: {}".format(line))
        emailContent["errors"] = "reserved key used in line: {}".format(line)
        continue
      emailContent[key.strip().lower()] = value.strip()
      if(value == ""):
        key.strip().lower()
        final = key.strip().lower()
        emailContent.setFinal(final)
        emailContent[final] = value.strip()
  return emailContent

def handleEmail(mail: email) -> bool:
  emailContent = parseEmail(mail)
  if not validateUser(emailContent["sender"], emailContent["id"]):
    print("invalid user or passphrase from {}".format(emailContent["sender"]))
    return False
  
  if emailContent["subject"].startswith("event"):
    return createEvent(emailContent)
  return False #no other email types are supported yet