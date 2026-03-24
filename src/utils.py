"""Utility helpers for console interactions."""


def choose_from_list(options, title, prompt, cancelled_message, invalid_message):
    """Prompt the user to choose one option from a numbered list.
    
    Args:
        options: List of options to choose from.
        title: Title to display before the list.
        prompt: Prompt text for user input.
        cancelled_message: Message if user cancels.
        invalid_message: Message if invalid choice.
        
    Returns:
        Tuple of (selected_option, error_message). Returns (None, error_msg) on error.
    """
    if not options or not isinstance(options, list):
        return None, "Error: Options list is empty or invalid."
    
    print(f"\n{title}")
    for index, option in enumerate(options, start=1):
        print(f"{index}. {option}")

    try:
        user_input = input(prompt).strip()
        if not user_input:
            return None, cancelled_message
        
        choice = int(user_input)
    except ValueError:
        return None, invalid_message
    except (KeyboardInterrupt, EOFError):
        print()  # New line after Ctrl+C
        return None, cancelled_message
    except Exception as e:
        return None, f"Error: Unexpected error during input. Details: {str(e)}"

    if choice < 1 or choice > len(options):
        return None, invalid_message

    return options[choice - 1], None
