

import os
import graphene
import graphql_jwt

from itertools import islice
from django.conf import settings
from django.utils import timezone
from django.db.utils import IntegrityError

from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from .models import Account
from .types import AccountType, AccountInputType



class CreateAccount(graphene.Mutation):
	message = graphene.String()
	account = graphene.Field(AccountType)

	class Arguments:
		message = graphene.String(required=True)
		account = AccountInputType()

	@staticmethod
	def mutate(self, info, account):

		try:
			account, is_new = Account.objects.get_or_create(
				name=account.name,
				start_date=account.start_date,
				end_date=account.end_date
			)
		except IntegrityError as ie:
			raise GraphQLError(f"An_error_occured: {str(ie)}")

		return CreateAccount(account=account, message='New_account_' + account.name + '_has_been_successfully_created')


class UpdateAccount(graphene.Mutation):
	message = graphene.String()
	account = graphene.Field(AccountType)

	class Arguments:
		message = graphene.String(required=True)
		account = graphene.String(required=True)

	@staticmethod
	def mutate(self, info, account):

		try:
			new_account = Account(
				pk=account.id
			)
			new_account.name=account.name,
			new_account.start_date=account.start_date,
			new_account.end_date=account.end_date

		except IntegrityError as ie:
			raise GraphQLError(f"An_error_occured: {str(ie)}")

		return UpdateAccount(account=new_account, message='Account_' + new_account.name + '_has_been_successfully_updated')



class DeleteAccount(graphene.Mutation):
	message = graphene.String()
	account = graphene.Field(AccountType)

	class Arguments:
		message = graphene.String(required=True)
		account = graphene.String(required=True)

	@staticmethod
	def mutate(self, info, account):

		try:
			account = Account.objects.get(
				pk=account.id
			).delete()
		except IntegrityError as ie:
			raise GraphQLError(f"An_error_occured: {str(ie)}")

		return DeleteAccount(account=account, message='Account_' + account.name + '_has_been_successfully_deleted')




class Mutation(graphene.ObjectType):
	#? Account
	create_account = CreateAccount.Field()
	update_account = UpdateAccount.Field()
	delete_account = DeleteAccount.Field()

