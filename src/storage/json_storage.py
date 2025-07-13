import json
import os
from typing import Dict, Any, Optional, List

from src.storage.storage_interface import StorageInterface

class JsonStorage(StorageInterface):
    """
    A concrete implementation of the StorageInterface that uses a JSON file
    for data persistence.

    This class manages reading from and writing to a specified JSON file,
    ensuring that data is stored and retrieved consistently.
    """

    def __init__(self, db_path: str = 'db.json'):
        """
        Initializes the JsonStorage instance.

        :param db_path: The path to the JSON file used for storage.
        """
        self.db_path = db_path
        self.data = self._load_data()

    def _load_data(self) -> Dict[str, Any]:
        """
        Loads data from the JSON file. If the file doesn't exist,
        it returns a default structure.
        """
        if not os.path.exists(self.db_path):
            return {"groups": {}}
        try:
            with open(self.db_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            # If the file is corrupted or unreadable, start with a fresh data structure
            return {"groups": {}}

    def _save_data(self) -> None:
        """Saves the current data to the JSON file."""
        try:
            with open(self.db_path, 'w') as f:
                json.dump(self.data, f, indent=4)
        except IOError as e:
            # In a real application, you would want to handle this more gracefully
            # (e.g., logging, backup mechanism)
            print(f"Error saving data: {e}")

    def _get_group_data(self, group_id: int) -> Dict[str, Any]:
        """
        A helper method to retrieve the data for a specific group,
        initializing it with default values if it doesn't exist.
        """
        group_id_str = str(group_id)
        if group_id_str not in self.data["groups"]:
            self.data["groups"][group_id_str] = {
                "record_seconds": 0.0,
                "last_message_timestamp": None,
                "last_user_info": None,
                "leaderboards": {
                    "last_word": {},
                    "silence_breaker": {}
                },
                "history": [],
                "config": {
                    "announce_records": True
                }
            }
        return self.data["groups"][group_id_str]

    def get_record(self, group_id: int) -> Optional[float]:
        group_data = self._get_group_data(group_id)
        return group_data.get("record_seconds")

    def set_record(self, group_id: int, record_seconds: float) -> None:
        group_data = self._get_group_data(group_id)
        group_data["record_seconds"] = record_seconds
        self._save_data()

    def get_last_message_timestamp(self, group_id: int) -> Optional[float]:
        group_data = self._get_group_data(group_id)
        return group_data.get("last_message_timestamp")

    def set_last_message_timestamp(self, group_id: int, timestamp: float) -> None:
        group_data = self._get_group_data(group_id)
        group_data["last_message_timestamp"] = timestamp
        self._save_data()

    def get_last_user_info(self, group_id: int) -> Optional[Dict[str, Any]]:
        group_data = self._get_group_data(group_id)
        return group_data.get("last_user_info")

    def set_last_user_info(self, group_id: int, user_info: Dict[str, Any]) -> None:
        group_data = self._get_group_data(group_id)
        group_data["last_user_info"] = user_info
        self._save_data()

    def get_group_config(self, group_id: int) -> Dict[str, Any]:
        group_data = self._get_group_data(group_id)
        return group_data.get("config", {"announce_records": True})

    def set_group_config(self, group_id: int, config: Dict[str, Any]) -> None:
        group_data = self._get_group_data(group_id)
        group_data["config"] = config
        self._save_data()

    def get_leaderboard(self, group_id: int) -> Dict[str, Dict[str, Dict[str, Any]]]:
        group_data = self._get_group_data(group_id)
        return group_data.get("leaderboards", {"last_word": {}, "silence_breaker": {}})

    def update_leaderboard(self, group_id: int, user_id: int, user_name: str, board: str) -> None:
        group_data = self._get_group_data(group_id)
        leaderboards = group_data.get("leaderboards", {"last_word": {}, "silence_breaker": {}})
        
        user_id_str = str(user_id)
        if user_id_str not in leaderboards[board]:
            leaderboards[board][user_id_str] = {"name": user_name, "score": 0}
        
        leaderboards[board][user_id_str]["score"] += 1
        # Update name in case it has changed
        leaderboards[board][user_id_str]["name"] = user_name
        
        self._save_data()

    def get_history(self, group_id: int) -> List[Dict[str, Any]]:
        group_data = self._get_group_data(group_id)
        return group_data.get("history", [])

    def add_to_history(self, group_id: int, record_entry: Dict[str, Any]) -> None:
        group_data = self._get_group_data(group_id)
        history = group_data.get("history", [])
        history.append(record_entry)
        self._save_data()