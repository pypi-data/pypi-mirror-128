import datetime
from elementalcms.persistence.repositories import PagesRepository
from elementalcms.services import UseCaseResult, Success
from elementalcms.core import MongoDbContext


class UpdateOne:
    __db_context: MongoDbContext

    def __init__(self, db_context: MongoDbContext):
        self.__db_context = db_context

    def execute(self, _id, page) -> UseCaseResult:
        repo = PagesRepository(self.__db_context)
        if '_id' in page:
            del page['_id']
        page['lastModifiedAt'] = datetime.datetime.utcnow()
        success = repo.update(_id, page, True)
        return Success(success)
