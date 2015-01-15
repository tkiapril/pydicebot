import re
import pathlib

import dice
import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr
import yaml

class DiceBot(irc.bot.SingleServerIRCBot):
    dice_notation = re.compile(
        r'^'
        r'(?:(?:[1-9](?:[0-9]+)?)?d(?:0|[1-9](?:[0-9]+)?)'
        r'|(?:0|[1-9](?:[0-9]+)?))'
        r'(?:(?:[+\-*/]'
        r'(?:(?:[1-9](?:[0-9]+)?)?d(?:0|[1-9](?:[0-9]+)?)'
        r'|(?:0|[1-9](?:[0-9]+)?))'
        r')?)+$'
    )

    def __init__(
        self,
        nickname,
        realname,
        server,
        port=6667,
        password=None
    ):
        irc.bot.SingleServerIRCBot.__init__(
            self,
            [irc.bot.ServerSpec(server, port, password)],
            nickname,
            realname
        )

    def on_welcome(self, c, e):
        print('Connected.')

    def on_pubmsg(self, c, e):
        message = e.arguments[0].strip()
        if self.dice_notation.match(message):
            c.privmsg(e.target, str(dice.roll(message)))


def main():
    with pathlib.Path('config.yaml').open('r') as f:
        config = yaml.load(f)
    password = None
    if 'password' in config:
        password = config['password']

    bot = DiceBot(
        config['nickname'],
        config['realname'],
        config['server'],
        config['port'],
        password
    )
    bot.start()


if __name__ == "__main__":
    main()
