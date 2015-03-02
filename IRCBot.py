import socket


class IRCBot():
    def __init__(self, nickname, server, port=6667):
        self.server = server
        self.running = True
        self.port = port
        self.nickname = nickname
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

    def connect(self):
        self.socket.connect((self.server, self.port))
        self.send("NICK " + self.nickname)
        self.send("USER " + self.nickname + " " + self.nickname + " " + self.nickname + " :Python Bot")

    def send(self, message):
        self.socket.send((message + "\r\n").encode())

    def join_channel(self, channel):
        self.send("JOIN " + channel)

    def leave_channel(self, channel):
        self.send("PART " + channel)

    def message(self, recipient, message):
        self.send("PRIVMSG " + recipient + " " + message)

    def pong(self, message=""):
        self.send("PONG " + message)

    def quit(self):
        self.send("QUIT")

    def on_message(self, message):
        pass

    def start(self):
        while self.running:
            data = self.socket.recv(4*1024)
            data = data.decode()

            for line in data.split("\r\n"):
                if line != "":
                    print(line)
                    # TODO: implement this