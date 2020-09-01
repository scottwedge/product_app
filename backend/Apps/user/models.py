import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

from graphql_jwt.settings import jwt_settings
from datetime import datetime, timedelta
from .manager import CustomUserManager

from backend.utils.enums import RoleTypes
from backend.utils.abm import AbstractBaseModel


# Create your models here.
'''user, authentication, profiles and roles'''





# ******************************** Roles *******************************
#? UserRole
class UserRole(models.Model):
    '''
    This User model provides the minimum fields and inherits 
    from AbstractBaseModel to audit users actions.
    In a context of a Saas app, we can add other methods 
    to freeze, suspend or terminate an account.
    '''
    designation = models.CharField(max_length=50)
    role_type = models.CharField(
        max_length=50, 
        choices=RoleTypes.choices(), 
        default=RoleTypes.from_index(1)
    )

    def create_role(self, name, role_type) -> 'UserRole':
        '''
        Creates a role based on the pre-defined roles enums
        '''
        return UserRole.objects.create(
            name=name,
            role_type=RoleTypes.from_canonical(role_type)
        )




# ******************************** User *********************************
#? User
class User(AbstractUser, AbstractBaseModel):
    '''
    This User model provides the minimum fields and inherits 
    from the AbstractUser class and the AbstractBaseModel to 
    audit users actions.
    The username is the default identifer used for authentication.
    a few methods have been added even the creation of a JWT token.
    '''
    username=models.CharField(max_length=50, unique=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    roles = models.ManyToManyField('UserRole')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    avatar = models.TextField(max_length=500, blank=True, null=True)

    objects = CustomUserManager()


    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @property
    def short_name(self):
        """
        Typically, this would be the user's username.
        """
        return self.username

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().

        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()


    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=60)

        token = jwt_settings.JWT_ENCODE_HANDLER({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

    def add_roles(self, roles=[]):
        '''
        This works for adding just one
        or several roles at the same time.
        '''
        for role in roles:
            if role not in self.roles.all():
                role = UserRole.objects.get(id=role.id)
                self.roles.add(role)
        self.save()
        print('roles', self.roles)
        #return self.roles

    def remove_role(self, role):
        '''
        Remove a user's role if exists.
        '''
        if role in self.roles:
            self.roles.remove(role)
        self.save()
        return True

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def __str__(self):
        return self.username





# # ***************************** User Profile ****************************
# ################################# profiles ##############################

#? UserProfile

class UserProfile(models.Model):
    '''
    This User Profile model can be used to display
    the user profile section on a web page of the app.
    '''    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(null=True)
    location = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.user.username



##################################### END ##################################