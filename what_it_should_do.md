I need a Telegram bot that tracks and reporting the longest period of inactivity between messages in a group..

Such a bot would:

    Monitor timestamps of all messages in a group.

    Calculate the interval between each message.

    Update and store the record when a new longest interval is detected.

    Optionally, announce the new record in the group.


Like, it saves that the actual record is 10 minutes. If a user then send a message at 10:00 and nobody write a message and then someone send a new message at 10:25 it will store that the new record is 25 minutes and will announce it