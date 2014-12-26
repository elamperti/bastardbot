import logging

#from database import BastardSQL
from bot import BotMain

if __name__ == '__main__':
    logging.basicConfig(
        format="[%(asctime)s] %(name)s/%(levelname)-6s - %(message)s", 
        level=logging.CRITICAL,
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    # Only enable debug level for bbot
    logger = logging.getLogger('bastardbot')
    logger.setLevel(logging.DEBUG)
    # Database instance
    #print("Initializing BastardSQL...")
    #bastardsql = BastardSQL()
    #bastardsql._populate()
  
    print("Initializing the BastardBot...")
    bastardbot = BotMain()

    #print("BastardBot uses BastardSQL")
    #bastardbot.set_database(bastardsql)

    try:
        bastardbot.start()
    except KeyboardInterrupt:
        print("Keyboard interrupt! BastardBot Stopped")
    except Exception as e:
        print("Something wrong happened")
        print(e)

    print("Bot finished")
