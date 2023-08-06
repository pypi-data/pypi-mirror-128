import pymongo

from elementalcms.persistence import MongoDbConnectionManager

from elementalcms.core import MongoDbContext


class GlobalDepsRepository(MongoDbConnectionManager):

    coll_name = 'global_deps'

    def __init__(self, db_context: MongoDbContext):
        self.__db = self._get_db(db_context)

    def find(self, query=None, page=None, page_size=None):
        if page is not None and page_size is not None:
            raise Exception('Paging not implemented.')
        result = self.__db.get_collection(self.coll_name).find(query if query is not None else {}).sort([('type', pymongo.ASCENDING),
                                                                                                         ('order', pymongo.ASCENDING)])
        return list(result)
