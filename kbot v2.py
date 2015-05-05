##    Kbot IRC bot
##    Copyright (C) 2015  Karsten Schnier
##
##    This program is free software; you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation; either version 2 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License along
##    with this program; if not, write to the Free Software Foundation, Inc.,
##    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
##
##This General Public License does not permit incorporating your program into
##proprietary programs.  If your program is a subroutine library, you may
##consider it more useful to permit linking proprietary applications with the
##library.  If this is what you want to do, use the GNU Lesser General
##Public License instead of this License.

import sys
import socket
import string
from time import sleep
import settings, commands
import re
import atexit
import cleverbot
import random
from pygoogle import pygoogle
cb = cleverbot.Cleverbot()
HOST="irc.esper.net"
PORT=6667
channel=settings.Main_Channel
NICK=settings.username
IDENT=settings.identity
REALNAME="Kbot Version 2"
readbuffer=""
commands=("say", "sayraw", "nick", "msg", "sendraw BROKEN", "join", "leave")
channels=[channel]
tell=[]
ignore=[]
channelignore=[]

s=socket.socket( )
s.connect((HOST, PORT))
s.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
print("Sent " + "USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
s.send("NICK %s\r\n" % NICK)
print("Sent " + "NICK %s\r\n" % NICK)

while True:
    readbuffer=readbuffer+s.recv(1024)
    temp=string.split(readbuffer, "\n")
    readbuffer=temp.pop( )
    print readbuffer
    for line in temp:
        line=string.rstrip(line)
        line=string.split(line)
        if(line[1]=='433'):
            print "Reconnecting!"
            s.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
            s.send("NICK %s_\r\n" % NICK)
        if(line[0]=='PING'):
            s.send("PONG %s\r\n" % line[1])
            print("Ponged " + line[1])
    if(line[0]=='PING'):
        break
    print line
channel = settings.Main_Channel
s.send("JOIN %s\r\n" % settings.Main_Channel)
if not settings.nickserv_password == "":
    s.send("PRIVMSG NickServ identify %s\r\n" % settings.nickserv_password)
atexit.register(exit)
def exit():
    s.send("EXIT")
def reply( ch, message ):
    s.send("PRIVMSG %s :%s\r\n" % (ch, message))

reply(settings.Main_Channel, "Hello!")
takeinput = ""
while 1:
    if raw_input == "exit":
        s.send("exit")
    readbuffer=readbuffer+s.recv(1024)
    temp=string.split(readbuffer, "\n")
    print readbuffer
    readbuffer=temp.pop( )
    print readbuffer
    for line in temp:
        line=string.rstrip(line)
        line=string.split(line)
        if(line[0]=='PING'):
            s.send("PONG %s\r\n" % line[1])
            print("Ponged " + line[1])
        if len(line) >= 3:    
            channel = line[2]
    if line[0] != ':chaos.esper.net' and line[0] != ":Kountdown!~kountdown@2a00:ab00:10b:46:182:30:120:0" and line[0] != ":SpaceCore!~nodebot@173.193.193.212-static.reverse.softlayer.com" and line[0] != "PING":
        sep = '!'
        user = line[0]
        user = user.split(sep, 1)[0]
        user = user[1:]
        if not user in ignore and not channel in channelignore:
            line = line[3:]
            cmd = ""
            if line:
                print "line exists"
                line[0] = line[0][1:]
            l = " ".join(line)
            if l == ":kbot!~kbot@pool-108-41-42-44.nycmny.fios.verizon.net QUIT :Remote host closed the connection":
                s.send("NICK %s\r\n" % NICK)
            print l
            if l[:1] == '\\':
                p=True
            else:
                p=False
            if l.find(" ") == -1:
                print "no space"
                space=False
                no = len(l)+1
                l = l+" "
            else:
                space=True
                no = l.find(" ")
            if takeinput != "" and user == takeinput:
                print "taking input!"
                takeinput = ""
                if not space:
                    cmd = l
                else:
                    cmd = l[:no+1]
                p=True
            if l[:1] == "\\":
                print "Prefix"
                if space:
                    cmd = l[l.find("\\")+1:no+1]
                else:
                    cmd = l[l.find("\\")+1:]
            if user in tell[0::3]:
                for _ in range(tell[0::3].count(user)):
                    print tell
                    print tell.index(user)
                    print len(tell)
                    print type(tell)
                    print type(tell)
                    reply(channel, user+": Message from " + tell[tell.index(user)+1] + ": " + tell[tell.index(user)+2])
                    tell.remove(tell[tell.index(user)+2])
                    print tell
                    if tell[tell.index(user)+1] in tell:
                        tell.remove(tell[tell.index(user)+1])
                    tell.remove(tell[tell.index(user)])
            args = l[no+1:len(l)]
            cmd = cmd[:-1]
            print cmd
            print args
            if channel[:1] != "#":
                p = True
            print p
            rint = random.randint(1,100)
            print rint
            
            if l[:4] == NICK and l[4:] != " ":
                reply(channel, cb.ask(l[4:]))
            elif l[:4] == NICK and not takeinput == user:
                reply(channel, "Yes?")
                takeinput = user
            if p:
                print "Running a command"
                if cmd=="cmds":
                    reply(channel, user+", I am sending you a list of my commands.")
                    reply(user, "Commands:")
                    reply(user, ", ".join( commands ))
                elif cmd == "sayraw":
                    print "saying raw"
                    reply(channel, args)
                elif cmd == "say":
                    reply(channel, user+': '+args)
                elif cmd == "nick" and user == "Karsten":
                    s.send("NICK %s\r\n" % args)
                elif cmd == "msg":
                    s.send("PRIVMSG %s\r\n" % args)
                    reply(channel, "Sent!")        
                elif cmd == "slap":
                    if args == "me":
                        s.send("\x01ACTION slaps %s\r\n" % user) 
                    elif args == "":
                        s.send("\x01ACTION slaps someone\r\n") 
                    else:
                        s.send("\x01ACTION slaps %s\r\n" % args)
                elif cmd == "sendraw":
                    s.send(args)
                elif cmd == "nocommand":
                    reply(channel, "Make you your mind!")
                elif cmd == "join":
                    s.send("JOIN %s\r\n" % args)
                    reply(channel, "Joined "+args)
                    channels.append(args)
                elif cmd == "leave":
                    s.send("PART %s\r\n" % args)
                    reply(channel, "Left "+args)
                    channels.remove(args)
                elif cmd == "flags" and user == "Karsten":
                    s.send("PRIVMSG ChanServ flags %s\r\n" % args)
                elif cmd == "anc":
                    print channels
                    i=0
                    for _ in range(len(channels)):
                        print channels[i]
                        reply(channels[i], "Anouncement from "+user+": "+args)
                        i=i+1
                elif cmd == "tell":
                    tell.append(args[:args.find(" ")])
                    tell.append(user)
                    tell.append(args[args.find(" "):])
                    print tell
                    reply(channel, "I'll tell them when they come around!")
                elif cmd == "ignore":
                    ignore.append(args)
                elif cmd == "unignore":
                    ignore.remove(args)
                elif cmd == "ignore-channel":
                    channelignore.append(args)
                elif cmd == "unignore-channel":
                    channelignore.remove(args)
                elif cmd == "source" or cmd == "source-please":
                    reply(channel, "My source code can be found at https://github.com/karstenes/kbot")
                #else:
                    #reply(channel, cb.ask(cmd+" "+args))
                    

