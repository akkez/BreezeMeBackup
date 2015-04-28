import ftplib
import os
import time
import sys
import locale
import datetime

ftp_host = ""
ftp_user = ""
ftp_pass = ""

connection = ftplib.FTP(ftp_host)
connection.login(ftp_user, ftp_pass)
locale.setlocale(locale.LC_ALL, 'en_US.utf8')

def listing(connect):
	lines = []
	connection.retrlines('LIST', lines.append)
	ans = []
	for line in lines:
		parts = line.split()
		ans.append((parts[8], parts[4], line[0] == 'd'))
	return ans

def walk(where, indent):
	connection.cwd(where)
	size = 0
	for l in listing(connection):
		if l[2]:
			print '|' + " " * indent + l[0] + ":"
			size += walk(where + "/" + l[0], indent + 2)
		else:
			size += int(l[1])
			print '|' + " " * indent + l[0] + " [" + str(l[1]) + "]"
	return size

def curtime():
	return "[" + time.strftime("%Y.%m.%d %H:%M:%S") + "] "

def download(connect, from_path, to_path, size, threshold):
	f = open(to_path, "wb")
	cur = {"size": 0, "before_next": 0}
	def chunk_received(block):
		cur["size"] += len(block)
		cur["before_next"] += len(block)
		if cur["before_next"] >= threshold:
			print curtime() + "DL " + from_path + ": " + str(cur["size"]) + "/" + str(size) + "..."
			cur["before_next"] = 0
		f.write(block)
	res = connect.retrbinary('RETR ' + from_path, chunk_received)
	f.close()
	return res

def upload_ex(connect, filename, f, total_size, to_path, threshold):
	cur = {"size": 0, "before": 0}
	def chunk_uploaded(block):
		cur["size"] += len(block)
		cur["before"] += len(block)
		if cur["before"] >= threshold:
			print curtime() + "UL " + filename + ": " + str(cur["size"]) + "/" + str(total_size) + "..."
			cur["before"] = 0
	res = connect.storbinary('STOR ' + to_path, f, callback=chunk_uploaded)
	return res

def upload(connect, from_path, to_path, threshold):
	f = open(from_path, "rb")
	size = os.path.getsize(from_path)
	return upload_ex(connect, from_path, f, size, to_path, threshold)
	# f.close()

print "-" * 25
size = walk("/", 2)
print "|"
print "| Total size:", locale.format("%d", size, grouping=True)
print "-" * 25
print ""

if len(sys.argv) > 1 and sys.argv[1] == 'upload_from_stdin':
	filename = "all_" + time.strftime("%Y.%m.%d") + ".zip"
	upload_ex(connection, "STDIN", sys.stdin, 0, filename, 500 * 1000 * 1000)
elif len(sys.argv) > 1 and sys.argv[1] == 'cleanup':
	valid = []
	day = datetime.date.today()
	valid.append((day.strftime("%Y.%m.%d"), "today"))
	monday = day + datetime.timedelta(days=-day.weekday())
	valid.append((monday.strftime("%Y.%m.%d"), "monday"))
	for x in range(0, 3):
		day += datetime.timedelta(-1)
		valid.append((day.strftime("%Y.%m.%d"), "prev"))
		if x < 2:
			monday += datetime.timedelta(weeks=-1)
			valid.append((monday.strftime("%Y.%m.%d"), "monday"))

	today = datetime.date.today()
	fday = datetime.date(day=1, month=today.month, year=today.year)
	valid.append((fday.strftime("%Y.%m.%d"), "fday"))

 	lastMonth = fday - datetime.timedelta(days=1)
 	valid.append((lastMonth.strftime("%Y.%m.01"), "fday"))
 	prevMonth = datetime.date(day=1, month=lastMonth.month, year=lastMonth.year) - datetime.timedelta(days=1)
 	valid.append((prevMonth.strftime("%Y.%m.01"), "fday"))
 	
 	print "Valid archives: "
	for d in valid:
		print "    " + d[0] + " because '" + d[1] + "'"

 	connection.cwd("/")
 	archives = listing(connection)
 	removing = []
 	for f in archives:
 		if f[2]:
 			print "Skip " + f[0] + " because dir."
 			continue
 		name = f[0]
 		if len(name) != 18:
 			print "Deleting " + name + "because length dont equal 18"
 			removing.append(name)
 			continue
 		cdate = name[4:14]
 		alive = False
 		for v in valid:
 			if v[0] == cdate:
 				print "Skip " + f[0] + " because valid (" + v[1] + ")"
 				alive = True
 				break
 		if not alive:
 			print "Deleting " + name + " because does not valid"
 			removing.append(name)
 			continue
 	print "So removing:", removing
 	for r in removing:
 		print connection.delete("/" + r)

	print "cleanup completed."
elif len(sys.argv) > 2 and sys.argv[1] == 'up':
	upload(connection, sys.argv[2], "/" + sys.argv[2].split("/")[-1], 100 * 1000 * 1000)
elif len(sys.argv) > 2 and sys.argv[1] == 'dl':
	download(connection, "/" + sys.argv[2], sys.argv[2], 0, 100 * 1000 * 1000)
elif len(sys.argv) > 2 and sys.argv[1] == 'delete':
	print connection.delete(sys.argv[2])
elif len(sys.argv) > 3 and sys.argv[1] == 'rename':
	print connection.rename(sys.argv[2], sys.argv[3])
else:
	print "Usage: this.py upload_from_stdin"
	print "Usage: this.py cleanup"
	print "Usage: this.py up something.zip"
	print "Usage: this.py dl something.zip"
	print "Usage: this.py delete something.zip"
	print "Usage: this.py rename from.zip to.zip"
