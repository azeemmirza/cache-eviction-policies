from src.utils.node import Node

class DoublyLinkedList:
    '''
    A doubly linked list implementation in Python.
    Each node contains a value and pointers to the previous and next nodes.
    The list supports appending, prepending, deleting nodes, and finding nodes by value.
    '''
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0


    def append(self, value):
        # Create a new node with the given value
        new_node = Node(value)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.length += 1


    def prepend(self, value):
        # Create a new node with the given value
        new_node = Node(value)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.length += 1


    def delete(self, node):
        # Remove the node from the list and update the pointers of the previous and next nodes
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next

        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev

        self.length -= 1


    def find(self, value):
        # Traverse the list to find the first node with the given value and return it
        current = self.head
        while current:
            if current.value == value:
                return current
            current = current.next
        return None

    def move_to_front(self, node):
        # Move the given node to the front of the list
        if node is self.head:
            return  # Node is already at the front

        self.delete(node)  # Remove the node from its current position
        self.prepend(node.value)  # Add the node to the front of the list


    def move_to_end(self, node):
        # Move the given node to the end of the list
        if node is self.tail:
            return  # Node is already at the end

        self.delete(node)  # Remove the node from its current position
        self.append(node.value)  # Add the node to the end of the list

    def __len__(self):
        return self.length

    def __iter__(self):
        current = self.head
        while current:
            yield current.value
            current = current.next
