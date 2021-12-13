# -*- coding: utf-8 -*-
from flask import jsonify
from flask_jwt_extended import jwt_required

from database.models import SmarterInfo
from common.views import ModelView


class SmarterInfoApi(ModelView):
    model = SmarterInfo

    @jwt_required()
    def get(self):
        """
        Get information on SMARTER database
        ---
        tags:
          - Info
        responses:
          200:
            description: SMARTER Database status
        """
        info = self.get_object(pk='smarter')
        return jsonify(info)
