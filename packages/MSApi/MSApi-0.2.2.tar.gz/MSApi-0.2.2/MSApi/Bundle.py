from typing import Optional

from MSApi.Assortment import Assortment
from MSApi.ObjectMS import check_init
from MSApi.ProductFolder import ProductFolder
from MSApi.mixin import AttributeMixin, SalePricesMixin, GenerateListMixin, ProductfolderMixin


class Bundle(Assortment,
             AttributeMixin,
             SalePricesMixin,
             GenerateListMixin,
             ProductfolderMixin):

    _type_name = 'bundle'
