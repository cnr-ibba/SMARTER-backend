#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 27 17:39:44 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

from unittest.mock import patch

from commands import create_user
from database.models import User

from .base import BaseCase


class TestUserCreate(BaseCase):
    @classmethod
    def setUpClass(cls):
        # calling base methods
        super().setUpClass()

        # get a test cli runner, as described at
        # https://flask.palletsprojects.com/en/2.0.x/testing/#testing-cli
        cls.runner = cls.app.test_cli_runner()

    def test_help(self):
        result = self.runner.invoke(create_user, ['--help'])
        self.assertRegex(result.output, r'create .OPTIONS. NAME')

    @patch('getpass.getpass', return_value="password")
    def test_create(self, my_getpass):
        # test command
        result = self.runner.invoke(create_user, ['smarter'])
        self.assertEqual(result.exit_code, 0)

        # test user in db
        qs = User.objects.filter(username="smarter")
        self.assertEqual(qs.count(), 1)

        # test password encryption
        user = qs.get()
        self.assertTrue(user.check_password('password'))
