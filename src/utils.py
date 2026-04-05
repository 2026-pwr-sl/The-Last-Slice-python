"""Utility helpers for console interactions."""


def choose_from_list(options, title, prompt, cancelled_message, invalid_message):
    """Prompt the user to choose one option from a numbered list."""
    print(f"\n{title}")
    for index, option in enumerate(options, start=1):
        print(f"{index}. {option}")

    try:
        choice = int(input(prompt))
    except (ValueError, KeyboardInterrupt):
        return None, cancelled_message

    if choice < 1 or choice > len(options):
        return None, invalid_message

    return options[choice - 1], None
