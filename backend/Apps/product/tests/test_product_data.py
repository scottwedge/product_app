import json
import pytest
from pytest import raises

from mixer.backend.django import mixer

import graphene
from graphene.test import Client
from graphene_django import DjangoObjectType
from graphql_jwt.testcases import JSONWebTokenTestCase

from django.contrib.auth import get_user_model

from backend.Apps.product.models import Product
from backend.schema import schema


#* ################################ Testing urls ################################ *#
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode


def url_string(string="/graphql", **url_params):
    if url_params:
        string += "?" + urlencode(url_params)

    return string


def batch_url_string(**url_params):
    return url_string("/graphql/batch", **url_params)


def response_json(response):
    return json.loads(response.content.decode())


def test_graphiql_is_enabled(client):
    response = client.get(url_string(), HTTP_ACCEPT="text/html")
    assert response.status_code == 200
    assert response["Content-Type"].split(";")[0] == "text/html"


def test_query_on_graphiql(client):
    response = client.get(
        url_string(query="{test}"),
        HTTP_ACCEPT="application/json;q=0.8, text/html;q=0.9",
    )
    assert response.status_code == 200
    assert response["Content-Type"].split(";")[0] == "text/html"



#* ######################### Testing Queryies on Types ########################## *#
#? Testing Queryies on Types
def test_should_query_only_fields():
    '''
    The feature "only_fields" is deprecated now in favor of 
    "fields" in Types.py
    '''
    with raises(Exception):

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

        schema = graphene.Schema(query=ProductType)
        query = """
            query Product {
                'id',
                'sku',
                'name',
                'quantity',
                'price'
            }
        """
        result = schema.execute(query)
        assert not result.errors



def test_should_query_properly():
    class ProductType(DjangoObjectType):
        class Meta:
            model = Product

    class Query(graphene.ObjectType):
        product = graphene.Field(ProductType)

        def resolve_product(self, info):
            return Product(sku='BLU-TOWEL-M', name='Blue Towel Medium Size')

    query = """
        query {
            product {
                sku,
                name,
                quantity,
                price
            }
        }
    """
    expected = {
        'product': {
            'sku': 'BLU-TOWEL-M',
            'name': 'Blue Towel Medium Size',
            'quantity': 0,
            'price': 0
        }
    }

    schema = graphene.Schema(query=Query)
    result = schema.execute(query)
    assert not result.errors
    assert result.data == expected



#* ###################### Testing Queryies and Mutations ######################## *#
#? Testing Queryies and Mutations

products_list_query = """
    query{
        products {
            id
            sku
            name
            quantity
            price
        }
    }
"""

single_product_query = """
    query($sku: String!){
        product(sku: $sku) {
            id
            sku
            name
            quantity
            price
        } 
    }
"""

register_product_mutation = """
    mutation RegisterProduct($product: ProductInputType!) {
        registerProduct(product: $product) {
            message
            product {
                id
                sku
                name
                quantity
                price
            }
        }
    }
"""

update_product_mutation = """
    mutation($increment_method: QTYUpdateOptions!, $product: ProductInputType!){
        updateProduct(incrementMethod: $increment_method, product: $product){
            message
            product{
                id
                sku
                name
                quantity
                price
            }
        }
    }
"""

delete_product_mutation = """
    mutation DeleteProduct($product_id: String!) {
        deleteProduct(productId: $product_id) {
            message
            product{
            id
            sku
            name
            quantity
            price
            }
        }
    }
"""


#? JSONWebTokenTestCase inherits from TestCase so we can do normal testing on models
@pytest.mark.django_db
class TestProductSchema(JSONWebTokenTestCase):

    def setUp(self):
        self.product = mixer.blend(Product)
        self.user = get_user_model().objects.create(username='test')
        self.client.authenticate(self.user)

    def test_get_user(self):
        query = '''
        query GetUser($username: String!) {
            user(username: $username) {
                id
            }
        }'''

        variable_values = {
            'username': self.user.username,
        }

        self.client.execute(query, variable_values)

    def test_single_product_query(self):
        response = self.client.execute(single_product_query, {"sku": self.product.sku})
        product = response.data["product"]
        assert product[0]["sku"] == str(self.product.sku)

    def test_products_list_query(self):
        mixer.blend(Product)
        mixer.blend(Product)

        response = self.client.execute(products_list_query)
        products = response.data["products"]
        assert len(products)

    def test_register_product(self):
        self.client = Client(schema)
        prod = mixer.blend(Product)
        product = Product(id=prod.id)
        payload = {
            "name": "Test Product",
            "sku": product.sku,
            "quantity": 20,
            "price": 50
        }
        response = self.client.execute(register_product_mutation, variable_values={"product": payload})
        product = response.get("data").get("registerProduct").get("product")
        name = product.get("name")
        assert name == str(payload["name"])

    def test_update_product(self):
        self.client = Client(schema)
        payload = {
            "increment_method": "MINUS",
            "product":{
                "id": self.product.id,
                "name": "Test Product 2",
                "sku": "YELLOW-TSHIRT-L",
                "quantity": 20,
                "price": 50
            }
        }
        response = self.client.execute(update_product_mutation, variable_values={"increment_method": payload['increment_method'], "product": payload['product']})
        response_product = response.get("data").get("updateProduct").get("product")
        name = response_product.get("name")
        assert name == payload['product']["name"]
        assert name != self.product.name 

    def test_delete_product(self):
        self.client = Client(schema)
        payload = {
            "product_id": str(self.product.id)
        }
        response = self.client.execute(delete_product_mutation, variable_values={"product_id": payload['product_id']})
        message = response.get("data").get("deleteProduct").get("message")
        assert str(message)