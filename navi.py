import socket
import re

# IRC PROTOCOL
WELCOME = "001"
PRIVMSG = "PRIVMSG"
NOTICE = "NOTICE"
CHANNEL_JOIN = "JOIN"
CHANNEL_LEAVE = "PART"


class NaviBot():
    packetpattern = re.compile(
        (r'^'
         '(:(?P<prefix>\S+) )?'
         '(?P<command>\S+)'
         '( (?!:)(?P<params>.+?))?'
         '( :(?P<trail>.+))?'
         '$'))
    userpattern = re.compile(  # nick!ident@host
        (r'^'
         '(?P<nick>\S+)!'
         '(?P<ident>\S+)@'
         '(?P<host>\S+)'
         '$'))

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
        self.send_packet("NICK {0}".format(self.nickname))
        self.send_packet("USER {0} {0} {0} :{1}".format(self.nickname,
                                                        self.realname))

    def send_packet(self, message):
        self.socket.send((message + "\r\n").encode())

    def join_channel(self, channel):
        self.send_packet("JOIN {0}".format(channel))
        self.on_join(channel)

    def leave_channel(self, channel):
        self.send_packet("PART {0}".format(channel))

    def send_message(self, channel, message):
        self.send_packet("PRIVMSG {0} {1}".format(channel, message))

    def pong(self, message=""):
        self.send_packet("PONG {0}".format(message))

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
        packetmatch = self.packetpattern.match(message)
        if packetmatch is not None:
            groups = packetmatch.groupdict()
            prefix = groups['prefix']
            command = groups['command']

            usermatch = self.userpattern.match(prefix)
            if usermatch is not None:
                sender = usermatch.groupdict()['nick']
            else:
                sender = prefix

            if command == WELCOME:
                pass
            elif command == PRIVMSG:
                channel = groups['params']
                message = groups['trail']
                self.on_message(sender, channel, message)
            elif command == NOTICE:
                message = groups['trail']
                self.on_notice(sender, message)
            elif command == CHANNEL_JOIN:
                channel = groups['args'][1:]
                self.on_client_join(sender, channel)
            elif command == CHANNEL_LEAVE:
                channel = groups['args'][1:]
                self.on_client_leave(sender, channel)
            # TODO: handling unknown packets
