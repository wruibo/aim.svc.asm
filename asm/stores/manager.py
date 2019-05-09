"""
    store manager
"""
import threading


class _StoreManager(threading.Thread):
    def __init__(self):
        """
            init store manager
        """
        super().__init__(name='store manager')

    def run(self):
        pass
