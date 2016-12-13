import qrcode2pdf
import sys


if(len(sys.argv) < 2):
	print "error : please choose input file"
	exit()

# file = open(sys.argv[1])
qrcode2pdf.mainFunc(sys.argv[1])