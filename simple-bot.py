#!/usr/bin/env python3
# -*- coding: utf8 -*-

import irc.client
import irc.bot
import string

irc.client.ServerConnection.buffer_class.encoding = 'utf-8'
irc.client.ServerConnection.buffer_class.errors = 'replace'

nick = "usrename"
chan = "#channelname"
server = "servername"



#------------------------------------------------------------------------------
# Root commands
#------------------------------------------------------------------------------
class KillCommand:
    def execute(self, bot, server, event):
        bot.die("Bye bye ! <3") #commenter paragraphe

class NickCommand:
    def execute(self, bot, server, event):
        server.nick(event.arguments[0].split(" ")[1])

class JoinCommand:
    def execute(self, bot, server, event):
        server.join(event.arguments[0].split(" ")[1])

class PartCommand:
    def execute(self, bot, server, event):
        arguments = event.arguments[0].split(" ");
        server.part(arguments[1] if len(arguments) > 1 else event.target)

class MsgCommand:
    def execute(self, bot, server, event):
        arguments = event.arguments[0].split(" ")
        if irc.client.is_channel(arguments[1]):
            server.privmsg(arguments[1], " ".join(arguments[2:]))
        else:
            server.privmsg(event.target, " ".join(arguments[1:]))

#------------------------------------------------------------------------------
# User commands
#------------------------------------------------------------------------------
class WakeCommand:
    def execute(self, bot, server, event):
        server.privmsg(event.target, " ".join(event.arguments[0].split(' ')[1:]) + ", réveille toi!")

#------------------------------------------------------------------------------
# Bot class
#------------------------------------------------------------------------------
class Bot(irc.bot.SingleServerIRCBot):
    def __init__(self, nick, channel, server, port = 6667):
        self.defaultChannel = channel
        
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nick, "gnidmoo's bot")
        
        self.rootUsers = (
            "gnidmoo"
        )
        
        self.rootCommands = {
            "!kill":   KillCommand(),
            "!nick":   NickCommand(),
            "!join":   JoinCommand(),
            "!part":   PartCommand(),
            "!msg":    MsgCommand()
        }
        
        self.userCommands = {
            "!wake":   WakeCommand()
        }
           
    def on_welcome(self, server, event):
        server.join(self.defaultChannel)
    
    def on_pubmsg(self, server, event):
        message = event.arguments[0] + ' '
        if message[0] == '!':
            command = message.split(' ')[0];
            if command in self.rootCommands and event.source.nick in self.rootUsers:
                self.rootCommands[command].execute(self, server, event)
            elif command in self.userCommands:
                self.userCommands[command].execute(self, server, event)
    
    def on_privmsg(self, server, event):
        self.on_pubmsg(server, event)

if __name__ == "__main__":
#    import sys
    
    Bot(nick, chan, server).start()
