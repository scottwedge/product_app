
from django.utils.deconstruct import deconstructible
from richenum import OrderedRichEnum, OrderedRichEnumValue
from enum import Enum


#? regular enums

class QTYUpdateOptions(Enum):
    '''
    Gives the options to users to add
    or minus quantity
    '''
    ADD = 1  # add quantity
    MINUS = 2  # minus quantity (not an original name :-) but reduce for example is a private keyword ... decrement could be an option...)

    @classmethod
    def choices(cls):
        return [(b, b.value) for b in cls]




#? complex enums


#? Role Types
@deconstructible
class _RoleTypes(OrderedRichEnumValue):
    def __init__(self, index, canonical_name, display_name):
        super(_RoleTypes, self).__init__(index, canonical_name, display_name)

@deconstructible
class RoleTypes(OrderedRichEnum):
    BUDGET_MANAGER = _RoleTypes(1, 'budget manager', 'Budget Manager')
    LINE_MANAGER = _RoleTypes(2, 'line manager', 'Line Manager')
    REGULAR_USER = _RoleTypes(3, 'regular user', 'Regular User')

    @classmethod
    def choices(cls):
        return [(rt, rt.display_name) for rt in cls]




#? Account Types
@deconstructible
class _AccountTypes(OrderedRichEnumValue):
    def __init__(self, index, canonical_name, display_name):
        super(_AccountTypes, self).__init__(index, canonical_name, display_name)

@deconstructible
class AccountTypes(OrderedRichEnum):
    REGULAR = _AccountTypes(1, 'standard', 'Standard')
    MASTER = _AccountTypes(2, 'master', 'Master')
    VIP = _AccountTypes(3, 'vip', 'VIP')

    @classmethod
    def choices(cls):
        return [(ct, ct.display_name) for ct in cls]