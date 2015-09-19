import readTable
import readMeta
import os

def getRecordsFromTextFile():
	data = {}
	tb = readMeta.tb
	for i in tb.keys():
		cols = readTable.getColumns(i.lower(),tb)
		vRecords = readTable.getRowsFromTable(i.lower(),cols)
		data = readTable.addTableToHash(data,i.lower(),vRecords)
	
	return data


def writeRecordsToTextFile(data):
	for i in data.keys():
		vRecFile = "./data/"+i.lower()+".txt"
		fRecTextFile = open(vRecFile,'w')
		for a in data[i].keys():
			for b in data[i][a]
				fRecTextFile.write(data[i][a][b])
				fRecTextFile.write('|')#must first check if this is the last column before writing ('|').
			fRecTextFile.write('\n')
		fRecTextFile.close()


records = getRecordsFromTextFile()

for k in records.keys():
	print("\t%s\t" % k.upper(), end="")
	print()

	for k in records[k].keys():
		print("\t%s\t " % k, end="")
		print()

	input('next')