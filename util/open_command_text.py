import os 

class OpenCommandText:
    @staticmethod
    def get_text(file_name: str) -> str:
        # Get the directory of the current script (main.py)
        main_directory = os.path.dirname(__file__)
        # Construct the full file path to the data folder one level up
        file_path = os.path.join(main_directory, '..', 'data', file_name)
        # Normalize the path to avoid issues with relative paths
        file_path = os.path.normpath(file_path)
        try:
            # Attempt to read the help text from the file
            with open(file_path, 'r') as file:
                help_text = file.read()
        except FileNotFoundError:
            help_text = "Help text file not found. Please ensure 'command_text.txt' is in the same directory as the bot."
        except IOError as e:
            help_text = f"An error occurred while reading the help text file: {e}"
        
        return help_text
    