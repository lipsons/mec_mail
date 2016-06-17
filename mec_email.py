import sys
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
import json

'''
 Four TODO's are documented in comments below for enhancing this program
'''


def send_email(send_from, send_to, subject, text, mail_user, mail_pwd, files=None):

    # Build Multipart MIME message
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach(MIMEText(text))

    # TODO:  Test passing absolute paths, or setting the absolute path in the config file that is
    # Attach file
    for f in files or []:
        with open(f, "rb") as fil:
            # print fil.read()
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
            part['Content-Disposition'] = "attachment; filename={}".format(basename(f))
            msg.attach(part)

    try:
        # Establish SMTP server, authenticate, and send email message using parameters passed to send_mail function
        smtp = smtplib.SMTP("smtp.gmail.com", 587)  # TODO:  Add smtp server to config file
        smtp.ehlo()
        smtp.starttls()
        smtp.login(mail_user, mail_pwd)
        smtp.sendmail(send_from, send_to, msg.as_string())
        smtp.close()
        print "Successfully sent email to: {}.".format(send_to)
    except KeyError as e:
        print "Invalid account passed, exiting program.\n {}".format(e)
    except Exception as e:
        # TODO:  Too broad, add specific exception handling
        print "Failed to send email\n {}".format(e)


def get_config(credential_file, account):
    """
    Get configuration details to send email.
    The config file (mec_sendmail_config) is in the following json format:

    "acct1": {
      "user": "[account-name]"
      , "pwd": "password"
      , "from": "youremail@gmail.com"
      , "to": "none@thistime.net"
      , "subject": "This is the subject"
      , "body": "This is the body of the email"
      , "filename": "myFile.txt"
      }
    }
    """
    try:
        with open(credential_file) as cred:
            credentials = json.load(cred)
        return credentials[account]
    except Exception as e:
        # TODO:  Too broad, add specific exception handling
        print "Invalid account, exiting program.\n"
        exit()


def main(args):
    """
    Main function receives email account to be used for sending email in the form of an argument

    args[] : The account to be used in order to grab configuration details from config file.

    """
    if len(args) == 1:
        # No args(account) passed, use the default account
        print "No arguments passed, using the 'default' account."
        config = get_config('mec_email_config', 'default')
    elif len(args) == 2:
        # One argument (account) passed, set account from config file
        # TODO: check for valid accounts being passed as arguments
        print "One argument passed, using account: '{}'.".format(args[1])
        config = get_config('mec_email_config', args[1])
    elif len(args) > 2:
        # More than one argument passed, user did not read the readme file
        print "Too many arguments passed, exiting program."
        exit()

    send_email(config['from'], config['to'], config['subject'], config['body'],
               config['user'], config['pwd'], [config['filename']])


if __name__ == '__main__':
    main(sys.argv)

