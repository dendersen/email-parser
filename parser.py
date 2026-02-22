from email_service.emailLib import emailHandler
from email_service.emailReader import email
from event import createEvent
from shared import *
from help import handleHelpEmail

__emailService = emailHandler("", "", "", "") #placeholder, should be unlocked with unlockEmailService before use
__passphrases = {} #empty, shopuld be updated with updatePassPhrases before use
__userName = ""

def unlockEmailService(keyPath: str):
  """unlocks the emailService
  Args:
      keyPath (str): path to key file, should contain username, password, imap_url and smpt_url in separate lines
  """
  global __emailService, __userName
  __userName,__password,__service_in,__service_out = (line.strip() for line in open(keyPath).readlines())
  __emailService = emailHandler(__userName, __password, __service_in, __service_out)

def lockEmailService():
  """locks email service
  does not affect passphrasses
  """
  global __emailService, __userName, __passphrases
  __emailService.lock()
  __emailService = emailHandler("", "", "", "")
  __userName = ""

def updatePassPhrases():
  """reads passPhrases from the emailServer, this allows validating emails
  without calling this, all emails will be invalid
  """
  global __passphrases
  getPassPhrases:list[email] = __emailService.specificList("inbox.secrets", __userName)
  for PassPhraseMail in getPassPhrases:
    if("_passphrase_" in PassPhraseMail.subject.lower()):
      passphrase, user = PassPhraseMail.body.strip().split("\n")
      passphrase = passphrase.strip()
      user = user.strip()
      if(passphrase and user):
        print("valid passphrase from {}".format(user))
        if user in __passphrases:
          print("\tuser already has a passphrase, overwriting with new passphrase")
        __passphrases[user] = passphrase
      elif(user):
        print("missing passphrase in email for user: {}".format(user))
        if user in __passphrases:
          print("\tuser already has a passphrase, removing old passphrase")
          del __passphrases[user]
      elif(passphrase):
        print("something went wrong with parsing passphrase email, missing user")
        print("\temailID: {}, subject: {}, date: {}".format(PassPhraseMail.idNumber,PassPhraseMail.subject,PassPhraseMail.date))
        print("\tsender: {}, ".format(PassPhraseMail.sender))
      else:
        print("missing user and passphrase in email:")
        print("\tsender: {}, ".format(PassPhraseMail.sender))
        print("\tsubject: {}".format(PassPhraseMail.subject))
        print("\tbody: {}".format(PassPhraseMail.body))

def validateUser(user: str, passphrase: str) -> bool:
  return user in __passphrases and __passphrases[user] == passphrase

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

def forgetPassPhrases():
  global __passphrases
  for user in __passphrases:
    __passphrases[user] = None
  __passphrases = {}

def handleEmail(emailContent:emailFields, prevalidated: bool = False) -> bool:
  if not prevalidated and validateEmail(emailContent):
    prevalidated = True
  
  if emailContent["subject"].startswith("event") and prevalidated:
    return createEvent(emailContent)
  
  if emailContent["subject"].startswith("help"):
    return handleHelpEmail(emailContent,__emailService)
  
  return False #no other email types are supported yet

def validateEmail(emailContent:emailFields) -> bool:
  if  "sender" not in emailContent or "id" not in emailContent or "subject" not in emailContent:
    print("missing required fields in email from {}".format(emailContent["sender"]))
    return False
  if not validateUser(emailContent["sender"], emailContent["id"]):
    print("invalid user or passphrase from {}".format(emailContent["sender"]))
    return False
  return True

def validateEmailList(emailContents: list[emailFields]) -> list[bool]:
  return [validateEmail(emailContent) for emailContent in emailContents]

def handleEmailList(emailContents: list[emailFields], validations: list[bool] | None = None) -> list[bool]:
  if validations is None:
    validations = [False] * len(emailContents)
  return [handleEmail(emailContent, prevalidated=validated) for validated, emailContent in zip(validations, emailContents)]

def parseEmailList(emails: list[email] | None) -> list[emailFields]:
  if emails is None:
    return [parseEmail(mail) for mail in __emailService.getAllEmails(False)]
  return [parseEmail(mail) for mail in emails]

def readInbox(unreadOnly: bool = True) -> list[email]:
  __emailService.specific("inbox", unread = unreadOnly) #update inbox to get new emails
  return [* __emailService.getAllEmails(False)]