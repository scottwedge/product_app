#from backend.Apps.user.types import UserInputType
from .models import Product
import graphene
from graphene_django import DjangoObjectType





# ****************************** Product *******************************
#? Product Types
class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = (
            'id',
            'sku',
            'name',
            'quantity',
            'price'
        )


class ProductObjectType(graphene.ObjectType):
    account = graphene.Field(ProductType)


class ProductInputType(graphene.InputObjectType):
    id = graphene.ID()
    sku = graphene.String()
    name = graphene.String()
    quantity = graphene.Float()
    price = graphene.Float()