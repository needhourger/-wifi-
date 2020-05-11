# -*- coding:utf-8 -*-
import os
import json
import time
import ctypes
import base64
import requests
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

ctypes.windll.shcore.SetProcessDpiAwareness(1)
ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)

if getattr(sys, "frozen", False):
    WORK_AREA = sys._MEIPASS
else:
    WORK_AREA, _ = os.path.split(os.path.abspath(__file__))


class ByteEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode("utf-8")
        return json.JSONEncoder.default(self, obj)


class GUI():
    LOGIN_URL = "http://a.nuist.edu.cn/index.php/index/login"
    LOGOUT_URL = "http://a.nuist.edu.cn/index.php/index/logout"

    domains = ["南京信息工程大学", "中国移动", "中国电信", "中国联通"]
    domainsCode = ["NUSIT", "CMCC", "ChinaNet", "Unicom"]

    isSaved = False

    def __init__(self):
        super().__init__()
        self.window = Tk()
        self.window.title("One Key Stupid Wifi")

        self.window.tk.call('tk', 'scaling', ScaleFactor/75)
        self.window.update()
        self.window.iconbitmap(os.path.join(WORK_AREA, "images/game.ico"))
        # self.window.iconbitmap("images/game.ico")
        self.window.resizable(0, 0)

        self.menubar = Menu(self.window)
        self.menubar.add_command(label="关于", command=self.show_about)
        self.window.config(menu=self.menubar)
        # self.menubar.pack()

        self.frame = Frame(self.window)
        self.frame.pack()

        self.frameR = Frame(self.frame)
        self.frameR.pack(side="right")
        self.image = PhotoImage(file=os.path.join(
            WORK_AREA, "images/image0.png"))
        # self.image=PhotoImage(file="images/image0.png")
        self.imagelable = Label(
            self.frameR, image=self.image, foreground="white")
        self.imagelable.pack()

        self.frameL = Frame(self.frame)
        self.frameL.pack(side="left")

        self.labelTitle = Label(
            master=self.frameL, text="STUPID WIFI", font=("黑体", 20))
        self.labelTitle.pack()

        self.seperator0 = Separator(self.frameL)
        self.seperator0.pack(fill=X)

        self.frame0 = Frame(self.frameL)
        self.frame0.pack()
        self.seperator1 = Separator(self.frameL)
        self.seperator1.pack(fill=X)

        self.frame1 = Frame(self.frameL)
        self.frame1.pack()
        self.seperator2 = Separator(self.frameL)
        self.seperator2.pack(fill=X)

        self.frame2 = Frame(self.frameL)
        self.frame2.pack()
        self.seperator3 = Separator(self.frameL)
        self.seperator3.pack(fill=X)
        self.labelUsername = Label(master=self.frame0, text="用户名  ")
        self.labelUsername.pack(side="left")

        self.labelPassword = Label(master=self.frame1, text="密   码  ")
        self.labelPassword.pack(side="left")

        self.labelArea = Label(master=self.frame2, text="认证域  ")
        self.labelArea.pack(side="left")

        self.usernameEntry = Entry(master=self.frame0, show=None)
        self.usernameEntry.pack(side="right")

        self.passwordEntry = Entry(master=self.frame1, show="*")
        self.passwordEntry.pack(side="right")

        self.areaListbox = Listbox(
            master=self.frame2, selectmode="browse", height=5)
        for i in self.domains:
            self.areaListbox.insert("end", i)
        self.areaListbox.bind("<Button-1>", self.listbox_activate)
        self.areaListbox.pack(side="right")

        self.seperator = Separator(self.window, orient=HORIZONTAL)
        self.seperator.pack(fill=X)

        self.textarea = Text(self.window, height=5, state=DISABLED)
        self.textarea.pack()

        self.button = Button(master=self.window, text="认证")
        self.button.bind("<Button-1>", self.auth_wifi)
        self.button.pack(fill=X)

        if self.loadData():
            self.auth_wifi(None)

    def show_about(self):
        messagebox.showinfo("关于",
                            """
One key Stupid wifi
                --code by cc
license cc-by-nc
""")

    def listbox_activate(self, event):
        index = self.areaListbox.curselection()
        if index:
            self.areaListbox.activate(index)

    def auth_wifi(self, event):
        self.textarea["state"] = NORMAL
        self.textarea.delete(0.0, END)
        self.textarea.insert(END, "认证中\n")
        self.window.update()

        username = self.usernameEntry.get()
        password = self.passwordEntry.get()
        x = self.areaListbox.curselection()
        # print(x)

        password = base64.b64encode(password.encode("utf-8"))
        payload = {'username': username, 'password': password,
                   'enablemacauth': '0', "domain": "NUIST"}
        if x:
            if len(self.domains) > x[0]:
                payload["domain"] = self.domainsCode[x[0]]
        else:
            messagebox.showinfo(title='提示', message='请选择认证域')
            return

        r = requests.post(self.LOGIN_URL, data=payload)
        data = json.loads(r.text)
        # print(data)
        if not data:
            messagebox.showerror("警告", "No data response！")
            return
        if data.get("status", 0) == 1:
            if not self.isSaved:
                self.isSaved = True
                self.saveData(payload)

            self.textarea.insert(END, data.get("info", "")+"\n")
            self.textarea.insert(END, data.get("logout_domain", "")+"\n")
            self.textarea.insert(END, data.get("logout_location", "")+"\n")
            self.textarea.insert(END, data.get("logout_ip", "")+"\n")
            self.textarea["state"] = DISABLED

            self.button["text"] = "注销"
            self.button.unbind("<Button-1>")
            self.button.bind("<Button-1>", self.logout_wifi)
        else:
            msg = data.get("info", "")
            if msg == "用户已登录":
                if not self.isSaved:
                    self.isSaved = True
                    self.saveData(payload)

                self.textarea.insert(END, data.get("info", "")+"\n")
                self.textarea.insert(END, data.get("logout_domain", "")+"\n")
                self.textarea.insert(END, data.get("logout_location", "")+"\n")
                self.textarea.insert(END, data.get("logout_ip", "")+"\n")
                self.textarea["state"] = DISABLED

                self.button["text"] = "注销"
                self.button.unbind("<Button-1>")
                self.button.bind("<Button-1>", self.logout_wifi)
                return
            messagebox.showinfo("认证失败", msg)
        self.textarea["state"] = DISABLED
        return

    def logout_wifi(self, event):
        self.textarea["state"] = NORMAL
        self.textarea.delete(0.0, END)
        self.textarea.insert(END, "注销中\n")
        self.window.update()

        r = requests.post(self.LOGOUT_URL)
        data = json.loads(r.text)
        # print(data)
        if not data:
            messagebox.showerror("警告", "No data response!")
            return
        if data.get("status", 0) == 1:
            self.textarea.insert(END, data.get("info"))
            self.button["text"] = "认证"
            self.button.unbind("<Button-1>")
            self.button.bind("<Button-1>", self.auth_wifi)
        else:
            messagebox.showwarning("警告", data.get("info"))
        self.textarea["state"] = DISABLED

    def saveData(self, data):
        with open("data.json", "w", encoding="utf-8") as f:
            # print("saveData:",data)
            json.dump(data, f, cls=ByteEncoder)

    def loadData(self):
        if not os.path.exists("data.json"):
            self.isSaved = False
            return
        self.isSaved = True

        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            # print("loadData:",data)

            if data:
                self.usernameEntry.delete(0, END)
                self.usernameEntry.insert(0, data.get("username", ""))
                self.passwordEntry.delete(0, END)
                self.passwordEntry.insert(
                    0, base64.b64decode(data.get("password", "")))
                self.areaListbox.selection_set(
                    self.domainsCode.index(data.get("domain", "")) if data.get("domain", "") in self.domainsCode else 0)
                return True
        return False

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    win = GUI()
    win.run()
