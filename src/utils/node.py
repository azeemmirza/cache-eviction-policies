from dataclasses import dataclass

@dataclass
class Node:
    '''
    A node in a doubly linked list.
    Each node contains a value and pointers to the previous and next nodes.
    '''
    value: any
    prev: 'Node' = None
    next: 'Node' = None