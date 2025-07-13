from typing import Optional

from src.storage.storage_interface import StorageInterface

class InactivityService:
    """
    Handles the core business logic for tracking and calculating inactivity periods.

    This service processes message timestamps to determine if a new inactivity
    record has been set for a group.
    """

    def __init__(self, storage: StorageInterface):
        """
        Initializes the InactivityService with a storage backend.

        :param storage: An object that conforms to the StorageInterface.
        """
        self.storage = storage

    def update_inactivity(self, group_id: int, current_timestamp: float) -> Optional[float]:
        """
        Processes a new message timestamp and updates the inactivity record if necessary.

        :param group_id: The unique identifier for the group.
        :param current_timestamp: The Unix timestamp of the new message.
        :return: The new record in seconds if a new record was set, otherwise None.
        """
        last_timestamp = self.storage.get_last_message_timestamp(group_id)
        self.storage.set_last_message_timestamp(group_id, current_timestamp)

        if last_timestamp is None:
            # This is the first message we've seen in this group, so there's no interval to calculate.
            return None

        interval = current_timestamp - last_timestamp
        current_record = self.storage.get_record(group_id)

        if current_record is None or interval > current_record:
            self.storage.set_record(group_id, interval)
            return interval

        return None

    def get_current_record(self, group_id: int) -> float:
        """
        Retrieves the current inactivity record for a group.

        :param group_id: The unique identifier for the group.
        :return: The current record in seconds. Returns 0.0 if no record exists.
        """
        record = self.storage.get_record(group_id)
        return record if record is not None else 0.0

    def seed_record(self, group_id: int, seconds: float) -> None:
        """
        Sets an initial inactivity record for a group.

        :param group_id: The unique identifier for the group.
        :param seconds: The initial record in seconds.
        """
        self.storage.set_record(group_id, seconds)