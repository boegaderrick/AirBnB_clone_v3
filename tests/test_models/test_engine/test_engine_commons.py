#!/usr/bin/python3
"""This module contains shared tests"""
from unittest import TestCase
from models import storage
from models.state import State
import logging


class CommonEngineTests(TestCase):
    """This class defines tests for both storage engines"""
    def test_get_return(self):
        """This method tests the get method of the storage engine"""
        fake = State(name='fake')
        storage.new(fake)
        self.assertIs(type(storage.get(State, fake.id)), type(fake))
        self.assertTrue(storage.get(State, fake.id) is fake)
        self.assertTrue(storage.get(State, fake.id) == fake)
        self.assertIsNone(storage.get(State, 'hello world'))

    def test_count_return(self):
        """This method tests the count method of the storage engines"""
        self.assertIs(type(storage.count()), int)
        self.assertIs(type(storage.count()), type(storage.count(State)))
        count1 = storage.count(State)
        fake = State(name='fake')
        storage.new(fake)
        count2 = storage.count(State)
        self.assertTrue(count2 == count1 + 1)
