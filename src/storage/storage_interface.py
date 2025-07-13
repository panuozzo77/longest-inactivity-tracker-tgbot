from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

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