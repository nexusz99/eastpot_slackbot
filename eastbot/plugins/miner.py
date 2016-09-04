import os
import re

from slackbot.bot import respond_to

from eastbot import bot, sched


def is_running():
    cmd = "ps ax | grep 'qtminer' | awk '{print $1}'"
    output = os.popen(cmd).read().count('\n')
    if output == 2 or output > 3:
        stop_mining()
        return False
    elif output == 3:
        return True


@sched.scheduled_job('cron', hour=2, minute=00)
def stop_mining():
    cmd = "kill -9 $(ps ax | grep 'qtminer' | awk '{print $1}')"
    os.system(cmd)
    slack_client = getattr(bot, "_client", None)
    channel_id = slack_client.find_channel_by_name('ethereum')
    slack_client.send_message(channel_id, "[Mining Alert] Mining stopped")


@sched.scheduled_job('cron', hour=9, minute=00)
def start_mining():
    if is_running():
        msg = 'Mining already started'
    else:
        cmd = "sh /home/eastpot/qtminer/qtminer.sh -s asia1.ethermine.org:14444 " \
              "-u 0x71694c8f184b2133dd080c3dcb8e726e00194687.khupot -G " \
              "> /dev/null 2>&1 &"
        os.system(cmd)
        msg = 'Mining started!'

    slack_client = getattr(bot, "_client", None)
    channel_id = slack_client.find_channel_by_name('ethereum')
    slack_client.send_message(channel_id, "[Mining Alert] " + msg)


@respond_to('^start$', re.IGNORECASE)
def bot_start_mining(message):
    start_mining()


@respond_to('^stop$', re.IGNORECASE)
def bot_stop_mining(message):
    stop_mining()
