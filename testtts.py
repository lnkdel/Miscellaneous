#coding: UTF-8
import PyPDF2
import pyttsx3
import sys

content = ''
book = open('d:/LJY/doc/a111.pdf','rb')
pdfreader = PyPDF2.PdfFileReader(book)
pages = pdfreader.numPages
print(pages)
speaker = pyttsx3.init()
speaker.setProperty('voice', 'zh')
page= pdfreader.getPage(0)
text = page.extractText()
content = text

# if isinstance(text, unicode):
#     print text.encode('gb2312')
# else:
#     print text.decode('utf-8').encode('gb2312')
# print(content.decode('utf-8'))
print(content)
# speaker.say(text)
# speaker.runAndWait()