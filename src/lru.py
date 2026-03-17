from src.utils.doubly_linked_list import DoublyLinkedList


class LRU:
    '''
    The Least Recently Used (LRU) cache implementation.
    The cache has a fixed capacity and evicts the least recently used item when the capacity is exceeded.
    The cache uses a dictionary for O(1) access to values and a doubly linked list to track the order of usage.
    [A:Least Recently Used] <-> [B] <-> [C] ... [X:Most Recently Used]

    When an item is accessed or added, it is moved to the end of the list (most recently used).
    '''
    def __init__(self, capacity=100, prefix=None):
        self.cache = {}
        self.order = DoublyLinkedList()
        self.capacity = capacity
        self.prefix = prefix

    def _make_key(self, key) -> str:
        return f'{self.prefix}:{key}' if self.prefix else key

    def get(self, key):
        key = self._make_key(key)
        if key not in self.cache:
            return None

        node = self.cache[key]
        self.order.move_to_end(node)

        return node.value

    def set(self, key, value):
        key = self._make_key(key)

        if key in self.cache:
            # update the value and move the node to the end of the list (most recently used)
            node = self.cache[key]
            node.value = value
            self.order.move_to_front(node)
        else:
            # if the cache is at capacity, remove the least recently used item (the tail of the list)
            if self.order.length >= self.capacity:
                # Remove the least recently used item from the cache and the list
                lru_node = self.order.tail
                del self.cache[lru_node.value[0]]
                self.order.delete(lru_node)

            # add the new item to the cache and the front of the list (most recently used)
            new_node = self.order.prepend((key, value))
            self.cache[key] = new_node

    def delete(self, key):
        key = self._make_key(key)
        if key in self.cache:
            node = self.cache[key]
            self.order.delete(node)
            del self.cache[key]

    def clear(self):
        self.cache.clear()
        self.order = DoublyLinkedList()






