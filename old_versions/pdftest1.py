from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial",size=24)

myText = open("./vision_output.txt", "r")
string1 = myText.read()
myText.close()

string1 = string1.encode(encoding='UTF-8',errors='replace')

pdf.cell(200,500, txt = string1, ln=1, align="C")
##pdf.output("text2pdftest.pdf") 
