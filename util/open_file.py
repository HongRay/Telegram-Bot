import os 

class OpenCommandText:
    @staticmethod
    def get_text(file_name: str) -> str:
        # getting file_path from main directory
        main_directory = os.path.dirname(__file__)
        file_path = os.path.join(main_directory, '..', 'data', file_name)
        file_path = os.path.normpath(file_path)
        try:
            with open(file_path, 'r') as file:
                help_text = file.read()
        except FileNotFoundError:
            help_text = "Help text file not found. Please ensure 'command_text.txt' is in the same directory as the bot."
        except IOError as e:
            help_text = f"An error occurred while reading the help text file: {e}"
        
        return help_text
    
    @staticmethod
    def get_token() -> str:
        # getting file_path from main directory
        main_directory = os.path.dirname(__file__)
        file_path = os.path.join(main_directory, '..', 'data', 'token_id.txt')
        file_path = os.path.normpath(file_path)
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            print("Help text file not found. Please ensure 'command_text.txt' is in the same directory as the bot.")
        except IOError as e:
            print(f"An error occurred while reading the help text file: {e}")