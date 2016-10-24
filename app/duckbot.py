import discord
import duckbot_settings
import random
import re

client = discord.Client()
rand = random.SystemRandom()

arg_split_regex = re.compile('\s+')
range_regex = re.compile('\d+-\d+')


def roll(message, *args):
    lower_bound = 1
    upper_bound = 100

    if len(args) >= 2:
        lower_bound = int(args[0])
        upper_bound = int(args[1])
    elif len(args) == 1:
        if (range_regex.match(args[0])):
            range_split = args[0].split('-')
            lower_bound = int(range_split[0])
            upper_bound = int(range_split[1])
        else:
            upper_bound = int(args[0])

    lower_bound = max(lower_bound, 1)
    upper_bound = max(lower_bound, upper_bound)

    format_string = ('**%%s** rolls (%%d-%%d): **%%0%dd**' %
                     len(str(upper_bound)))
    return format_string % (message.author, lower_bound, upper_bound,
                            rand.randint(lower_bound, upper_bound))

COMMANDS = {
    'roll': roll,
}


@client.event
async def on_ready():
    print('logged in: %s (%s)' % (client.user.name, client.user.id))

    oauth_url = discord.utils.oauth_url(
        duckbot_settings.CLIENT_ID, permissions=discord.Permissions.text())
    print('invite me: %s' % oauth_url)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/'):
        split = arg_split_regex.split(message.content)

        cmd = split[0][1:]
        args = split[1:]

        if cmd in COMMANDS:
            reply = COMMANDS[cmd](message, *args)
            if reply is not None:
                await client.send_message(message.channel, reply)

client.run(duckbot_settings.TOKEN)
