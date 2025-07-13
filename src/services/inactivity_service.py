import time
from typing import Optional, Dict, Any, Tuple, List

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

    def update_inactivity(self, group_id: int, current_timestamp: float, user_info: Dict[str, Any]) -> Optional[Tuple[float, Dict[str, Any]]]:
        """
        Processes a new message and updates the inactivity record if necessary.

        :param group_id: The unique identifier for the group.
        :param current_timestamp: The Unix timestamp of the new message.
        :param user_info: Information about the user who sent the message.
        :return: A tuple containing the new record and the previous user's info, or None.
        """
        last_timestamp = self.storage.get_last_message_timestamp(group_id)
        last_user_info = self.storage.get_last_user_info(group_id)

        self.storage.set_last_message_timestamp(group_id, current_timestamp)
        self.storage.set_last_user_info(group_id, user_info)

        if last_timestamp is None or last_user_info is None:
            # This is the first message, so no interval to calculate.
            self.storage.save()
            return None

        interval = current_timestamp - last_timestamp
        current_record = self.storage.get_record(group_id)

        if current_record is None or interval > current_record:
            self.storage.set_record(group_id, interval)
            
            # Update leaderboards
            self.storage.update_leaderboard(group_id, last_user_info['id'], last_user_info['name'], 'last_word')
            self.storage.update_leaderboard(group_id, user_info['id'], user_info['name'], 'silence_breaker')

            # Add to history
            history_entry = {
                "record_seconds": interval,
                "timestamp": time.time(),
                "last_user": last_user_info,
                "breaker_user": user_info
            }
            self.storage.add_to_history(group_id, history_entry)

            self.storage.save()
            return interval, last_user_info

        # Save the updated timestamp and user info even if a record was not broken
        self.storage.save()
        return None

    def get_current_record(self, group_id: int) -> float:
        """
        Retrieves the current inactivity record for a group.

        :param group_id: The unique identifier for the group.
        :return: The current record in seconds. Returns 0.0 if no record exists.
        """
        record = self.storage.get_record(group_id)
        return record if record is not None else 0.0

    def get_leaderboards(self, group_id: int) -> Dict[str, Dict[str, Dict[str, Any]]]:
        """Retrieves the leaderboards for a group."""
        return self.storage.get_leaderboard(group_id)

    def get_history(self, group_id: int) -> List[Dict[str, Any]]:
        """Retrieves the record history for a group."""
        return self.storage.get_history(group_id)

    def seed_record(self, group_id: int, seconds: float) -> None:
        """
        Sets an initial inactivity record for a group.

        :param group_id: The unique identifier for the group.
        :param seconds: The initial record in seconds.
        """
        self.storage.set_record(group_id, seconds)
        self.storage.save()

    def clean_stats(self, group_id: int) -> None:
        """Deletes all stats for a specific group."""
        self.storage.delete_group_data(group_id)
        self.storage.save()