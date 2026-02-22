from shared import *
from os import path
from email_service.emailLib import emailHandler
helpTopics: dict[str, tuple[str, str]] = {
  "event": ("event.txt", "you have recieved an event email in the correct format for an event, the subject is: event_example, it also has good to know information\n\tthis is the system used to create events that this system can help notify users about, this way you can make sure everyone gets the event information in a format that is easy to read and understand, and also allows the system to easily parse the event information to create events based on the email content"),
  "help": ("help.txt", "this is a 'command' email requesting help with specific topics, or all topics if no specific topics are requested, the subject is: helpSystem, the body contains the topics you want help with, one topic per line, for example:\n\thelp\n\tevent\n\nthis would request help with events and general help, while just sending an email with the subject 'help' and an empty body would request help with all topics"),
  
  }

def handleHelpEmail(emailContent: emailFields, emailService: emailHandler) -> bool:
  sender = emailContent["sender"]
  helpEmails: list[str | None] = []
  helpMessage = "Hello, this is the help message for the email parser."
  if emailContent["subject"].strip().lower() != "help":
    return False
  foundKey = False
  for key in emailContent:
    if key not in reserved_keys and key:
      if emailContent[key].strip().lower() == "yes":
        if key in helpTopics:
          foundKey = True
          helpMessage += "\n\n{}:\n{}".format(key, helpTopics[key][1])
          helpEmails.append(helpTopics[key][0])
        else:
          helpMessage += "\n\n{}:\nNo help available for this topic.".format(key)
  
  if not foundKey:
    helpMessage += "\n\tsince no specific help topic was requested, here are all responses.\n\tEXAMPLES WILL NOT BE SENT, except help with help"
    helpEmails.append(helpTopics["help"][0])
    for key in helpTopics:
      helpMessage += "\n\n{}:\n{}".format(key, helpTopics[key][1])
  emailService.sendEmails("Help Response", helpMessage, sender)
  
  for helpEmail in helpEmails:
    if helpEmail is not None:
      with open(path.join("./emailTemplates",helpEmail), "r") as f:
        first = True
        subject = ""
        msg = ""
        for line in f:
          msg = ""
          if first:
            subject = "Help Response: {}".format(helpEmail)
            first = False
          else:
            msg += line.strip() + "\n"
        
        emailService.sendEmails(subject, msg, sender)
  
  return True