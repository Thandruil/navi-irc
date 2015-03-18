import navi


class Navi(navi.NaviBot):
    nickname = 'Navi'
    realname = 'Navi IRC Bot'
    server = 'irc.heylisten.net'

    def on_message(self, sender, channel, message, **kwargs):
        if sender == 'Thandruil':
            self.send_packet(message)  # For debugging purposes

    def on_client_join(self, client, channel):
        if client != 'Navi':
            self.send_message(channel, "Welcome, " + client + " to " + channel + "!")

    def __init__(self):
        super(Navi, self).__init__(self.nickname, self.realname, self.server)


if __name__ == '__main__':
    navi = Navi()
    navi.start()
