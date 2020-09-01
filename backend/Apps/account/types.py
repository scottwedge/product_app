from backend.Apps.user.types import UserInputType
from backend.utils.enums import AccountTypes
from .models import Account
import graphene
from graphene_django import DjangoObjectType





# ****************************** Account *******************************
# Account Types
class AccountType(DjangoObjectType):
    class Meta:
        model = Account
        convert_choices_to_enum = ['AccountTypes']


class AccountObjectType(graphene.ObjectType):
    account = graphene.Field(AccountType)


class AccountInputType(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    account_type = graphene.String()
    start_date = graphene.DateTime()
    end_date = graphene.DateTime(null=True)
    is_active = graphene.Boolean()
