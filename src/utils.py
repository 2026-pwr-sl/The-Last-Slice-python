"""Utility helpers for console interactions."""


def choose_from_list(options, title, prompt, cancelled_message, invalid_message):
    """Prompt the user to choose one option from a numbered list.
    
    Returns (option, error_message) tuple. On success, error_message is None.
    """
    try:
        if not isinstance(options, (list, tuple)) or len(options) == 0:
            return None, "Error: Invalid options list provided."
        
        print(f"\n{title}")
        for index, option in enumerate(options, start=1):
            print(f"{index}. {option}")
        
        user_input = input(prompt).strip()
        if not user_input:
            return None, cancelled_message
        
        try:
            choice = int(user_input)
        except ValueError:
            return None, invalid_message
        
        if choice < 1 or choice > len(options):
            return None, invalid_message
        
        return options[choice - 1], None
    
    except KeyboardInterrupt:
        print()  # New line after ^C
        return None, cancelled_message
    except Exception as e:
        return None, f"Error: Unexpected error in selection. {str(e)}"
