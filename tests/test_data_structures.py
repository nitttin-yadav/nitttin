"""Comprehensive tests for the data_structures module."""

import pytest

from nitttin.data_structures import Stack, Queue, LinkedList


class TestStack:
    def test_new_stack_is_empty(self):
        s = Stack()
        assert s.is_empty() is True
        assert s.size() == 0

    def test_push_increases_size(self):
        s = Stack()
        s.push(1)
        assert s.size() == 1
        assert s.is_empty() is False

    def test_push_multiple(self):
        s = Stack()
        s.push("a")
        s.push("b")
        s.push("c")
        assert s.size() == 3

    def test_pop_returns_last_pushed(self):
        s = Stack()
        s.push(10)
        s.push(20)
        assert s.pop() == 20
        assert s.pop() == 10

    def test_pop_decreases_size(self):
        s = Stack()
        s.push(1)
        s.push(2)
        s.pop()
        assert s.size() == 1

    def test_pop_empty_raises(self):
        s = Stack()
        with pytest.raises(IndexError, match="Pop from empty stack"):
            s.pop()

    def test_peek_returns_top_without_removing(self):
        s = Stack()
        s.push(42)
        assert s.peek() == 42
        assert s.size() == 1

    def test_peek_empty_raises(self):
        s = Stack()
        with pytest.raises(IndexError, match="Peek at empty stack"):
            s.peek()


class TestQueue:
    def test_new_queue_is_empty(self):
        q = Queue()
        assert q.is_empty() is True
        assert q.size() == 0

    def test_enqueue_increases_size(self):
        q = Queue()
        q.enqueue("x")
        assert q.size() == 1
        assert q.is_empty() is False

    def test_dequeue_returns_first_enqueued(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        q.enqueue(3)
        assert q.dequeue() == 1
        assert q.dequeue() == 2

    def test_dequeue_decreases_size(self):
        q = Queue()
        q.enqueue("a")
        q.enqueue("b")
        q.dequeue()
        assert q.size() == 1

    def test_dequeue_empty_raises(self):
        q = Queue()
        with pytest.raises(IndexError, match="Dequeue from empty queue"):
            q.dequeue()

    def test_front_returns_first_without_removing(self):
        q = Queue()
        q.enqueue(99)
        q.enqueue(100)
        assert q.front() == 99
        assert q.size() == 2

    def test_front_empty_raises(self):
        q = Queue()
        with pytest.raises(IndexError, match="Front of empty queue"):
            q.front()


class TestLinkedList:
    def test_new_list_is_empty(self):
        ll = LinkedList()
        assert ll.is_empty() is True
        assert ll.size() == 0
        assert ll.to_list() == []

    def test_append(self):
        ll = LinkedList()
        ll.append(1)
        ll.append(2)
        ll.append(3)
        assert ll.to_list() == [1, 2, 3]
        assert ll.size() == 3

    def test_prepend(self):
        ll = LinkedList()
        ll.prepend(1)
        ll.prepend(2)
        ll.prepend(3)
        assert ll.to_list() == [3, 2, 1]
        assert ll.size() == 3

    def test_find_existing(self):
        ll = LinkedList()
        ll.append("a")
        ll.append("b")
        assert ll.find("a") is True
        assert ll.find("b") is True

    def test_find_missing(self):
        ll = LinkedList()
        ll.append(1)
        assert ll.find(99) is False

    def test_find_empty_list(self):
        ll = LinkedList()
        assert ll.find(1) is False

    def test_delete_head(self):
        ll = LinkedList()
        ll.append(1)
        ll.append(2)
        assert ll.delete(1) is True
        assert ll.to_list() == [2]
        assert ll.size() == 1

    def test_delete_middle(self):
        ll = LinkedList()
        ll.append(1)
        ll.append(2)
        ll.append(3)
        assert ll.delete(2) is True
        assert ll.to_list() == [1, 3]

    def test_delete_tail(self):
        ll = LinkedList()
        ll.append(1)
        ll.append(2)
        ll.append(3)
        assert ll.delete(3) is True
        assert ll.to_list() == [1, 2]

    def test_delete_missing(self):
        ll = LinkedList()
        ll.append(1)
        assert ll.delete(99) is False
        assert ll.size() == 1

    def test_delete_from_empty(self):
        ll = LinkedList()
        assert ll.delete(1) is False
