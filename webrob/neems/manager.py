import os
from flask import session
from webrob.neems.neem import NEEM
from webrob.app_and_db import app, get_mongo_db_meta_collection
from webrob.models.NEEMHubSettings import get_settings_count

NEEM_DIR = "/neems"


class NEEM_Manager:
    def __init__(self):
        self.neem_ids = self.set_neem_ids()

    def set_neem_ids(self):
        self.neem_ids = []

        # get all neem ids information from collection
        # first find if there is any existing entry in db
        count = get_settings_count()
        if count > 0:
            mongoDBMetaCollection = get_mongo_db_meta_collection()
            self.neem_ids = mongoDBMetaCollection.find().distinct('_id')

        return self.neem_ids

    def get_requested(self, request):
        neem_id = request.args.get('neem_id',
                                      default=session.get('neem_id', None))
        if neem_id is None:
            return None
        else:
            return self.get(neem_id)

    def get(self, neem_id):
        return NEEM(neem_id)

    def query_neem_ids(self, query_string):
        if query_string is '':
            return self.neem_ids
        else:
            return self.filter_neems(query_string)

    def filter_neems(self, query_string):
        # FIXME: keywords are ignored at the moment
        #   - can an array be added to text index?
        #   - regex search possible, but only without index!!
        #       db.meta.find({"keywords": {"$regex": ".*robot.*","$options": 'i'}},{_id: 1}).pretty()

        mongoDBMetaCollection = get_mongo_db_meta_collection()
        return map(lambda doc: doc["_id"], mongoDBMetaCollection.find(
            {"$text": {"$search": query_string}}, {"_id": 1}))
