from colorama import Fore, init

init = (init())


def format_warning(text):
    if text is None:
        return None
    if not isinstance(text, (basestring, str, unicode)):
        raise ValueError("The object received is not of type basestring, str or unicode.")
    return Fore.YELLOW + text + Fore.RESET


def format_error(text):
    if text is None:
        return None
    if not isinstance(text, (basestring, str, unicode)):
        raise ValueError("The object received is not of type basestring, str or unicode.")
    return Fore.LIGHTRED_EX + text + Fore.RESET


def format_success(text):
    if text is None:
        return None
    if not isinstance(text, (basestring, str, unicode)):
        raise ValueError("The object received is not of type basestring, str or unicode.")
    return Fore.LIGHTGREEN_EX + text + Fore.RESET
