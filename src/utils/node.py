from dataclasses import dataclass
from typing import Any

@dataclass
class Node:
    '''
    A node in a doubly linked list.
    Each node contains a value and pointers to the previous and next nodes.
    '''
    value: Any
    prev: 'Node' = None
    next: 'Node' = None