import transaction
import navi
import database as db


class Navi(navi.NaviBot):
    nickname = 'Navi'
    realname = 'Navi IRC Bot'
    server = 'irc.heylisten.net'
    db_file = 'lgbteensbot.fs'

    def on_message(self, sender, channel, message, **kwargs):
        if sender == 'TotempaaltJ':
            self.send_packet(message)  # For debugging purposes
            self.join_channel('#programming')
        if message[:5] == '!info':
            self.info(sender, channel, message)
        if message[:4] == '!add':
            self.add(sender, channel, message)

    def info(self, sender, channel, message):
        username = message[6:]
        if username in self.root.users:
            self.send_message(
                channel, "{0}: {1}".format(username,
                                           self.root.users[username].info)
            )
        else:
            self.send_message(channel, "I don't know {0}.".format(username))

    def add(self, sender, channel, message):
        if sender not in self.root.users:
            self.root.users[sender] = db.UserInfo(sender, message[5:])
        else:
            self.root.users[sender].info = message[5:]
        transaction.commit()

        self.send_message(
            channel, "{0}: {1}".format(sender, self.root.users[sender].info)
        )

    def on_client_join(self, client, channel):
        if client != 'Navi':
            self.send_message(
                channel, "Welcome, {0} to {1}!".format(client, channel)
            )

    def __init__(self):
        super(Navi, self).__init__(self.nickname, self.realname, self.server)
        self.database = db.init_db(self.db_file)
        _, self.root = db.open_conn(self.database)


if __name__ == '__main__':
    navi = Navi()
    navi.start()
