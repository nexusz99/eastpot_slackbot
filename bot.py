import eastbot
# https://github.com/lins05/slackbot


def main():
    eastbot.sched.start()
    eastbot.bot.run()


if __name__ == "__main__":
    main()
