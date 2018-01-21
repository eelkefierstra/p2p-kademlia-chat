#!/usr/bin/env python3
'''
@author: Eelke
The GUI for the chat application
'''

import tkinter as tk
from twisted.internet import reactor
from twisted.internet.task import react
import random


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)

        self.grid(sticky=tk.N+tk.E+tk.S+tk.W)
        self.createWidgets()

    def createWidgets(self):
        # Build the chat listing
        self.chatList = tk.Frame(self)
        self.chatList.grid(row=0, column=0)

        self.chatScroll = tk.Scrollbar(self.chatList, orient=tk.VERTICAL)
        self.chatScroll.grid(row=0, column=1, sticky=tk.N+tk.S)
        self.chatListBox = tk.Listbox(self.chatList, yscrollcommand=self.chatScroll.set)
        self.chatListBox.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.chatScroll['command'] = self.chatListBox.yview
        self.chatListButton = tk.Button(self.chatList, text='Select chat', command=self.changeChat)
        self.chatListButton.grid(row=1, column=0, columnspan=2, sticky=tk.E+tk.W)

        # Build the chat message view
        self.configureChatmessageList()

        self.quitButton = tk.Button(self, text='Quit', command=reactor.stop, bg='#f22')
        self.quitButton.grid(row=1, column=0, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)

    def configureChatmessageList(self):
        self.chatView = tk.Frame(self)
        self.chatView.grid(row=0, column=1, sticky=tk.N+tk.E+tk.S+tk.W)

        self.chatMessageCanvas = tk.Canvas(self.chatView, borderwidth=0, background='#fff')
        self.chatMessageFrame = tk.Frame(self.chatMessageCanvas, background='#fff')
        self.chatMessageScroll = tk.Scrollbar(self.chatView, orient='vertical', command=self.chatMessageCanvas.yview)
        self.chatMessageCanvas.configure(yscrollcommand=self.chatMessageScroll.set)

        self.chatMessageScroll.grid(row=0, column=2, sticky=tk.N+tk.S)
        self.chatMessageCanvas.grid(row=0, column=0, sticky=tk.N+tk.E+tk.S+tk.W, columnspan=2)
        self.chatMessageCanvas.create_window(4, 4, window=self.chatMessageFrame, anchor=tk.NE, tags='self.chatMessageFrame')

        self.chatMessageFrame.bind('<Configure>', self.onFrameConfigure)
        self.populate()

        self.chatMessageEntry = tk.Entry(self.chatView)
        self.chatMessageEntry.grid(row=1, column=0, sticky=tk.W+tk.E)
        self.chatMessageButtonSend = tk.Button(self.chatView, text='Send', command=None)
        self.chatMessageButtonSend.grid(row=1, column=1)

    def addChat(self, chatName):
        self.chatListBox.insert(tk.END, chatName)

    def changeChat(self):
        selected = self.chatListBox.curselection()
        if selected == ():
            return
        chatname = self.chatListBox.get(selected)
        # TODO: Get chat
        self.populate()

    def populate(self):
        '''Put in some fake data'''
        # TODO: get real chat messages to show up
        # TODO: reset frame to show new chat
        random.seed()
        for row in range(random.randint(50, 100)):
            if row % 2 == 0:
                sender = 'You'
            else:
                sender = 'Me'
            tk.Label(self.chatMessageFrame, text=sender).grid(row=row, column=0)
            t = "This is message number %s" % row
            tk.Label(self.chatMessageFrame, text=t).grid(row=row, column=1)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.chatMessageCanvas.configure(scrollregion=self.chatMessageCanvas.bbox("all"))
