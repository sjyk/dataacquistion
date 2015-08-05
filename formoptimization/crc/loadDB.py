import environ
from crc import models
import csv
import time

FILENAME = 'crc/CRC_Survey Monkey_Data.csv'
CONFIRM = 'I confirm that I am at least 18 years old.'


with open(FILENAME, 'rb') as csvfile:
	csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')

	count = 0
	for row in csvreader:
		#skip the first line
		if count <= 1:
			count = count + 1
			continue

		row_list = [attr for attr in row]
		print row_list
		a = models.Response(responseId=row_list[0],
			 				collectorId=row_list[1],
			 				startDate = time.strftime('%Y-%m-%d %H:%M',time.strptime(row_list[2], '%m/%d/%y %H:%M')),
			 				endDate = time.strftime('%Y-%m-%d %H:%M',time.strptime(row_list[3], '%m/%d/%y %H:%M')),
			 				confirm = (row_list[4] == CONFIRM),
			 				metroArea = row_list[5],
			 				zipCode = row_list[7],
			 				q1 = row_list[9],
			 				q2 = row_list[10],
			 				q3 = row_list[11],
			 				q4 = row_list[12],
	         				q5 = row_list[13],
			 				q6 = row_list[14],
			 				q7 = row_list[15],
			 				openEnded = row_list[16],
			 				gender = row_list[17],
			 				age = row_list[18],
			 				income = row_list[19],
			 				education = row_list[20])
		a.save()
		count = count + 1