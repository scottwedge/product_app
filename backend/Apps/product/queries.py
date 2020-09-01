import graphene
from django.db.models import F, Q
from django.utils.timezone import get_current_timezone
from django.db.models.functions import TruncDate
from django.contrib.auth.backends import RemoteUserBackend
from django.views.decorators.cache import cache_page

from dateutil.relativedelta import relativedelta
from datetime import datetime

from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from graphql_auth.schema import UserQuery, MeQuery

from .models import Product
from .types import ProductType

import os


class Query(UserQuery, MeQuery, graphene.ObjectType):
    products = graphene.List(
        ProductType
    )
    product = graphene.List(
        ProductType,
        sku=graphene.String()
    )
    total_products = graphene.Int(
        offset=graphene.Int(),
        limit=graphene.Int(),
        start_date=graphene.String(),
        end_date=graphene.String(),
    )
    available_products = graphene.Int(
        offset=graphene.Int(),
        limit=graphene.Int(),
        ascending=graphene.Boolean(),
        start_date=graphene.String(),
        end_date=graphene.String(),
    )
    sold_out_products = graphene.Int(
        offset=graphene.Int(),
        limit=graphene.Int(),
        ascending=graphene.Boolean(),
        start_date=graphene.String(),
        end_date=graphene.String(),
    )

    @login_required
    def resolve_products(self, info):
        '''
        get all products.
        '''
        return Product.objects.all()

    @login_required
    #@cache_page(60 * 60)
    def resolve_product(self, info, sku=None):
        '''
        get a product based on its Sku.
        '''
        # USER_AGENT = os.environ.get('HTTP_USER_AGENT', None)
        # print('user agent', USER_AGENT)
        return Product.objects.filter(sku=sku)

    @login_required
    def resolve_available_products(
        self, 
        info,
        offset=None,
        limit=None,
        ascending=True,
        start_date=None,
        end_date=None
    ):
        '''
        Returns all available products (>0 Qty). 
        A Few options have been added for filtering as well.
        '''
        tz = get_current_timezone()
        qs = Product.objects.filter(quantity__gt=0)

        if start_date and end_date:
            if start_date == end_date:
                sd = tz.localize(datetime.strptime(start_date, '%d-%m-%Y'))
                delta = relativedelta(minutes=-1, days=+1)
                ed = sd + delta

                qs = qs.filter(created_at__gte=sd)
                qs = qs.annotate(created_to=TruncDate('created_at')).filter(created_to__lte=ed)

        if start_date:
            dt = tz.localize(datetime.strptime(start_date, '%d-%m-%Y'))
            qs = qs.filter(created_at__gte=dt)

        if end_date:
            dt = tz.localize(datetime.strptime(end_date, '%d-%m-%Y'))
            qs = qs.annotate(created=TruncDate('created_at')).filter(created__lte=dt)

        if offset:
            qs = qs[offset - 1::]

        if limit:
            qs = qs[:limit]

        if not ascending:
            qs = reversed(qs)

        available = len(qs)

        return available


    @login_required
    def resolve_sold_out_products(
        self, 
        info,
        offset=None,
        limit=None,
        ascending=True,
        start_date=None,
        end_date=None
    ):
        '''
        Returns all sold out products (0 Qty).
        A Few options have been added for filtering as well.
        '''

        tz = get_current_timezone()
        qs = Product.objects.filter(quantity=0)

        if start_date and end_date:
            if start_date == end_date:
                sd = tz.localize(datetime.strptime(start_date, '%d-%m-%Y'))
                delta = relativedelta(minutes=-1, days=+1)
                ed = sd + delta

                qs = qs.filter(created_at__gte=sd)
                qs = qs.annotate(created_to=TruncDate('created_at')).filter(created_to__lte=ed)

        if start_date:
            dt = tz.localize(datetime.strptime(start_date, '%d-%m-%Y'))
            qs = qs.filter(created_at__gte=dt)

        if end_date:
            dt = tz.localize(datetime.strptime(end_date, '%d-%m-%Y'))
            qs = qs.annotate(created=TruncDate('created_at')).filter(created__lte=dt)

        if offset:
            qs = qs[offset - 1::]

        if limit:
            qs = qs[:limit]

        if not ascending:
            qs = reversed(qs)

        sold_out = len(qs)

        return sold_out
