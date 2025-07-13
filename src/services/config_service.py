from src.storage.storage_interface import StorageInterface

class ConfigService:
    """
    Manages configuration settings for each group.

    This service provides a clean API for accessing and modifying group-specific
    settings, abstracting the underlying storage mechanism.
    """

    def __init__(self, storage: StorageInterface):
        """
        Initializes the ConfigService with a storage backend.

        :param storage: An object that conforms to the StorageInterface.
        """
        self.storage = storage

    def is_announcement_enabled(self, group_id: int) -> bool:
        """
        Checks if new record announcements are enabled for a specific group.

        :param group_id: The unique identifier for the group.
        :return: True if announcements are enabled, False otherwise.
        """
        config = self.storage.get_group_config(group_id)
        return config.get("announce_records", True)  # Default to True

    def toggle_announcements(self, group_id: int) -> bool:
        """
        Toggles the announcement setting for a specific group and returns the new state.

        :param group_id: The unique identifier for the group.
        :return: The new state of the announcement setting (True for enabled, False for disabled).
        """
        config = self.storage.get_group_config(group_id)
        new_state = not config.get("announce_records", True)
        config["announce_records"] = new_state
        self.storage.set_group_config(group_id, config)
        return new_state