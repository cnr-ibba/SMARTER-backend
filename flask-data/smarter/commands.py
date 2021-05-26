#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 26 15:57:49 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>

I wasn't able to create an user using my User (flask-mongoengine) base model,
maybe I should use a model based on mongoengine library. For the moment, I
get a pymongo database using my methods and I add a user using pymongo and
bcrypt
"""

import getpass

import click
from flask import Blueprint
from flask_bcrypt import generate_password_hash

from database.db import db, DB_ALIAS

usersbp = Blueprint('users', __name__)
# https://github.com/pallets/flask/issues/3608#issuecomment-628627335
usersbp.cli.short_help = "Manage users"


@usersbp.cli.command('create')
@click.argument('name')
def create(name):
    """ Creates a user """

    database = db.get_db(alias=DB_ALIAS)
    users = database['user']

    pass1 = getpass.getpass("Please enter a password: ")
    pass2 = getpass.getpass("Please confirm your password: ")

    if pass1 != pass2:
        raise Exception("Password doens't match")

    # generate password hash
    password = generate_password_hash(pass1).decode('utf8')

    # prepare to insert
    user = {
        'username': name,
        'password': password
    }

    user_id = users.insert_one(user).inserted_id

    print(f"User '{name}' added ({user_id})")
