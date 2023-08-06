from elementalcms.persistence.repositories import DraftsRepository
from elementalcms.services import UseCaseResult, NoResult, Success
from elementalcms.core import MongoDbContext


class GetDraft:
    __db_context: MongoDbContext

    def __init__(self, db_context: MongoDbContext):
        self.__db_context = db_context

    def execute(self, _id) -> UseCaseResult:
        repo = DraftsRepository(self.__db_context)
        page = repo.find_one(_id)
        if page is None:
            return NoResult()
        return Success(page)
