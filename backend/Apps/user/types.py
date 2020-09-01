import graphene
from graphene_django import DjangoObjectType

from .models import User, UserRole

from backend.utils.enums import RoleTypes





# ***************************** User Role ****************************
#? User Role
class UserRoleType(DjangoObjectType):
    class Meta:
        model=UserRole
        convert_choices_to_enum = ['RoleTypes']


class UserRoleObjectType(graphene.ObjectType):
    user_role = graphene.Field(UserRoleType)


class UserRoleInputType(graphene.InputObjectType):
    id = graphene.ID()
    designation = graphene.String()
    role_type = graphene.String()



# ****************************** User ********************************

#? User
class UserProductType(DjangoObjectType):
    class Meta:
        model = User
        fields = (
            'id',
            'created_at',
            'username', 
            'password', 
            'email',
            'roles',
            'is_active',
            'is_admin',
            'avatar'
        )

class UserObjectType(graphene.ObjectType):
    user = graphene.Field(UserProductType)


class UserInputType(graphene.InputObjectType):
    id = graphene.ID()
    created_at = graphene.DateTime()
    username = graphene.String()  
    password = graphene.String()
    email = graphene.String()
    roles = graphene.List(UserRoleInputType)


