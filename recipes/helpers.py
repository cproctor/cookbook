def int_input(prompt, error_message=None):
    selection = input(prompt)
    if selection.isdigit():
        return int(selection)
    else:
        print(error_message or "Please enter a number.")
        int_input(prompt, error_message)

def choose_from_options(options, labels, prompt=None, error_message=None):
    print(prompt or "Choose an option:")
    for i, (option, label) in enumerate(zip(options, labels)):
        print(f"    ({i+1}) {option}")
    selection = int_input("> ")
    if selection > 0 and selection <= len(options):
        return options[selection - 1]
    else:
        print(error_message or f"Please choose a number between 1 and {len(choices)}.")
        choose_from_options(options, labels, prompt, error_message)
