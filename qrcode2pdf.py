#!/usr/bin/python
#coding:utf-8
from PIL import Image, ImageDraw, ImageFont
import qrcode
import os
import img2pdf
import time
from PyPDF2 import PdfFileWriter, PdfFileReader
import re

def generate_relative_path(path):
	return "." + path

curr_time = time.strftime("%Y-%m-%d_%H_%M_%S",time.localtime(time.time()))
# output_dir = generate_relative_path("/" + curr_time)
output_dir = generate_relative_path("/output")
output_img_dir = output_dir + "/img"
output_sub_pdf_dir = output_dir + "/sub_pdf"
output_pdf_dir = output_dir

def generate_img(imei):
	qr = qrcode.QRCode(
	    version=1,
	    error_correction=qrcode.constants.ERROR_CORRECT_H,
	    box_size=10,
	    border=4,
	)
	qr.add_data("{\"imei\":\"" + imei +"\"}");
	qr.make(fit=True)
	return qr.make_image().convert('RGBA')

	# img = qrcode.make("{\"imei\":\"" + imei +"\"}").convert('RGBA')
	# return img

def generate_text(imei,img):
	# make a blank image for the text, initialized to transparent text color
	txt = Image.new('RGBA', img.size, (255,255,255,0))

	# get a fontTimes_New_Roman_Normal
	# fnt = ImageFont.truetype('FreeMono.ttf', 20)
	fnt = ImageFont.truetype(generate_relative_path("/font/Times_New_Roman_Normal.ttf"), 27)
	# fnt = ImageFont.load_default()
	draw = ImageDraw.Draw(img)
	# get a drawing context
	d = ImageDraw.Draw(txt)

	img_width = img.width;
	img_height = img.height;
	text_imei = "IMEI:" + imei;

	str_width, str_height = d.textsize(text_imei, font=fnt)
	# str_width, str_height = dc.GetTextExtent(text_imei)

	# draw text, half opacity
	d.text((img_width/2 - str_width /2,img_height - str_height - 10), "IMEI:" + imei, font=fnt, fill=(0,0,0))
	return txt

def draw_broad(im):
	draw = ImageDraw.Draw(im)
	draw.line((0, 0, 0, im.size[1]-1,im.size[0]-1,im.size[1]-1,im.size[0]-1,0,0,0), fill=(0,0,0))
	# draw.line((0, 0, 0, im.size[1]-1,im.size[0]-1,im.size[1]-1), fill=(0,0,0))
	# draw.line((0, 0, im.size[0],0), fill=(0,0,0))
	# draw.line((im.size[0] -1, 0, im.size[0] -1,im.size[0]), fill=(0,0,0))

def generate_img_text(imei):
	img = generate_img(imei)
	txt = generate_text(imei,img)
	draw_broad(img)
	out = Image.alpha_composite(img, txt)
	# dir = os.path.dirname(__file__)
	# out.save(dir+ "/img/"+imei+ ".png")
	# out.save(imei+ ".png")
	return out

def func_img2pdf(filename):
	pdf_bytes = img2pdf.convert([output_img_dir + "/" + filename +".png"])
	file = open(output_sub_pdf_dir + "/"+filename+".pdf","wb")
	file.write(pdf_bytes)


def mainFunc(input_file_name):

	curr_time = time.strftime("%Y-%m-%d_%H_%M_%S",time.localtime(time.time()))
	# output_dir = generate_relative_path("/" + curr_time)
	output_dir = generate_relative_path("/output")

	output_img_dir = output_dir + "/img"
	output_sub_pdf_dir = output_dir + "/sub_pdf"
	output_pdf_dir = output_dir
	if not os.path.exists(output_img_dir):
	    os.makedirs(output_img_dir)
	if not os.path.exists(output_sub_pdf_dir):
	    os.makedirs(output_sub_pdf_dir)
	if not os.path.exists(output_pdf_dir):
	    os.makedirs(output_pdf_dir)

	temp = generate_img_text("temp").convert('RGBA')
	single_img_withd = temp.width
	single_img_height = temp.height
	padding = 50
	column = 3
	row = 5
	background_width = (single_img_withd + padding) * column +padding
	background_height = (single_img_height + padding) * row + padding
	# background_height = 2000

	# file = open("sample.txt")
	
	# if(len(sys.argv) < 2):
	# 	print "error : please choose input file"
	# 	exit()

	# file = open(sys.argv[1])
	file = open(input_file_name)
	# sys.argv
	image_index = 0
	images_row_in_page = 0

	img_list = []
	base_l_image = Image.new("RGBA",(background_width,background_height),(255,255,255)).convert('RGBA')
	for line in file:
		if line.isspace():
			continue
		if not re.match(r'^\d{15}$', line):
			continue
		if(image_index == 0 or  image_index % (row * column) == 0):
			base_l_image = Image.new("RGBA",(background_width,background_height),(255,255,255)).convert('RGBA')
			img_list.append(base_l_image)
			images_row_in_page = 0
		new_img = generate_img_text(line.strip())
		images_cloum_in_page = image_index % column
		base_l_image.paste(new_img,(padding + images_cloum_in_page*(single_img_withd + padding),padding + images_row_in_page * (single_img_height + padding)))
		image_index += 1
		if(image_index % column == 0):
			images_row_in_page += 1



	# output_filename = output_dir + "/" +curr_time
	# print output_filename

	# print img_list
	temp_file_names = []
	img_i = 0
	for img in img_list:
		filename = curr_time  + "___"+str(img_i)
		temp_file_names.append(filename)
		img.save(output_img_dir + "/" + filename +".png")
		func_img2pdf(filename)
		img_i += 1



	# print generate_relative_path(output_pdf_dir)

	# pdf
	output = PdfFileWriter()
	for name in temp_file_names:	
		input1 = PdfFileReader(open(output_sub_pdf_dir + "/"+name+".pdf", "rb"))
		output.addPage(input1.getPage(0))

	outputStream = open(output_pdf_dir + "/"+curr_time+".pdf", "wb")
	output.write(outputStream)

	print "success!"
	return output_pdf_dir + "/"+curr_time+".pdf"







# qr1 = qrcode.QRCode(
# 	version=1,
# 	error_correction=qrcode.constants.ERROR_CORRECT_H,
# 	box_size=8,
# 	border=4,
# )
# imei = "865067022467529"
# qr1.add_data("{\"imei\":\"" + imei +"\"}");
# qr1.make(fit=True)
# img = qr1.make_image().convert('RGBA')
# img.show()
# print(img.width)
# print(img.height)
#37 74 111


