import re

def read_file(filename):
	eFile = open(filename, 'r')
	content = eFile.read()
	eFile.close()
	return content
	
txt = read_file("harrypotterextract.txt")
paragraphs = re.split("[\t\n\r\f\v]", txt)
for p in paragraphs:
	if "he" in p.split(" ") or "He" in p.split(" "):
		print p
		print ""
