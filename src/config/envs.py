from dotenv import load_dotenv
import os

class Envs:

    @staticmethod
    def load():
        load_dotenv()
        openai_api_key = os.getenv("OPENAI_API_KEY")

        if openai_api_key is None or openai_api_key == "":
            print("OPENAI_API_KEY is not set")
            exit(1)

        csv_file_path = os.getenv("CSV_FILE_PATH")

        if csv_file_path is None or csv_file_path == "":
            print("CSV_FILE_PATH is not set")
            exit(1)

    @staticmethod
    def get_csv_file_path():
        return os.getenv("CSV_FILE_PATH")

    @staticmethod
    def get_openai_api_key():
        return os.getenv("OPENAI_API_KEY")
