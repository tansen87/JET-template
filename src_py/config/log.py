'''
Author: tansen
Date: 2023-03-18 17:41:48
LastEditors: Please set LastEditors
LastEditTime: 2024-03-16 11:49:41
'''
import logging
from colorama import Fore, Style, init

class Log:
    init(autoreset=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s: %(message)s',
        datefmt="%H:%M:%S"
    )

    @staticmethod
    def info(message: str):
        logging.info(f"{Fore.GREEN}{message}{Style.RESET_ALL}")

    @staticmethod
    def warning(message: str):
        logging.warning(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")

    @staticmethod
    def error(message: str):
        logging.error(f"{Fore.RED}{message}{Style.RESET_ALL}")
