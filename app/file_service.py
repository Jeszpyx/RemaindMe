import os


class FileService:

    def __init__(self) -> None:
        self._temp_folder = "temp"
        self._temp_folder_path = "temp"

        self._temp_folder_path = os.path.join(os.getcwd(), self._temp_folder)
        if not os.path.exists(self._temp_folder_path):
            os.makedirs(self._temp_folder_path)

    def get_path_to_save(self, file_name: str) -> str:
        return os.path.join(self._temp_folder_path, file_name)


file_service = FileService()
