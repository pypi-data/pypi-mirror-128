
from MSApi.MSLowApi import caching, MSLowApi
from MSApi.Template import Template
from MSApi.ObjectMS import ObjectMS

from MSApi.mixin.GenListMixin import GenerateListMixin
from MSApi.mixin.NameMixin import NameMixin


class Assortment(ObjectMS,
                 GenerateListMixin,
                 NameMixin):
    _type_name = 'assortment'

    @classmethod
    @caching
    def gen_customtemplates(cls, **kwargs):
        return MSLowApi.gen_objects('entity/assortment/metadata/customtemplate', Template, **kwargs)
