from django.db import models
from django.urls import reverse

from backend.utils.abm import AbstractBaseModel 
# Create your models here.


# ***************** #
#? ## Products  ## ?#
# ***************** #



# ********************************* Product ********************************
#? Product
class Product(AbstractBaseModel):
	'''
	This Product model provides the minimum fields required
	and inherits from AbstractBaseModel to audit users actions
	and has 2 methods:
	- create product: creates a product using all fields
	  but the creation of products will be done from the graphql mutation
	  which allows to use only the minimum fields required
	- update quantity: increment or decrement the quantity
	'''
	sku = models.CharField(max_length=13, unique=True)
	barcode = models.CharField(max_length=13, null=True)
	name = models.CharField(max_length=255)
	description = models.TextField(null=True)
	price = models.FloatField(default=0)
	quantity = models.FloatField(default=0)

	def create_product(self, sku, barcode, name, description, price, quantity):
		'''
		creates a product based on all model fields
		'''
		new_product = Product.objects.create(
			sku=sku, 
			barcode=barcode, 
			name=name, 
			description=description, 
			price=price, 
			quantity=quantity
		)
		return new_product

	def update_quantity(self, increment_method):
		'''
		increments or decrement the quantity
		based on the provided increment method
		of the created instance.
		(SKU, +/- Value)
		'''
		if increment_method == 1:
			self.quantity +=1     
		elif increment_method == 2:
			self.quantity -=1
		self.save()
		return self.quantity

	def __str__(self):
		return self.sku
