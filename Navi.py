import IRCBot


class Navi(IRCBot.IRCBot):
    nickname = "Navi"
    server = "irc.heylisten.net"

    def on_message(self, sender, channel, message, **kwargs):
        if sender == "Thandruil":
            self.join_channel('#programming')
        if channel == "Navi":
            self.send_message('#programming', sender + ' said \"' + message + '\"')

    def on_client_join(self, client, channel):
        self.send_message(channel, "Welcome " + client + " to " + channel + "!")

    def __init__(self):
        super(Navi, self).__init__(self.nickname, self.server)


if __name__ == '__main__':
    navi = Navi()
    navi.start()
