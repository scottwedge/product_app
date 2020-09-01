
from django.db import models
from django.db.models import DateTimeField


class AbstractBaseModel(models.Model):
    """AbstractBaseModel contains common fields between models.
    All models should extend this class.
    	Improvements: 
        - this model can be changed to a mixin 
          adding who created, updated or deleted actions were
          performed by.
        - or this can be performed by creating an audit log
        - or or this can be done by implementing Event Sourcing
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True