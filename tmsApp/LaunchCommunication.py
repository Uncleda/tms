#!/usr/bin/env python
#-*-coding:utf-8-*-
from fabfile import *
from Tkinter import *
import datetime
import time
import thread
import threading
import StringIO
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

class ChatRoomUI():
    '''
    Create UI for django communication model
    '''
    hostlist   = list()
    lines      = list()
    threadLock = threading.Lock()
    textmg     = ''
    exitflag   = 0

    def __init__(self,hosts):
        self.root = Tk()
        self.root.title('AdminChatRoom')
        self.hostlist = hosts
        self.var      = ''
        #The elements needed in GUI
        self.text_msglist      = Text(self.root, height=20)
        self.text_msg          = Text(self.root, height=10)
        self.button_sendmsg    = Button(self.root, text='发送', width=20, height=2, command=self.sendmessage,font=('Arial', 10))
        self.button_quit       = Button(self.root, text='退出', width=20, height=2, command=self.close,font=('Arial', 10))
        self.srcl_text_msglist = Scrollbar(self.root, orient="vertical")
        self.srcl_text_msg     = Scrollbar(self.root, orient="vertical") 
        self.srcl_user_lb      = Scrollbar(self.root, orient="vertical") 
        self.user_lb           = Listbox(self.root, height=30, selectmode=BROWSE, listvariable=self.var)
        self.root.bind("TextMessage",lambda evt:self.text_msglist("insert",textmg)) #add for receving text event
      
        for self.var in self.hostlist:
	        self.user_lb.insert(END, self.var)

        self.user_lb['yscrollcommand']      = self.srcl_user_lb.set
        self.srcl_user_lb['command']        = self.user_lb.yview
        self.user_lb.yview(END)

        self.text_msglist['yscrollcommand'] = self.srcl_text_msglist.set
        self.srcl_text_msglist['command']   = self.text_msglist.yview

        self.text_msg['yscrollcommand']     = self.srcl_text_msg.set
        self.srcl_text_msg['command']       = self.text_msg.yview

        #create a green tag for text_msglist
        self.text_msglist.tag_config('green', foreground='#008B00')
        self.text_msglist.grid(row=0,column=0,padx=2, pady=5,sticky= E+W+S+N)
        self.srcl_text_msglist.grid(row=0,column=1,sticky= E+W+S+N)
        self.user_lb.grid(row=0,column=2,rowspan=2,sticky= E+W+S+N)
        self.srcl_user_lb.grid(row=0,column=3,rowspan=2,sticky= E+W+S+N)

        self.text_msg.grid(row=1,column=0,padx=2, pady=5,sticky= E+W+S+N)
        self.srcl_text_msg.grid(row=1,column=1,sticky= E+W+S+N)

        self.button_sendmsg.grid(row=2,column=0,columnspan=2,sticky= N)
        self.button_quit.grid(row=2,column=1,columnspan=2,sticky= N)
        #launch a thread to monitor the status of lines list for adding return message on text_msglist 
        thread.start_new_thread(self.checkTextCache,("checkTextCacheThread",0.3,))

    def checkTextCache(self,threadname,delay):
        '''check the content of the element lines(lb)'''
        while True:
            if self.exitflag:
                thread.exit()
            if len(self.lines):
                self.write_to_messge_text(self.lines[0],'{0}\n'.format(self.lines[1]))
                del self.lines[:]
                self.threadLock.release() #release thread lock
            #else:
            #    print self.lines
            #print threadname,delay
            time.sleep(delay)
                   
    def runPopZenity(self,item):
        output = execute(launch_communication, host=item)
        #acquire thread lock
        self.threadLock.acquire()
        self.ltkey = output.keys()
        self.ltvalue = output.values()
        self.ltkey[0] = time.strftime("{0}:%Y-%m-%d %H:%M:%S{1}", time.localtime()).format(self.ltkey[0],'\n ')
        self.lines = [self.ltkey[0],self.ltvalue[0]]
        print self.lines
        thread.exit()

    def write_to_messge_text(self,userwithtime,content):
        self.text_msglist.insert(END,userwithtime,'green')
        self.text_msglist.insert(END,content)

    def caller(self,content_input,func):
        func(content_input)

    #Even of sending message
    def sendmessage(self):
        '''Add users and the time of message sending'''
        self.msgcontent = '管理员:{0}{1}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),'\n ')
        self.threadLock.acquire()
        self.write_to_messge_text(self.msgcontent,self.text_msg.get('0.0', END))
        self.threadLock.release()
        talk_content = self.text_msg.get('0.0', END)
        self.caller(talk_content,get_talk_content)
        self.text_msg.delete('0.0', END)
        self.text_msglist.yview(END)
        for item in self.hostlist:
            thread.start_new_thread(self.runPopZenity,(item,))

    def close(self):
        self.exitflag = 1
        self.root.destroy()
'''      
def main():
    #main even cycle
    hosts=['192.168.103.182']
    chatroomui=ChatRoomUI(hosts)
    chatroomui.root.mainloop()

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    #from .commons import *
    main()
'''