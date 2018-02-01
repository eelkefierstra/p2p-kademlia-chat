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
    def __init__(self, master, uiInterface):
        self.uiInterface = uiInterface
        self.chatListLabels = []
        
        tk.Frame.__init__(self, master)
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)

        self.grid(sticky=tk.N+tk.E+tk.S+tk.W)
        self.create_widgets()
        self.refresh_chat_list()

    def create_widgets(self):
        # Create Menubar
        self.create_menubar()
        # Build the chat listing
        self.chatList = tk.Frame(self)
        self.chatList.grid(row=0, column=0)

        self.chatScroll = tk.Scrollbar(self.chatList, orient=tk.VERTICAL)
        self.chatScroll.grid(row=0, column=1, sticky=tk.N+tk.S)
        self.chatListBox = tk.Listbox(self.chatList, yscrollcommand=self.chatScroll.set)
        self.chatListBox.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.chatListBox.activate(0)
        self.change_chat() # Initiate program on first chat
        self.chatScroll['command'] = self.chatListBox.yview
        self.chatListButton = tk.Button(self.chatList, text='Select chat', command=self.change_chat)
        self.chatListButton.grid(row=1, column=0, columnspan=2, sticky=tk.E+tk.W)

        # Build the chat message view
        self.configure_chatmessage_list()

    def create_menubar(self):
        top = self.winfo_toplevel()
        self.menubar = tk.Menu(top)

        chatmenu = tk.Menu(self.menubar, tearoff=0)
        chatmenu.add_command(label='Create chat', command=self.create_chat_popup)
        chatmenu.add_command(label='Refresh chats', command=self.refresh_chat_list)

        self.menubar.add_cascade(label='Chats', menu=chatmenu)
        
        top.config(menu=self.menubar)
        return
    
    def create_chat_popup(self):
        createChatText = 'Enter name for new chat:'
        topLevel = tk.Toplevel()
        label = tk.Label(topLevel, text=createChatText)
        label.grid(row=0, column=0)
        
        textEntry = tk.Entry(topLevel)
        textEntry.grid(row=1, column=0)
        
        createButton = tk.Button(topLevel, text='Create chat', command=lambda: self.create_chat_popup_action(textEntry.get(), topLevel))
        createButton.grid(row=2, column=0)
        return
    
    def create_chat_popup_action(self, chatName, toplevel):
        self.uiInterface.create_chat(chatName)
        self.refresh_chat_list()
        toplevel.destroy()
        return

    def configure_chatmessage_list(self):
        self.chatView = tk.Frame(self)
        self.chatView.grid(row=0, column=1, sticky=tk.N+tk.E+tk.S+tk.W)

        self.chatMessageCanvas = tk.Canvas(self.chatView, borderwidth=0, background='#fff')
        self.chatMessageFrame = tk.Frame(self.chatMessageCanvas, background='#fff')
        self.chatMessageScroll = tk.Scrollbar(self.chatView, orient='vertical', command=self.chatMessageCanvas.yview)
        self.chatMessageCanvas.configure(yscrollcommand=self.chatMessageScroll.set)

        self.chatMessageScroll.grid(row=0, column=2, sticky=tk.N+tk.S)
        self.chatMessageCanvas.grid(row=0, column=0, sticky=tk.N+tk.E+tk.S+tk.W, columnspan=2)
        self.chatMessageCanvas.create_window(4, 4, window=self.chatMessageFrame, anchor=tk.NE, tags='self.chatMessageFrame')

        self.chatMessageFrame.bind('<Configure>', self.on_frame_configure)
        self.refresh_chat_messages()

        self.chatMessageEntry = tk.Entry(self.chatView)
        self.chatMessageEntry.grid(row=1, column=0, sticky=tk.W+tk.E)
        self.chatMessageButtonSend = tk.Button(self.chatView, text='Send', command=self.send_chat_message)
        self.chatMessageButtonSend.grid(row=1, column=1)
    
    def send_chat_message(self):
        chatMessage = self.chatMessageEntry.get()
        self.uiInterface.send_chat_message(self.currentChat, chatMessage)
        self.chatMessageEntry.delete(0, len(chatMessage))
        return

    def add_chat(self, chatName):
        self.chatListBox.insert(tk.END, chatName)

    def change_chat(self):
        selected = self.chatListBox.curselection()
        if selected == ():
            return
        self.currentChat = self.chatListBox.get(selected)[0]
        # TODO: Get chat
        self.refresh_chat_messages()
    
    def refresh_chat_list(self):
        self.uiInterface.get_chat_list().addCallback(self._refresh_chat_list)
        
    def _refresh_chat_list(self, chatList):
        if chatList:
            chatListBoxLength = self.chatListBox.size()
            self.chatListBox.delete(0, chatListBoxLength-1)
            for chat in chatList:
                self.add_chat(chat)
            return
        else:
            self.add_chat('*None*')
            return

    def refresh_chat_messages(self):
        '''Put in some fake data'''
        # TODO: get real chat messages to show up
        for label in self.chatListLabels:
            label.destroy()
        random.seed()
        for row in range(random.randint(50, 100)):
            if row % 2 == 0:
                sender = 'You'
            else:
                sender = 'Me'
            chatSenderLabel = tk.Label(self.chatMessageFrame, text=sender)
            chatSenderLabel.grid(row=row, column=0)
            self.chatListLabels.append(chatSenderLabel)
            t = "This is message number %s" % row
            chatMessageLabel = tk.Label(self.chatMessageFrame, text=t)
            chatMessageLabel.grid(row=row, column=1)
            self.chatListLabels.append(chatMessageLabel)

    def on_frame_configure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.chatMessageCanvas.configure(scrollregion=self.chatMessageCanvas.bbox("all"))
