import logging, sys

def main():
  logger = logging.getLogger("main")

  stdout_handler = logging.StreamHandler(sys.stdout)
  stdout_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  stdout_handler.setLevel(logging.DEBUG)
  stdout_handler.setFormatter(stdout_formatter)

  logger.addHandler(stdout_handler)

  logger.error("Logger working")


if __name__ == "__main__":
  main()
