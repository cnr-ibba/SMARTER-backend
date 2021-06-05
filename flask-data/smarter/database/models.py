#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 21 18:09:30 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

from flask_bcrypt import check_password_hash

from .db import db, DB_ALIAS


class User(db.Document):
    username = db.StringField(required=True, unique=True)
    password = db.StringField(required=True, min_length=6)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    meta = {
        'db_alias': DB_ALIAS,
        'collection': 'user'
    }


class Dataset(db.Document):
    """Describe a dataset instace with fields owned by data types"""

    file = db.StringField(required=True, unique=True)
    uploader = db.StringField()
    size_ = db.StringField(db_field="size")
    partner = db.StringField()

    # HINT: should country, species and breeds be a list of items?
    country = db.StringField()
    species = db.StringField()
    breed = db.StringField()

    n_of_individuals = db.IntField()
    n_of_records = db.IntField()
    trait = db.StringField()
    gene_array = db.StringField()

    # add type tag
    type_ = db.ListField(db.StringField(), db_field="type")

    # file contents
    contents = db.ListField(db.StringField())

    meta = {
        'db_alias': DB_ALIAS,
        'collection': 'dataset'
    }

    def __str__(self):
        return f"file={self.file}, uploader={self.uploader}"


class BreedAlias(db.EmbeddedDocument):
    fid = db.StringField(required=True)
    dataset = db.ReferenceField(
        'Dataset',
        db_field="dataset_id")
    country = db.StringField()

    def __str__(self):
        return f"{self.fid}: {self.dataset}"


class Breed(db.Document):
    species = db.StringField(required=True)
    name = db.StringField(required=True)
    code = db.StringField(required=True)
    aliases = db.ListField(
        db.EmbeddedDocumentField(BreedAlias))
    n_individuals = db.IntField()

    meta = {
        'db_alias': DB_ALIAS,
        'collection': 'breeds',
        'indexes': [
            {
                'fields': [
                    "species",
                    "code"
                ],
                'unique': True,
                'collation': {'locale': 'en', 'strength': 1}
            },
            {
                'fields': [
                    "species",
                    "name"
                ],
                'unique': True,
                'collation': {'locale': 'en', 'strength': 1}
            }
        ]
    }

    def __str__(self):
        return f"{self.name} ({self.code}) {self.species}"
