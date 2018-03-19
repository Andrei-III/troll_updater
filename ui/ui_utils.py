import colors

from ui_constants import INDENTATION_AMOUNT, JUSTIFY_AMOUNT


def clear_screen():
    import os
    os.system("cls")


def ask_input(valid_inputs):
    while True:
        choice = raw_input(format_indented(text="> ",
                                           indent_amount=INDENTATION_AMOUNT - 1,
                                           new_line_before=True))
        for arg in valid_inputs:
            if choice == arg:
                return choice


def print_indented(text, indent_amount=INDENTATION_AMOUNT, new_line_before=False):
    if new_line_before:
        print "\n"
    print indent_amount * " ", text


def format_indented(text, indent_amount=INDENTATION_AMOUNT, new_line_before=False):
    if text is None:
        return None
    elif new_line_before:
        formatted_text = "\n"
    else:
        formatted_text = ""
    formatted_text += (indent_amount * " " + text)
    return formatted_text


def format_justified_left(text, justify_amount=JUSTIFY_AMOUNT):
    if text is None:
        return None
    return ("{0:<%d}" % justify_amount).format(text)

def print_addon(index, name, version, installed_version):
    text = "{0}. {1:<30} Version: {2:<10} Installed: {3:>6}" \
        .format(index,
                name,
                version,
                colors.format_success(installed_version)
                if version == installed_version
                else colors.format_error(installed_version))
    print_indented(text)
