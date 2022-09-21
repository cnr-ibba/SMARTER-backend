#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 21 18:09:30 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

import logging

from enum import Enum

from flask_bcrypt import check_password_hash

from .db import db, DB_ALIAS

# Get an instance of a logger
logger = logging.getLogger(__name__)


def complement(genotype: str):
    bases = {
        "A": "T",
        "T": "A",
        "C": "G",
        "G": "C",
        "/": "/"
    }

    result = ""

    for base in genotype:
        result += bases[base]

    return result


class SmarterDBException(Exception):
    pass


class User(db.Document):
    username = db.StringField(required=True, unique=True)
    password = db.StringField(required=True, min_length=6)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    meta = {
        'db_alias': DB_ALIAS,
        'collection': 'user'
    }


class SmarterInfo(db.Document):
    """A class to track database status informations"""

    id = db.StringField(primary_key=True)
    version = db.StringField(required=True)
    working_assemblies = db.DictField()
    plink_specie_opt = db.DictField()
    last_updated = db.DateTimeField()

    meta = {
        'db_alias': DB_ALIAS,
        'collection': 'smarterInfo'
    }

    def __str__(self):
        return f"{self.id}: {self.version} (self.last_updated)"


class Country(db.Document):
    """A helper class to deal with countries object. Each record is created
    after data import, when database status is updated"""

    alpha_2 = db.StringField(
        required=True, unique=True, min_length=2, max_length=2)
    alpha_3 = db.StringField(
        required=True, unique=True, min_length=3, max_length=3)
    name = db.StringField(required=True, unique=True)
    numeric = db.IntField(required=True, unique=True)
    official_name = db.StringField()

    species = db.ListField(db.StringField())

    meta = {
        'db_alias': DB_ALIAS,
        'collection': 'countries'
    }

    def __str__(self):
        return f"{self.name} ({self.alpha_2})"


class SupportedChip(db.Document):
    name = db.StringField(required=True, unique=True)
    species = db.StringField(required=True)
    manifacturer = db.StringField()
    n_of_snps = db.IntField(default=0)

    meta = {
        'db_alias': DB_ALIAS,
        'collection': 'supportedChips'
    }

    def __str__(self):
        return f"'{self.name}' ({self.species})"


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

    # track the original chip_name with dataset
    chip_name = db.StringField()

    meta = {
        'db_alias': DB_ALIAS,
        'collection': 'dataset'
    }

    def __str__(self):
        return f"file={self.file}, uploader={self.uploader}"


class SEX(bytes, Enum):
    UNKNOWN = (0, "Unknown")
    MALE = (1, "Male")
    FEMALE = (2, "Female")

    def __new__(cls, value, label):
        obj = bytes.__new__(cls, [value])
        obj._value_ = value
        obj.label = label
        return obj

    def __str__(self):
        return self.label


class Phenotype(db.DynamicEmbeddedDocument):
    """A class to deal with Phenotype. A dynamic document and not a generic
    DictField since that there can be attributes which could be enforced to
    have certain values. All other attributes could be set without any
    assumptions
    """

    purpose = db.StringField()
    chest_girth = db.FloatField()
    height = db.FloatField()
    length = db.FloatField()

    def __str__(self):
        return f"{self.to_json()}"


class SAMPLETYPE(Enum):
    FOREGROUND = 'foreground'
    BACKGROUND = 'background'


class SampleSpecies(db.Document):
    original_id = db.StringField(required=True)
    smarter_id = db.StringField(required=True, unique=True)

    country = db.StringField(required=True)

    # generic species type (required to derive other stuff)
    species_class = None

    breed = db.StringField(required=True)
    breed_code = db.StringField(min_length=2)

    # this will be a original_id alias (a different sample name in original
    # data file)
    alias = db.StringField()

    # required to search a sample relying only on original ID
    dataset = db.ReferenceField(
        Dataset,
        db_field="dataset_id",
        reverse_delete_rule=db.DENY
    )

    # add type tag
    type_ = db.EnumField(SAMPLETYPE, db_field="type", required=True)

    # track the original chip_name with sample
    chip_name = db.StringField()

    # define enum types for sex
    sex = db.EnumField(SEX)

    # GPS location
    # NOTE: X, Y where X is longitude, Y latitude
    locations = db.MultiPointField(
        auto_index=True, default=None)

    # additional (not modelled) metadata
    metadata = db.DictField(default=None)

    # for phenotypes
    phenotype = db.EmbeddedDocumentField(Phenotype, default=None)

    meta = {
        'abstract': True,
        'indexes': [
            [("locations", "2dsphere")]
        ]
    }

    def __str__(self):
        return f"{self.smarter_id} ({self.breed})"


class SampleSheep(SampleSpecies):
    species = db.StringField(required=True, default="Ovis aries")

    # generic species type (required to derive other stuff)
    species_class = "Sheep"

    # try to model relationship between samples
    father_id = db.LazyReferenceField(
        'SampleSheep',
        passthrough=True,
        reverse_delete_rule=db.NULLIFY
    )

    mother_id = db.LazyReferenceField(
        'SampleSheep',
        passthrough=True,
        reverse_delete_rule=db.NULLIFY
    )

    meta = {
        'db_alias': DB_ALIAS,
        'collection': 'sampleSheep'
    }


class SampleGoat(SampleSpecies):
    species = db.StringField(required=True, default="Capra hircus")

    # generic species type (required to derive other stuff)
    species_class = "Goat"

    # try to model relationship between samples
    father_id = db.LazyReferenceField(
        'SampleGoat',
        passthrough=True,
        reverse_delete_rule=db.NULLIFY
    )

    mother_id = db.LazyReferenceField(
        'SampleGoat',
        passthrough=True,
        reverse_delete_rule=db.NULLIFY
    )

    meta = {
        'db_alias': DB_ALIAS,
        'collection': 'sampleGoat'
    }


class Consequence(db.EmbeddedDocument):
    pass


class Location(db.EmbeddedDocument):
    ss_id = db.StringField()
    version = db.StringField(required=True)
    chrom = db.StringField(required=True)
    position = db.IntField(required=True)
    alleles = db.StringField()
    illumina = db.StringField(required=True)
    illumina_forward = db.StringField()
    illumina_strand = db.StringField()
    affymetrix_ab = db.StringField()
    strand = db.StringField()
    imported_from = db.StringField(required=True)

    # this could be the manifactured date or the last updated
    date = db.DateTimeField()

    consequences = db.ListField(
        db.EmbeddedDocumentField(Consequence), default=None)

    def __init__(self, *args, **kwargs):
        illumina_top = None

        # remove illumina top from arguments
        if 'illumina_top' in kwargs:
            illumina_top = kwargs.pop('illumina_top')

        # initialize base object
        super(Location, self).__init__(*args, **kwargs)

        # fix illumina top if necessary
        if illumina_top:
            self.illumina_top = illumina_top

    @property
    def illumina_top(self):
        """Return genotype in illumina top format"""

        if self.illumina_strand in ['BOT', 'bottom']:
            return complement(self.illumina)

        elif (not self.illumina_strand or
              self.illumina_strand in ['TOP', 'top']):
            return self.illumina

        else:
            raise SmarterDBException(
                f"{self.illumina_strand} not managed")

    @illumina_top.setter
    def illumina_top(self, genotype: str):
        if (not self.illumina_strand or
                self.illumina_strand in ['TOP', 'top']):
            self.illumina = genotype

        elif self.illumina_strand in ['BOT', 'bottom']:
            self.illumina = complement(genotype)

        else:
            raise SmarterDBException(
                f"{self.illumina_strand} not managed")

    def __str__(self):
        return (
            f"({self.imported_from}:{self.version}) "
            f"{self.chrom}:{self.position} [{self.illumina_top}]"
        )


class Probeset(db.EmbeddedDocument):
    chip_name = db.StringField(required=True)

    # more probe could be assigned to the same SNP
    probeset_id = db.ListField(db.StringField())

    def __str__(self):
        return (
            f"{self.chip_name}: {self.probeset_id}"
        )


class VariantSpecies(db.Document):
    rs_id = db.ListField(db.StringField(), default=None)
    chip_name = db.ListField(db.StringField())

    name = db.StringField(unique=True)

    # sequence should model both illumina or affymetrix sequences
    sequence = db.DictField()

    # illumina top variant at variant level
    illumina_top = db.StringField(required=True)

    locations = db.ListField(
        db.EmbeddedDocumentField(Location))

    # HINT: should sender be a Location attribute?
    sender = db.StringField()

    # Affymetryx specific fields
    probesets = db.ListField(
        db.EmbeddedDocumentField(Probeset), default=None)
    affy_snp_id = db.StringField()
    cust_id = db.StringField()

    # abstract class with custom indexes
    # TODO: need a index for position (chrom, position, version)
    meta = {
        'abstract': True,
        'indexes': [
            {
                'fields': [
                    "locations.chrom",
                    "locations.position"
                ],
            },
            {
                'fields': ["affy_snp_id"],
                'partialFilterExpression': {
                    "affy_snp_id": {
                        "$exists": True
                    }
                }
            },
            "probesets.probeset_id",
            'rs_id',
        ]
    }

    def __str__(self):
        if not self.name and self.affy_snp_id:
            return (
                f"affy_snp_id='{self.affy_snp_id}', rs_id='{self.rs_id}', "
                f"illumina_top='{self.illumina_top}'")

        return (
            f"name='{self.name}', rs_id='{self.rs_id}', "
            f"illumina_top='{self.illumina_top}'")

    def to_mongo(self, *args, **kwargs):
        """Override flask-mongoengine method"""

        data = super().to_mongo(*args, **kwargs)

        # add illumina_top property to locations
        for i, location in enumerate(data['locations']):
            data['locations'][i]['illumina_top'] = \
                self.locations[i].illumina_top

        return data


class VariantSheep(VariantSpecies):
    meta = {
        'db_alias': DB_ALIAS,
        'collection': 'variantSheep'
    }


class VariantGoat(VariantSpecies):
    meta = {
        'db_alias': DB_ALIAS,
        'collection': 'variantGoat'
    }
