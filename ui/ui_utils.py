import colors

from ui_constants import INDENTATION_AMOUNT, JUSTIFY_AMOUNT


def clear_screen():
    """
    Clears the console.
    """
    import os
    os.system("cls")


def ask_input(valid_inputs):
    """
    Displays a choice submition line and validates the choice
    by checking against the provided valid inputs. The submition
    line will be repeated until a valid choice is made.

    :param valid_inputs: List of valid choices the user can make.
    :return: The choice of the user in string format.
    """
    while True:
        choice = raw_input(format_indented(text="> ",
                                           indent_amount=INDENTATION_AMOUNT - 1,
                                           new_line_before=True))
        for arg in valid_inputs:
            if choice == arg:
                return choice


def print_indented(text, indent_amount=INDENTATION_AMOUNT, new_line_before=False):
    """
    Displays the given text with an indentation provided.
    If a new line is required before printing the text,
    set the last parameter to true.

    :param text: The text to be printed.
    :param indent_amount: The indentation amount.
    :param new_line_before: If true, inserts a new line before printing the text.
    """
    if new_line_before:
        print "\n"
    print indent_amount * " ", text


def format_indented(text, indent_amount=INDENTATION_AMOUNT, new_line_before=False):
    """
    Formats the given text with the indentation provided.
    If a new line is required before printing the text,
    set the last parameter to true.

    :param text: The text to be formatted.
    :param indent_amount: The indentation amount.
    :param new_line_before: If true, inserts a new line before printing the text.
    :return: The formatted text, ready to be printed.
    """
    if text is None:
        return None
    elif new_line_before:
        formatted_text = "\n"
    else:
        formatted_text = ""
    formatted_text += (indent_amount * " " + text)
    return formatted_text


def format_justified_left(text, justify_amount=JUSTIFY_AMOUNT):
    """
    Formats the given text so that it will fit in the given amount of characters.
    The text will be formatted to start from left to right.

    :param text: The text to be formatted.
    :param justify_amount: The fixed amount of characters that the text will have to fit into.
    :return: The formatted text, ready to be printed.
    """
    if text is None:
        return None
    return ("{0:<%d}" % justify_amount).format(text)


def print_addon(index, name, version, installed_version):
    """
    Displays a special line made up of a troll-game addon details.
    Helpful for creating addon install menus.

    :param index: The index that will precede the addon name.
    Typically used to determine the user's choice.

    :param name: The name of the addon.

    :param version: The latest version of the addon available.

    :param installed_version: The version of the addon installed on the machine.

    :return: The formatted text, ready to be printed.
    """
    text = "{0}. {1:<30} Version: {2:<10} Installed: {3:>6}" \
        .format(index,
                name,
                version,
                colors.format_success(installed_version)
                if version == installed_version
                else colors.format_error(installed_version))
    print_indented(text)
