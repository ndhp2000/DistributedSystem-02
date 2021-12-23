class Notification:
    def __init__(self):
        self._messages_queue_ = []

    def clear(self):
        self._messages_queue_.clear()

    def append(self, log):
        self._messages_queue_.append(log)

    def get_messages(self):
        return tuple(self._messages_queue_)
