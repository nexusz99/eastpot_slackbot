import eastbot
import eastbot.plugins.miner as miner
# https://github.com/lins05/slackbot


def main():
    eastbot.sched.start()
    eastbot.bot.run()

    if not miner.is_running():
        miner.start_mining()

if __name__ == "__main__":
    main()
