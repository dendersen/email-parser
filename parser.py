from email_service.emailLib import emailHandler 
from email_service.emailReader import email
from event import createEvent
from shared import *

userName,password,service_in,service_out = (line.strip() for line in open(".key.secret").readlines())
emailService = emailHandler(userName, password, service_in, service_out)
passphrases = {"dendersen@endersen.dk": "dendersen123"} #test passphrase, should be replaced with actual passphrases from getPassPhrases
reserved_keys = ["subject", "sender", "errors"]

getPassPhrases:list[email] = emailService.specificList("inbox.secrets", userName)
for PassPhraseMail in getPassPhrases:
  if("_passphrase_" in PassPhraseMail.subject.lower()):
    passphrase, user = PassPhraseMail.body.strip().split("\n")
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
      print("subject: {}".format(PassPhraseMail.subject))
      print("body: {}".format(PassPhraseMail.body))

def validateUser(user: str, passphrase: str) -> bool:
  return user in passphrases and passphrases[user] == passphrase

def parseEmail(email: email) -> emailFields:
  emailContent = emailFields()
  final = None
  emailContent["subject"] = email.subject.strip().lower()
  emailContent["sender"] = email.sender.strip().lower()
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
      if value.strip() == "":
        final = key.strip().lower()
        emailContent.setFinal(final)
      else:
        emailContent[key.strip().lower()] = value.strip()
  return emailContent

def handleEmail(mail: email) -> bool:
  emailContent = parseEmail(mail)
  if "sender" not in emailContent or "id" not in emailContent or "subject" not in emailContent:
    print("missing required fields in email from {}".format(mail.sender))
    return False
  if not validateUser(emailContent["sender"], emailContent["id"]):
    print("invalid user or passphrase from {}".format(emailContent["sender"]))
    return False
  
  if emailContent["subject"].startswith("event"):
    return createEvent(emailContent)
  return False #no other email types are supported yet

if __name__ == "__main__":
  #while True:
  emailService.specific("inbox") #update inbox to get new emails
  for mail in emailService.getAllEmails(False):
    print("handling email from {}".format(mail.sender))
    if handleEmail(mail):
      print("email handled successfully")
      mail.markAsRead() #mark email as read if it was handled successfully
    else:
      print("failed to handle email from {}".format(mail.sender))