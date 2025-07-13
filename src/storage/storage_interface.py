from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List

class StorageInterface(ABC):
    """
    An interface that defines the contract for storage implementations.
    This abstraction allows the core application logic to be decoupled
    from the specific details of the data storage mechanism.
    """

    @abstractmethod
    def get_record(self, group_id: int) -> Optional[float]:
        """
        Retrieves the longest inactivity record (in seconds) for a given group.

        :param group_id: The unique identifier for the group.
        :return: The record in seconds, or None if no record exists.
        """
        pass

    @abstractmethod
    def set_record(self, group_id: int, record_seconds: float) -> None:
        """
        Saves a new longest inactivity record for a given group.

        :param group_id: The unique identifier for the group.
        :param record_seconds: The new record in seconds.
        """
        pass

    @abstractmethod
    def get_last_message_timestamp(self, group_id: int) -> Optional[float]:
        """
        Retrieves the Unix timestamp of the last message recorded in a group.

        :param group_id: The unique identifier for the group.
        :return: The Unix timestamp, or None if no timestamp is stored.
        """
        pass

    @abstractmethod
    def set_last_message_timestamp(self, group_id: int, timestamp: float) -> None:
        """
        Saves the Unix timestamp of the latest message in a group.

        :param group_id: The unique identifier for the group.
        :param timestamp: The Unix timestamp of the message.
        """
        pass

    @abstractmethod
    def get_last_user_info(self, group_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieves the information of the user who sent the last message.

        :param group_id: The unique identifier for the group.
        :return: A dictionary with user info (e.g., id, name), or None.
        """
        pass

    @abstractmethod
    def set_last_user_info(self, group_id: int, user_info: Dict[str, Any]) -> None:
        """
        Saves the information of the user who sent the last message.

        :param group_id: The unique identifier for the group.
        :param user_info: A dictionary containing the user's info.
        """
        pass

    @abstractmethod
    def get_leaderboard(self, group_id: int) -> Dict[str, Dict[str, Dict[str, Any]]]:
        """
        Retrieves the leaderboards for a group.

        :param group_id: The unique identifier for the group.
        :return: A dictionary containing the leaderboards.
        """
        pass

    @abstractmethod
    def update_leaderboard(self, group_id: int, user_id: int, user_name: str, board: str) -> None:
        """
        Updates a user's score on a specific leaderboard.

        :param group_id: The unique identifier for the group.
        :param user_id: The unique identifier for the user.
        :param user_name: The name of the user.
        :param board: The name of the leaderboard to update.
        """
        pass

    @abstractmethod
    def get_history(self, group_id: int) -> List[Dict[str, Any]]:
        """
        Retrieves the record history for a group.

        :param group_id: The unique identifier for the group.
        :return: A list of historical records.
        """
        pass

    @abstractmethod
    def add_to_history(self, group_id: int, record_entry: Dict[str, Any]) -> None:
        """
        Adds a new entry to the record history of a group.

        :param group_id: The unique identifier for the group.
        :param record_entry: The record entry to add.
        """
        pass

    @abstractmethod
    def get_group_config(self, group_id: int) -> Dict[str, Any]:
        """
        Retrieves the configuration settings for a given group.

        :param group_id: The unique identifier for the group.
        :return: A dictionary containing the group's configuration.
        """
        pass

    @abstractmethod
    def set_group_config(self, group_id: int, config: Dict[str, Any]) -> None:
        """
        Saves the configuration settings for a given group.

        :param group_id: The unique identifier for the group.
        :param config: A dictionary containing the group's new configuration.
        """
        pass