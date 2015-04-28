import mandrill
import datetime
import sys

path = sys.argv[1]
try:
	mandrill_client = mandrill.Mandrill('TOKEN')
	message = {
		'html': open(path).read(100000).replace("\n", "<br>\n"),
		'subject': "Backup log from HOST",
		'from_email': 'mandrila@breezeme.su',
		'from_name': 'peton mailer',
		'to': [{'email': 'RECIPIENT', 'name': ''}],
	}
	result = mandrill_client.messages.send(message=message, async=False)
except mandrill.Error, e:
    # Mandrill errors are thrown as exceptions
    print 'A mandrill error occurred: %s - %s' % (e.__class__, e)