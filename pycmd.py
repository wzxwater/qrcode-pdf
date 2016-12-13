import qrcode2pdf
import sys


if(len(sys.argv) < 2):
	print "error : please choose input file"
	exit()

filename = sys.argv[1]


# filename = "/Users/wzx/Documents/qrcode-pdf/input.txt"


qrcode2pdf.mainFunc(filename)