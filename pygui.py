#!/usr/bin/python
#coding:utf-8
from Tkinter import *
from tkFileDialog import askopenfilename
import qrcode2pdf
import tkMessageBox

class Application(Frame):

    def showError(self):
        # name = self.nameInput.get() or 'world'
        tkMessageBox.showinfo('提示', '请选择文本文件')

    def sfa(self,filename):
        qrcode2pdf.mainFunc(filename)


    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createFileChooser(self):
        # self.aa("2")
	   # filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
       
       filename = askopenfilename()
       if filename and not filename.isspace():
            if filename.endswith('txt'):
                qrcode2pdf.mainFunc(filename)
                tkMessageBox.showinfo('提示', '生成二维码成功')
            else:
                self.showError()
            # qrcode2pdf.mainFunc(filename)
       # print("123")
       # self.sfa(filename)


    def createWidgets(self):
        self.helloLabel = Label(self, text='\n这是一个安行宝二维码批量生成程序\n\n\n')
        self.helloLabel.pack()
        self.heb = Button(self, text='选择输入文件', command=self.createFileChooser)
        self.heb.pack()
        self.helloLabel1 = Label(self, text='')
        self.helloLabel1.pack()
        self.quitButton = Button(self, text='退出', command=self.quit)
        self.quitButton.pack()



app = Application()
app.master.minsize(width=400, height=200)
app.master.maxsize(width=400, height=200)

app.master.title('二维码批量生成器-wzx')
# 主消息循环:
app.mainloop()