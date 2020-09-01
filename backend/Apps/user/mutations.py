
import os
import json 
from django.conf import settings
from django.contrib.auth import authenticate
from django.utils import timezone
from django.db.utils import IntegrityError
#from django.contrib.auth import authenticate
#from backend.middleware.remoteuser import CustomHeaderMiddleware as chm
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.validators import validate_email
from django_currentuser.middleware import get_current_authenticated_user

import graphene
import graphql_jwt
from graphql_jwt.shortcuts import get_token
from graphql import GraphQLError
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations

from .models import UserRole, User
from .types import (
	UserRoleType,
	UserRoleInputType,
	UserProductType,
	UserInputType,
)

from backend.Apps.account.models import Account
from backend.Apps.account.types import AccountType, AccountInputType

from backend.utils.enums import RoleTypes, AccountTypes





# ******************************** Create User Roles ********************************
#? Create User Roles
class CreateUserRoles(graphene.Mutation):
	'''
	Roles are pre-created using richenums and we simply bulk
	upload them here
	'''
	message = graphene.String()
	roles = graphene.List(UserRoleType)

	class Arguments:
		roles = graphene.List(UserRoleInputType)

	@staticmethod
	def mutate(self, info, roles):

		all_roles = []
		roles_ids = [str(r.id) for r in roles]
		for i in range (0, len(roles)):
			role = roles[i]

			all_roles.append(
				UserRole(
					designation=role['designation'],
					role_type=RoleTypes.from_canonical(role['role_type'])
				)
			)

		new_roles = None
		try:
			new_roles=UserRole.objects.bulk_create(all_roles)
			return CreateUserRoles(
				roles=new_roles,
				message=f"New_roles_{str(roles_ids)}_have_been_successfully_created"
			)
		except IntegrityError as ie:
			if "error UNIQUE constraint failed:" in str(ie):
				raise GraphQLError("Roles_already_created!")
			else:
				raise GraphQLError(f"An_error_occured: {str(ie)}")




# ************************************ Create User ************************************
#? Create User
class CreateUser(graphene.Mutation):
	'''
	User is created along with his account and user can assign
	an account type to the account as well
	'''
	message = graphene.String()
	user = graphene.Field(UserProductType)
	account = graphene.Field(AccountType)

	class Arguments:
		user = UserInputType()
		account = AccountInputType()

	@staticmethod
	def mutate(self, info, user, account):

		if 'email' in user:
			print('email', user['email'])
			try:
				validate_email(user['email'])
			except ValidationError:
				raise GraphQLError("email_format_is_not_correct!")

		new_user = User(
			username=user['username'],
			email=user['email']
		)
		print('user', user)
		new_user.set_password(user['password'])
		new_user.save()

		if 'roles' in user:
			new_user.add_roles(user['roles'])
			new_user.save()

		try:
			new_account, is_new = Account.objects.get_or_create(
				name=account['name'],
				account_type=AccountTypes.from_canonical(account['account_type']),
				start_date=account['start_date'],
				end_date=account['end_date'],
				user=new_user,
				is_active=account['is_active']
			)
			print('new account', new_account)
		except IntegrityError as ie:
			raise GraphQLError(f"An_error_occured: {str(ie)}")

		username=new_user.username
		message=f"New_user_{username}_has_been_successfully_created"


		return CreateUser(
			user=new_user, 
			account=new_account, 
			message=message
		)





# ************************************* Login User ************************************
#? Login User
class LoginUser(graphene.Mutation):
	'''
	User is logged in using its username ...
	this can be improve by allowing both username and 
	emails for logging in.
	'''
	token = graphene.String()
	message = graphene.String()
	user = graphene.Field(UserProductType)

	class Arguments:
		'''
		This mutation provides a basic login.
		It can be extended by:
		- adding login attempts limit
		  and counting the attempts and registering these
		- adding notification when account is locked to the 
		exeeded number of login attempts
		- etc...
		'''
		user = UserInputType()

	@staticmethod
	def mutate(root, info, user):

		user = authenticate(
			username=user['username'],
			password=user['password'],
		)

		print('user', user, info.context.user)

		if not user:
			raise Exception('Invalid username or password!')

		info.context.session['token'] = get_token(user)

		info.context.session.save()

		return LoginUser(
			user=user,
			token=get_token(user),
			message=f"Welcome_{user.username}_you_have_been_successfully_logged_in"
		)



class Mutation(graphene.ObjectType):
	# #? token
	token_auth = graphql_jwt.ObtainJSONWebToken.Field()
	verify_token = graphql_jwt.Verify.Field()
	refresh_token = graphql_jwt.Refresh.Field()
	revoke_token = graphql_jwt.Revoke.Field()


	#? User Roles
	create_user_roles = CreateUserRoles.Field()


	#? User
	create_user = CreateUser.Field()
	login_user = LoginUser.Field()
