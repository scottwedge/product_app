

import os
import graphene
import graphql_jwt

from itertools import islice
from django.conf import settings
from django.utils import timezone
from django.db.utils import IntegrityError
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from .models import Product
from .types import ProductType, ProductInputType

from backend.utils.enums import QTYUpdateOptions


class RegisterProduct(graphene.Mutation):
	'''
	This mutation creates a Product based on the minimum 
	fields required.
	'''
	message = graphene.String()
	product = graphene.Field(ProductType)

	class Arguments:
		product = ProductInputType()

	@staticmethod
	def mutate(self, info, product):

		try:
			new_product = Product.objects.create(
				sku=product.sku,
				name=product.name,
				quantity=product.quantity,
				price=product.price
			)
		except IntegrityError as ie:
			raise GraphQLError(f"An_error_occured: {str(ie)}")

		return RegisterProduct(
			product=new_product,
			message='New_product_' + product.name + '_has_been_successfully_created'
		)



class UpdateProduct(graphene.Mutation):
	'''
	This mutation updates a Product details by selecting 
	the product by its id and allow users to also update 
	the quantity at the same time based on the requirements.
	'''
	message = graphene.String()
	product = graphene.Field(ProductType)

	class Arguments:
		increment_method = graphene.Argument(
			graphene.Enum.from_enum(QTYUpdateOptions)
		)
		product = ProductInputType()

	@staticmethod
	def mutate(self, info, increment_method, product):

		if 'id' in product:
			product['id'] = product['id']

		try:
			existing_product = Product.objects.get(id=product['id'])
			if 'sku' in product:
				existing_product.sku=product['sku']

			if 'name' in product:
				existing_product.name=product['name']

			if increment_method:
				existing_product.update_quantity(increment_method)

			if 'price' in product:
				existing_product.price=product['price']
			existing_product.save()
		except Product.DoesNotExist as ie:
			raise GraphQLError(f"An_error_occured: {str(ie)}")


		return UpdateProduct(
			product=existing_product,
			message='Product_' + existing_product.name + '_has_been_successfully_updated'
		)



class DeleteProduct(graphene.Mutation):
	'''
	This mutation deletes a Product based on the id
	provided. This can also be improved by allowing 
	the product to be deleted by its sku as well.
	'''
	message = graphene.String()
	product = graphene.Field(ProductType)

	class Arguments:
		product_id = graphene.String()

	@staticmethod
	def mutate(self, info, product_id):

		try:
			all_products = Product.objects.all()
			existing_product = Product.objects.get(pk=product_id)
			product_name = existing_product.name
			existing_product.delete()
		except Product.DoesNotExist as ie:
			if 'does not exist' in str(ie):
				raise GraphQLError("Product does not exist!")
			else:
				raise GraphQLError(f"An_error_occured:_{str(ie)}")

		return DeleteProduct(
			#product=existing_product,
			message='Product_' + product_name + '_has_been_successfully_deleted'
		)




class Mutation(graphene.ObjectType):
	#? Product
	register_product = RegisterProduct.Field()
	update_product = UpdateProduct.Field()
	delete_product = DeleteProduct.Field()

