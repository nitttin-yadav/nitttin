"""Custom data structure implementations."""

from typing import Any


class Stack:
    """A simple stack implementation using a list."""

    def __init__(self) -> None:
        self._items: list[Any] = []

    def push(self, item: Any) -> None:
        """Push an item onto the stack."""
        self._items.append(item)

    def pop(self) -> Any:
        """Remove and return the top item.

        Raises:
            IndexError: If the stack is empty.
        """
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        return self._items.pop()

    def peek(self) -> Any:
        """Return the top item without removing it.

        Raises:
            IndexError: If the stack is empty.
        """
        if self.is_empty():
            raise IndexError("Peek at empty stack")
        return self._items[-1]

    def is_empty(self) -> bool:
        """Check if the stack is empty."""
        return len(self._items) == 0

    def size(self) -> int:
        """Return the number of items in the stack."""
        return len(self._items)


class Queue:
    """A simple queue implementation using a list."""

    def __init__(self) -> None:
        self._items: list[Any] = []

    def enqueue(self, item: Any) -> None:
        """Add an item to the back of the queue."""
        self._items.append(item)

    def dequeue(self) -> Any:
        """Remove and return the front item.

        Raises:
            IndexError: If the queue is empty.
        """
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        return self._items.pop(0)

    def front(self) -> Any:
        """Return the front item without removing it.

        Raises:
            IndexError: If the queue is empty.
        """
        if self.is_empty():
            raise IndexError("Front of empty queue")
        return self._items[0]

    def is_empty(self) -> bool:
        """Check if the queue is empty."""
        return len(self._items) == 0

    def size(self) -> int:
        """Return the number of items in the queue."""
        return len(self._items)


class LinkedListNode:
    """A node in a singly linked list."""

    def __init__(self, data: Any) -> None:
        self.data = data
        self.next: "LinkedListNode | None" = None


class LinkedList:
    """A singly linked list implementation."""

    def __init__(self) -> None:
        self.head: LinkedListNode | None = None
        self._size = 0

    def append(self, data: Any) -> None:
        """Append an item to the end of the list."""
        new_node = LinkedListNode(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
        self._size += 1

    def prepend(self, data: Any) -> None:
        """Prepend an item to the beginning of the list."""
        new_node = LinkedListNode(data)
        new_node.next = self.head
        self.head = new_node
        self._size += 1

    def delete(self, data: Any) -> bool:
        """Delete the first occurrence of data. Returns True if found."""
        if self.head is None:
            return False
        if self.head.data == data:
            self.head = self.head.next
            self._size -= 1
            return True
        current = self.head
        while current.next is not None:
            if current.next.data == data:
                current.next = current.next.next
                self._size -= 1
                return True
            current = current.next
        return False

    def find(self, data: Any) -> bool:
        """Check if data exists in the list."""
        current = self.head
        while current is not None:
            if current.data == data:
                return True
            current = current.next
        return False

    def to_list(self) -> list[Any]:
        """Convert the linked list to a Python list."""
        result = []
        current = self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result

    def size(self) -> int:
        """Return the number of items in the list."""
        return self._size

    def is_empty(self) -> bool:
        """Check if the list is empty."""
        return self._size == 0
