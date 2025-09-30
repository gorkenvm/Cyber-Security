from tkinter import *
import datetime


def kontrol_et():
    dosya = open("usom.txt", "r")
    icerik = dosya.read()
    dosya.close()
    ip = entry1.get()
    bugun = datetime.datetime.now()
    if str(ip) in icerik:
        dosya = open("log.txt", "a")
        yazi = str(ip)+"zararli\nTarih:"+str(bugun)+"\n"
        dosya.write(yazi)
        dosya.close()
        v.set("IP zararlidir")
    else:
        dosya.open("log.txt", "a")
        yazi1 = str(ip)+"zararli değildir\nTarih:"+str(bugun)+"\n"
        dosya.write(yazi1)
        dosya.close()
        v.set("IP zararli değildir")


top = Tk()
top.title("USOM IP Kontrol")

B = Button(top, text="Kontrol et", command=kontrol_et)
B.place(x=50, y=50)
B.pack()

label1 = Label(top, text="Kontrol edilecek IP adresini giriniz:")
label1.place(x=50, y=80)
label1.pack()

entry1 = Entry(top)
entry1.place(x=50, y=90)
entry1.pack()

v = StringVar()

entry2 = Entry(top, textvariable=v)
entry2.place(x=50, y=100)
entry2.pack()

top.mainloop()
