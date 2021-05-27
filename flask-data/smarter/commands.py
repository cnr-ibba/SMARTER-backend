#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 26 15:57:49 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

import getpass

import click
from flask import Blueprint
from flask_bcrypt import generate_password_hash

from database.models import User

usersbp = Blueprint('users', __name__)

# https://github.com/pallets/flask/issues/3608#issuecomment-628627335
usersbp.cli.short_help = "Manage users"


@usersbp.cli.command('create')
@click.argument('name')
def create(name):
    """ Creates a user """

    pass1 = getpass.getpass("Please enter a password: ")
    pass2 = getpass.getpass("Please confirm your password: ")

    if pass1 != pass2:
        raise Exception("Password doens't match")

    # generate password hash
    password = generate_password_hash(pass1).decode('utf8')

    # prepare to insert
    user = User(username=name, password=password)
    user.save()

    print(f"User '{name}' added ({user.id})")
