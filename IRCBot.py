import socket
import re


class IRCBot():
    pattern = re.compile(r'^:(?P<sender>\S+)!(?P<host>\S+)\s(?P<command>\w+)(?:\s(?P<args>.+))?$')

    def __init__(self, nickname, realname, server, port=6667):
        self.server = server
        self.running = True
        self.port = port
        self.nickname = nickname
        self.realname = realname
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

    def connect(self):
        self.socket.connect((self.server, self.port))
        self.send_packet("NICK " + self.nickname)
        self.send_packet("USER " + self.nickname + " " + self.nickname + " " + self.nickname + " :" + self.realname)

    def send_packet(self, message):
        self.socket.send((message + "\r\n").encode())

    def join_channel(self, channel):
        self.send_packet("JOIN " + channel)
        self.on_join(channel)

    def leave_channel(self, channel):
        self.send_packet("PART " + channel)

    def send_message(self, channel, message):
        self.send_packet("PRIVMSG " + channel + " " + message)

    def pong(self, message=""):
        self.send_packet("PONG " + message)

    def quit(self):
        self.send_packet("QUIT")

    def on_message(self, sender, channel, message):
        """Event raised when a message is received

        :param sender:
        :param channel:
        :param message:
        """
        pass

    def on_notice(self, sender, message):
        """Event raised when a notice is received

        :param sender:
        :param message:
        """
        pass

    def on_join(self, channel):
        """Event raised when joining a channel

        :param channel:
        """
        pass

    def on_client_join(self, client, channel):
        """Event raised when a client joins a channel

        :param client:
        :param channel:
        """
        pass

    def on_client_leave(self, client, channel):
        """Event raised when a client leaves a channel

        :param client:
        :param channel:
        :return:
        """
        pass

    def start(self):
        while self.running:
            data = self.socket.recv(4*1024)
            data = data.decode()

            for line in data.split("\r\n"):
                if line != "":
                    print(line)
                    if line.startswith("PING"):
                        self.pong(line.split()[1][1:])
                    else:
                        self.parse_packet(line)

    def parse_packet(self, message):
        match = self.pattern.match(message)
        if match is not None:
            groups = match.groupdict()
            sender = groups['sender']
            if groups['command'] == "PRIVMSG":
                channel, message = groups['args'].split(' ', 1)
                message = message[1:]
                self.on_message(sender, channel, message)
            if groups['command'] == "NOTICE":
                message = groups['args'][1:]
                self.on_notice(sender, message)
            if groups['command'] == "JOIN":
                channel = groups['args'][1:]
                self.on_client_join(sender, channel)
            if groups['command'] == "PART":
                channel = groups['args'][1:]
                self.on_client_leave(sender, channel)
