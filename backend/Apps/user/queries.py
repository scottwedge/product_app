import graphene
from .types import UserProductType
from .models import User

class Query(graphene.ObjectType):

    user_auth = graphene.Boolean()
    me = graphene.Field(UserProductType)
    users = graphene.List(UserProductType)

    def resolve_users(self, info):
        return User.objects.all()

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        return user