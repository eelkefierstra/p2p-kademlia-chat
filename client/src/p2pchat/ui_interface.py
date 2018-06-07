#!/usr/bin/env python3
'''
@author: Eelke
The GUI for the chat application
'''

import tkinter as tk
import random


class UIInterface(tk.Frame):
    def __init__(self, master, application):
        self.application = application
        self.chat_list_labels = []
        self.chat_uuid_list = []

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
        self.chat_list = tk.Frame(self)
        self.chat_list.grid(row=0, column=0)

        self.chat_scroll = tk.Scrollbar(self.chat_list, orient=tk.VERTICAL)
        self.chat_scroll.grid(row=0, column=1, sticky=tk.N+tk.S)
        self.chat_list_box = tk.Listbox(self.chat_list, yscrollcommand=self.chat_scroll.set)
        self.chat_list_box.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        # self.chat_list_box.activate(0)
        self.chat_list_box.bind("<<ListboxSelect>>", self.change_chat)
        # self.change_chat() # Initiate program on first chat
        self.chat_scroll['command'] = self.chat_list_box.yview
        # self.chat_list_button = tk.Button(self.chat_list, text='Select chat', command=self.change_chat)
        # self.chat_list_button.grid(row=1, column=0, columnspan=2, sticky=tk.E+tk.W)

        # Build the chat message view
        self.configure_chatmessage_list()

    def create_menubar(self):
        top = self.winfo_toplevel()
        self.menubar = tk.Menu(top)

        chatmenu = tk.Menu(self.menubar, tearoff=0)
        chatmenu.add_command(label='Create chat', command=self.create_chat_popup)
        chatmenu.add_command(label='Join chat', command=self.join_chat_popup)
        chatmenu.add_command(label='Refresh chats', command=self.refresh_chat_list)

        self.menubar.add_cascade(label='Chats', menu=chatmenu)

        top.config(menu=self.menubar)
        return

    def create_chat_popup(self):
        create_chat_text = 'Enter name for new chat:'
        top_level = tk.Toplevel()
        label = tk.Label(top_level, text=create_chat_text)
        label.grid(row=0, column=0)

        text_entry_new_chat = tk.Entry(top_level)
        text_entry_new_chat.grid(row=1, column=0)

        create_chat_button = tk.Button(top_level, text='Create chat', command=lambda: self.create_chat_popup_action(text_entry_new_chat.get(), top_level))
        create_chat_button.grid(row=2, column=0)

    def join_chat_popup(self):
        join_chat_text = 'Enter the chat uuid'
        top_level = tk.Toplevel()
        label = tk.Label(top_level, text=join_chat_text)
        label.grid(row=0, column=0)

        text_entry = tk.Entry(top_level)
        text_entry.grid(row=1, column=0)

        join_button = tk.Button(top_level, text='Join chat', command=lambda: self.join_chat_popup_action(text_entry.get(), top_level))
        join_button.grid(row=2, column=0)

        text_entry.focus_force()

    def popup_warning(self, title, msg):
        tk.messagebox.showwarning(title, msg)

    def join_chat_popup_action(self, chatuuid, top_level):
        d = self.application.join_chat(chatuuid)
        d.addCallback(lambda x: self.refresh_chat_list())
        top_level.destroy()

    def create_chat_popup_action(self, chatName, toplevel):
        self.application.create_chat(chatName)
        #self.refresh_chat_list()
        toplevel.destroy()

    def configure_chatmessage_list(self):
        self.chat_view = tk.Frame(self)
        self.chat_view.grid(row=0, column=1, sticky=tk.N+tk.E+tk.S+tk.W)

        self.chat_messages_canvas = tk.Canvas(self.chat_view, borderwidth=0, background='#fff')
        self.chat_messages_frame = tk.Frame(self.chat_messages_canvas, background='#fff')
        self.chat_messages_scroll = tk.Scrollbar(self.chat_view, orient='vertical', command=self.chat_messages_canvas.yview)
        self.chat_messages_canvas.configure(yscrollcommand=self.chat_messages_scroll.set)

        self.chat_messages_scroll.grid(row=0, column=2, sticky=tk.N+tk.S)
        self.chat_messages_canvas.grid(row=0, column=0, sticky=tk.N+tk.E+tk.S+tk.W, columnspan=2)
        self.chat_messages_canvas.create_window(4, 4, window=self.chat_messages_frame, anchor=tk.NE, tags='self.chat_messages_frame')

        self.chat_messages_frame.bind('<Configure>', self.on_frame_configure)
        # self.application.get_chat_messages(self.chat_uuid_list[0]).addCallback(self.refresh_chat_messages)

        self.chat_message_entry = tk.Entry(self.chat_view)
        self.chat_message_entry.bind('<Return>', self.send_chat_message)
        self.chat_message_entry.grid(row=1, column=0, sticky=tk.W+tk.E)
        self.chat_message_button_send = tk.Button(self.chat_view, text='Send', command=self.send_chat_message)
        self.chat_message_button_send.grid(row=1, column=1)

    def send_chat_message(self, event = None):
        chat_message = self.chat_message_entry.get()
        d = self.application.send_chat_message(self.current_chatuuid, chat_message)
        d.addCallback(lambda x: self.chat_message_entry.delete(0, len(chat_message)))

    def add_chat(self, chatName, chatuuid):
        self.chat_list_box.insert(tk.END, chatName)
        self.chat_uuid_list.append(chatuuid)

    def change_chat(self, evt):
        print("Changing chat...")
        selected = self.chat_list_box.curselection()
        if selected == ():
            return
        chat_number = selected[0]
        chat_uuid = self.chat_uuid_list[chat_number]
        chat_name = self.chat_list_box.get(chat_number)
        self.current_chatuuid = chat_uuid
        print("Current chat: {}; current chatUUID: {}".format(chat_name, chat_uuid))
        self.refresh_chat_messages()

        self.chat_message_entry.focus_force()

    def refresh_chat_list(self):
        d = self.application.get_chat_list()
        d.addCallback(self._refresh_chat_list)

    def _refresh_chat_list(self, chat_list):
        if chat_list:
            chat_list_box_length = self.chat_list_box.size()
            self.chat_list_box.delete(0, chat_list_box_length-1)
            self.chat_uuid_list = []
            for chat in chat_list:
                self.add_chat(chat[0], chat[1])
            return
        #else:
        #    self.add_chat('*None*', '')
        #    return

    def refresh_chat_messages(self, result = None):
        if (self.current_chatuuid == None):
            return
        d = self.application.get_chat_messages(self.current_chatuuid)
        d.addCallback(self._refresh_chat_messages)
        d.addErrback(print)

    def _refresh_chat_messages(self, chat_messages):
        for label in self.chat_list_labels:
            label.destroy()

        row_count=0
        for result_row in chat_messages:
            message = result_row[0]
            # TODO: Tekst links uit laten lijnen en lange berichten over meerdere regels
            chat_message_label = tk.Label(self.chat_messages_frame, text=message, background='#fff', wraplength=300, justify=tk.LEFT)
            chat_message_label.grid(row=row_count, column=0, sticky=tk.W)
            self.chat_list_labels.append(chat_message_label)
            row_count = row_count + 1

    def on_frame_configure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.chat_messages_canvas.configure(scrollregion=self.chat_messages_canvas.bbox("all"))
