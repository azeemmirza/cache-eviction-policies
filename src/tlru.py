from lru import LRU
from src.utils.time import current_time


class TLRU(LRU):
    '''
    Time-aware Least Recently Used (TLRU) cache implementation.
    The cache has a fixed capacity and evicts the least recently used item when the capacity is exceeded.
    Each item in the cache has a time-to-live (TTL) after which it is considered expired and can be evicted.
        The cache uses a dictionary for O(1) access to values and a doubly linked list to track the order of usage.
        [A:Least Recently Used] <-> [B] <-> [C] ... [X:Most Recently Used]

        When an item is accessed or added, it is moved to the end of the list (most recently used).
        Expired items are removed from the cache when accessed or when adding new items.
    '''

    def __init__(self, capacity=100, ttl=60, prefix=None):
        '''
        :param capacity: The maximum number of items the cache can hold.
        :param ttl: The time-to-live (TTL) for each item in seconds. After this time, the item is considered expired and can be evicted.
        :param prefix: An optional prefix to be added to all keys in the cache. This can be useful for namespacing or avoiding key collisions when using multiple caches.
        '''
        super().__init__(capacity, prefix)
        self.ttl = ttl
        self.ttl_map = {}

    def get(self, key):
        '''
        get the value associated with the key from the cache. If the key is not found or if the item has expired, return None.

        :param key: The key to retrieve from the cache.
        :return: The value associated with the key, or None if the key is not found or if the item has expired.
        '''
        key = self._make_key(key)
        if key not in self.cache:
            return None

        # Check if the item has expired
        if key in self.ttl_map and self.ttl_map[key] < current_time():
            self.delete(key)
            return None

        node = self.cache[key]
        self.order.move_to_end(node)

        return node.value[1]

    def set(self, key, value):
        '''
        set the value associated with the key in the cache.

        :param key: The key to set in the cache.
        :param value: The value to associate with the key in the cache.
        :return: None
        '''
        key = self._make_key(key)

        # Remove expired items before adding a new item
        self._remove_expired_items()

        if key in self.cache:
            # update the value and move the node to the end of the list (most recently used)
            node = self.cache[key]
            node.value = (key, value)
            self.order.move_to_front(node)
        else:
            # if the cache is at capacity, remove the least recently used item (the tail of the list)
            if self.order.length >= self.capacity:
                # Remove the least recently used item from the cache and the list
                lru_node = self.order.tail
                del self.cache[lru_node.value[0]]
                del self.ttl_map[lru_node.value[0]]
                self.order.delete(lru_node)

            # add the new item to the cache and the front of the list (most recently used)
            new_node = self.order.prepend((key, value))
            self.cache[key] = new_node
            self.ttl_map[key] = current_time() + self.ttl


    def _remove_expired_items(self):
        # Remove expired items from the cache and the list
        current_time_ = current_time()
        keys_to_remove = [key for key, expiry in self.ttl_map.items() if expiry < current_time_]
        for key in keys_to_remove:
            self.delete(key)

    def delete(self, key):
        '''
        delete the key from the cache if it exists.

        :param key: The key to delete from the cache.
        :return: None
        '''
        key = self._make_key(key)
        if key in self.cache:
            node = self.cache[key]
            self.order.delete(node)
            del self.cache[key]
            if key in self.ttl_map:
                del self.ttl_map[key]

