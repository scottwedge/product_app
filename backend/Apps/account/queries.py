import graphene
from django.db.models import F, Q
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from graphql_auth.schema import UserQuery, MeQuery
from .models import Account
from .types import AccountType


class Query(UserQuery, MeQuery, graphene.ObjectType):
    account = graphene.List(
        AccountType
    )
    total_accounts = graphene.Int(
        offset=graphene.Int(),
        limit=graphene.Int(),
        search=graphene.String(),
        start_date=graphene.String(),
        end_date=graphene.String(),
    )

    @login_required
    def resolve_account(self, info, account_id=None):
        return Account.objects.get(pk=account_id)