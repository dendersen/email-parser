from parser import parseEmailList, unlockEmailService, updatePassPhrases,readInbox,forgetPassPhrases, validateEmailList, handleEmailList, lockEmailService
from email_service.emailLib import email
from shared import emailFields as EmailFields

def parseInbox(keyLocation:str | None, logOutOnFinish: bool = True, unreadOnly:bool=True, markReadOnSuccess: bool = True, markReadOnFailure: bool = False, saveDestination:str = ".") -> None:
  """a single function to deal with all the email parsing nonsens at once
  some parser functions print status when they are done
  prints own status when done
  
  Args:
      keyLocation (str | None): location of key file to unlock email service, if None the email service is assumed to be already unlocked
      unreadOnly (bool, optional): whether to only read unread emails. Defaults to True.
  """
  
  saveDestination = saveDestination
  
  if keyLocation is not None:
    unlockEmailService(keyLocation) #unlock email service if not unlocked
  emails: list[email] = readInbox(unreadOnly)
  parsedEmails: list[EmailFields] = parseEmailList(emails)
  updatePassPhrases() #update passphrases to get new passphrases
  validMask = validateEmailList(parsedEmails)
  forgetPassPhrases() #forget passphrases after reading inbox for security reasons
  successMask = handleEmailList(parsedEmails, validMask)
  
  for email_item, emailFields, valid, success in zip(emails, parsedEmails, validMask, successMask):
    sender = emailFields["sender"] if "sender" in emailFields else "unknown sender"
    subject = emailFields["subject"] if "subject" in emailFields else "unknown subject"
    if not valid:
      print("email from {} with subject {} failed sender validation".format(sender, subject))
      if markReadOnFailure:
        email_item.markAsRead()
    if not success:
      print("email from {} with subject {} failed emailType parsing".format(sender, subject))
      if markReadOnFailure:
        email_item.markAsRead()
    else:
      print("email from {} with subject {} was successfully handled".format(sender, subject))
      if markReadOnSuccess:
        email_item.markAsRead() #mark email as read if it was handled successfully
      elif markReadOnFailure:
        email_item.markAsRead() #mark email as read if it failed handling to avoid trying to handle it again, even if it is valid but failed handling for some reason
  if logOutOnFinish:
    lockEmailService() #lock email service when done to prevent unauthorized access

if __name__ == "__main__":
  parseInbox(".secret", unreadOnly=True, markReadOnSuccess=True, markReadOnFailure=False)