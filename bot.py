import logging
from datetime import date
from bot import BotMain

if __name__ == "__main__":
    logging.basicConfig(
        format="[%(asctime)s] %(name)s/%(levelname)-6s - %(message)s", 
        level=logging.CRITICAL,
        datefmt="%Y-%m-%d %H:%M:%S",
        filename="logs/" + date.today().strftime('%Y-%m-%d_bot.log')
    )
    # Only enable debug level for bbot
    logger = logging.getLogger("bastardbot")
    logger.setLevel(logging.DEBUG)

    print("Initializing BastardBot...")
    bastardbot = BotMain()

    try:
        bastardbot.start()
    except KeyboardInterrupt:
        print("Keyboard interrupt! BastardBot Stopped")
    except Exception as e:
        print("Something wrong happened")
        print(e)

    print("Bot finished")
