from django.db import models
from django.conf import settings

from backend.utils.enums import AccountTypes
from backend.utils.abm import AbstractBaseModel


# Create your models here.
''''''

# ***************** #
#? ## Accounts  ## ?#
# ***************** #






# ********************************* Account ********************************
#? Account
class Account(AbstractBaseModel):
	'''
	This account model provides the minimum fields and inherits 
	from AbstractBaseModel to audit users actions.
	In a context of a Saas app, we can add other methods 
	to freeze, suspend or terminate an account.
	'''
	name = models.CharField(max_length=100, verbose_name='account_name')
	account_type = models.CharField(
		max_length=1,
		choices=AccountTypes.choices(),
		default=AccountTypes.from_index(1)
	)
	start_date = models.DateTimeField(auto_now_add=True)
	end_date = models.DateTimeField(null=True)
	user = models.OneToOneField(
		settings.AUTH_USER_MODEL, 
		related_name="account", 
		verbose_name="user", 
		on_delete=models.CASCADE
	)
	is_active = models.BooleanField(default=False)





#################################### END ####################################
