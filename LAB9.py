from tkinter import *
from tkinter import ttk
from tkinter import messagebox, filedialog
from PIL import ImageTk, Image
from tkinter.filedialog import askopenfilename, asksaveasfile
from random import randint
import numpy as np

window = Tk()
window.geometry("680x350")


lb0 = Label(text = "Контейнер")
lb0.place(x = 100,y = 5)


image_label = ttk.Label(window)

image_label.place(x = 10,y = 30)


def display_image(file_path):
    image = Image.open(file_path)
    photo = ImageTk.PhotoImage(image.resize((240,240)))
    image_label.config(image=photo)
    image_label.photo = photo



lb1 = Label(text = "Скрываемый файл")
lb1.place(x = 520,y = 5)


lb3 = Label(text = "Рейт")
lb3.place(x = 355,y = 5)

rate_str = ["1","2","3","4","5","6","7","8"]
lb2 = ttk.Label()
lb2.pack(padx=1,pady=1)
combobox = ttk.Combobox(values=rate_str,state="readonly")
combobox.place(x=300,y=30)

lb2 = ttk.Label()


filepath = ""
hiddenfilepath = ""

def open_carrier():
    global filepath
    global test
    global test2
    filepath = askopenfilename()

    if filepath:
        display_image(filepath)

    return filepath

def open_hiden_file():
    global hiddenfilepath
    hiddenfilepath = askopenfilename()

    return hiddenfilepath

def matching(x,ms,rate,iteration):
    x_p, x_m = x, x
    while (bin(x_p)[2:])[-1 * rate:] != ms[iteration:iteration + rate]:
        x_p += 1
    while (bin(x_m)[2:])[-1 * rate:] != ms[iteration:iteration + rate]:
        x_m -= 1
    if x_p > 255:
        return x_m
    elif x_m < 0:
        return x_p
    if x_p - x == x - x_m:
        rand = randint(0,1)
        if rand == 0:
            return x_m
        else:
            return x_p
    elif x_p - x < x - x_m:
        return x_p
    else:
        return x_m

def hemming(bit_of_pix, message):

    H = np.array([[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                  [0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
                  [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
                  [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]])

    c_str = bit_of_pix[2:7] + bit_of_pix[10:15] + bit_of_pix[17:22]
    c_arr = []
    for i in c_str:
        c_arr.append(int(i))
    c = np.array(c_arr)
    c_new = np.array(c_arr)
    m = message
    s = ((np.dot(H,c) % 2) + m) % 2
    i = 8 * s[3] + 4 * s[2] + 2 * s[1] + s[0]
    if i != 0:
        if c[i-1] == 1:
            c_new[i-1] = 0
        else:
            c_new[i-1] = 1
    c_new_str = ""
    for i in c_new:
        c_new_str += str(i)
    new_bit_of_pix = bit_of_pix[:3] + c_new_str[:5] \
                     + bit_of_pix[8:11] + c_new_str[5:10] \
                     + bit_of_pix[16:19] + c_new_str[10:]
    return new_bit_of_pix


def Encode():
    dest = asksaveasfile()

    message = open(hiddenfilepath, 'r').read()


    img = Image.open(filepath, 'r')
    width, height = img.size

    rate = int(combobox.get())

    message += " end.message."
    b_message = ''.join([format(ord(i), "08b") for i in message])
    pixels = img.load()

    out_img = Image.new("RGB", (width, height))
    new_pixels = out_img.load()
    while len(b_message) % rate != 0:
        b_message += "0"

    if rate * width * height * 3 < len(b_message):

        messagebox.showinfo("Отчет","Длина сообщения слишком высока, выберите контейнер побольше, либо поставьте рейт выше")
    else:

        iteration = 0

        for i in range(width):
            for j in range(height):
                r,g,b = pixels[i,j]
                if iteration < len(b_message):
                    r_n = bin(r)[2:]
                    if len(r_n) < 8:
                        r_n = ("0" * (8 - len(r_n))) + r_n
                    r_n = r_n[:-1*rate] + b_message[iteration:iteration+rate]
                    r = int(r_n, 2)
                    iteration += rate
                if iteration < len(b_message):
                    g_n = bin(g)[2:]
                    if len(g_n) < 8:
                        g_n = ("0" * (8 - len(g_n))) + g_n
                    g_n = g_n[:-1*rate] + b_message[iteration:iteration+rate]
                    g = int(g_n, 2)
                    iteration += rate
                if iteration < len(b_message):
                    b_n = bin(b)[2:]
                    if len(b_n) < 8:
                        b_n = ("0" * (8 - len(b_n))) + b_n
                    b_n = b_n[:-1*rate] + b_message[iteration:iteration+rate]
                    b = int(b_n, 2)
                    iteration += rate
                new_pixels[i,j] = (r,g,b)
        out_img.save(dest.name, format="BMP")

        messagebox.showinfo("Отчет","Сообщение успешно внедрено.")


def Encode_LSBM():
    dest = asksaveasfile()

    message = open(hiddenfilepath, 'r').read()

    img = Image.open(filepath,'r')
    width, height = img.size

    rate = int(combobox.get())

    message += " end.message."
    b_message = ''.join([format(ord(i), "08b") for i in message])
    pixels = img.load()

    out_img = Image.new("RGB", (width, height))
    new_pixels = out_img.load()
    while len(b_message) % rate != 0:
        b_message += "0"

    if rate * width * height * 3 < len(b_message):

        messagebox.showinfo("Отчет","Длина сообщения слишком высока, выберите контейнер побольше, либо поставьте рейт выше")
    else:
        iteration = 0

        for i in range(width):
            for j in range(height):
                r,g,b = pixels[i,j]
                if iteration < len(b_message):
                    r = matching(r,b_message,rate,iteration)
                    iteration += rate
                if iteration < len(b_message):
                    g = matching(g, b_message, rate, iteration)
                    iteration += rate
                if iteration < len(b_message):
                    b = matching(b, b_message, rate, iteration)
                    iteration += rate
                new_pixels[i,j] = (r,g,b)

        out_img.save(dest.name, format="BMP")

        messagebox.showinfo("Отчет","Сообщение успешно внедрено.")


def Encode_Heming():
    dest = asksaveasfile()

    message = open(hiddenfilepath, 'r').read()

    img = Image.open(filepath, 'r')
    width, height = img.size

    rate = 4

    message += " end.message."
    b_message = ''.join([format(ord(i), "08b") for i in message])
    pixels = img.load()

    out_img = Image.new("RGB", (width, height))
    new_pixels = out_img.load()
    while len(b_message) % rate != 0:
        b_message += "0"

    if rate * width * height  < len(b_message):

        messagebox.showinfo("Отчет","Длина сообщения слишком высока, выберите контейнер побольше, либо поставьте рейт выше.")
    else:
        iteration = 0

        for i in range(width):
            for j in range(height):
                r,g,b = pixels[i,j]
                if iteration < len(b_message):
                    r_b, g_b, b_b = bin(r)[2:], bin(g)[2:], bin(b)[2:]
                    print(r_b, g_b, b_b)
                    while len(r_b) != 8:
                        r_b = "0" + r_b
                    while len(g_b) != 8:
                        g_b = "0" + g_b
                    while len(b_b) != 8:
                        b_b = "0" + b_b

                    bit_of_pix = r_b + g_b +b_b
                    b_s_m = b_message[iteration:iteration + rate]
                    b_arr = np.array([int(b_s_m[0]),int(b_s_m[1]),int(b_s_m[2]),int(b_s_m[3])])
                    new_bit_of_pix = hemming(bit_of_pix,b_arr)
                    r, g, b = int(new_bit_of_pix[:8],2), int(new_bit_of_pix[8:16],2), int(new_bit_of_pix[16:24],2)
                    iteration += rate
                new_pixels[i,j] = (r, g, b)

        out_img.save(dest.name, format="BMP")

        messagebox.showinfo("Отчет","Сообщение успешно внедрено.")

def Decod_heming():

    img = Image.open(filepath, 'r')
    width, height = img.size

    rate = 4

    H = np.array([[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                  [0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
                  [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
                  [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]])

    pixels = img.load()
    hidden_bits = ""
    for i in range(width):
        for j in range(height):
            h_b = ""
            r, g, b = pixels[i, j]
            r_b = bin(r)[2:]
            g_b = bin(g)[2:]
            b_b = bin(b)[2:]
            while len(r_b) != 8:
                r_b = "0" + r_b
            while len(g_b) != 8:
                g_b = "0" + g_b
            while len(b_b) != 8:
                b_b = "0" + b_b
            bit_of_pix = r_b + g_b + b_b
            c_str = bit_of_pix[3:8] + bit_of_pix[11:16] + bit_of_pix[19:]
            c_arr = []
            for k in c_str:
                c_arr.append(int(k))
            c = np.array(c_arr)

            hiden_bits_arr = np.dot(H,c) % 2
            h_b = str(hiden_bits_arr[0]) + str(hiden_bits_arr[1]) + str(hiden_bits_arr[2]) + str(hiden_bits_arr[3])
            hidden_bits += h_b

    message = ""
    iter = 1
    if len(hidden_bits) % 8 != 0:
        hidden_bits += "0" * (len(hidden_bits) % 8)
    for i in range(0, len(hidden_bits), 8):
        message += chr(int(hidden_bits[i:i + 8], 2))
        if len(message) / 17 == iter:
            ind = message.find(" end.message.")
            iter += 1
            if ind > 0:
                file = open("extracted_file.txt", "w")
                file.write(message[:ind])
                file.close()

                messagebox.showinfo("Скрытое сообщение", message[:ind])
                messagebox.showinfo("Отчет","Скрытое сообщение извлечено.")
                return True


    messagebox.showinfo("Отчет","Скрытого сообщения в контейнера не обнаружено.")


def Decode():


    img = Image.open(filepath, 'r')
    width, height = img.size

    rate = int(combobox.get())

    pixels = img.load()
    hidden_bits = ""

    for i in range(width):
        for j in range(height):
            r, g, b = pixels[i, j]
            r_n = bin(r)[2:]
            if len(r_n) < 8:
                r_n = ("0" * (8 - len(r_n))) + r_n
            g_n = bin(g)[2:]
            if len(g_n) < 8:
                g_n = ("0" * (8 - len(g_n))) + g_n
            b_n = bin(b)[2:]
            if len(b_n) < 8:
                b_n = ("0" * (8 - len(b_n))) + b_n
            hidden_bits += r_n[rate*-1:] + g_n[rate*-1:] + b_n[rate*-1:]

    message = ""
    iter = 1
    if len(hidden_bits) % 8 != 0:
        hidden_bits += "0" * (len(hidden_bits) % 8)
    for i in range(0,len(hidden_bits),8):
        message += chr(int(hidden_bits[i:i+8],2))
        if len(message) / 17 == iter:
            ind = message.find(" end.message.")
            iter += 1
            if ind > 0:
                file = open("extracted_file.txt", "w")
                file.write(message[:ind])
                file.close()

                messagebox.showinfo("Скрытое сообщение",message[:ind])
                messagebox.showinfo("Отчет","Скрытое сообщение извлечено.")
                return True


    messagebox.showinfo("Отчет","Скрытого сообщения в контейнере не обранужено.")

b1 = Button(text = "Выбор контейнера",width = 15, height = 1)
b1.config(command = open_carrier)
b1.place(x = 70,y = 280)

b2 = Button(text = "Выбор файла",width = 15, height = 1)
b2.config(command = open_hiden_file)
b2.place(x = 515,y = 35)

b3 = Button(text = "LSB-R",width = 15, height = 1)
b3.config(command = Encode)
b3.place(x = 310,y = 60)

b4 = Button(text = "LSB-M",width = 15, height = 1)
b4.config(command = Encode_LSBM)
b4.place(x = 310,y = 90)

b5 = Button(text = "Извлечение",width = 15, height = 1)
b5.config(command = Decode)
b5.place(x = 310,y = 120)

b6 = Button(text = "Хемминг",width = 15, height = 1)
b6.config(command = Encode_Heming)
b6.place(x = 310,y = 150)

b7 = Button(text = "Извлечение Хем",width = 15, height = 1)
b7.config(command = Decod_heming)
b7.place(x = 310,y = 180)

window.mainloop()
