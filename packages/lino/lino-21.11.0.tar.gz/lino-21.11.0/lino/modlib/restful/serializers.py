# -*- coding: UTF-8 -*-
# Copyright 2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from rest_framework import serializers
from django.db.models import ForeignKey
from lino.core.choicelists import ChoiceListField, ChoiceList
from .fields import ChoiceField


def get_serializer_for_model(Model, options={}):
    fks = []
    clfs = []
    for fld in Model._meta.fields:
        if isinstance(fld, ForeignKey):
            fks.append(fld)
        elif isinstance(fld, ChoiceListField):
            clfs.append(fld)

    meta_attrs = {
        'model': Model,
    }

    if options.get('fields', None) is not None:
        meta_attrs['fields'] = options['fields']
    else:
        meta_attrs['fields'] = '__all__'

    attrs_dict = dict(Meta=type('Meta', (type, ), meta_attrs))

    if options.get('extra_fields', None) is not None:
        attrs_dict.update(options['extra_fields'])

    for fld in clfs:
        attrs_dict[fld.name] = ChoiceField(choicelist=fld.choicelist)

    Serializer = type('Serializer', (serializers.ModelSerializer, ), attrs_dict)
    return Serializer


def unused_get_serializer_for_model(Model, options={}):
    fks = []
    clfs = []
    for fld in Model._meta.fields:
        if isinstance(fld, ForeignKey):
            fks.append(fld)
        elif isinstance(fld, ChoiceListField):
            clfs.append(fld)

    class DefaultSerializer(serializers.ModelSerializer):
        class Meta:
            model = Model
            if options.get('fields', None) is not None:
                fields = options['fields']
            else:
                fields = '__all__'
            # exclude = [fld.name for fld in clfs]

        # def to_representation(self, instance):
        #     data = super().to_representation(instance)
        #     return data

    # for name in fks:
    #     setattr(DefaultSerializer, name, serializers.PrimaryKeyRelatedField(read_only=True))

    for fld in clfs:
        setattr(DefaultSerializer, fld.name, get_choice_list_field_serializer())
    ef = options.get('extra_fields', None)
    if ef is not None:
        for k, v in ef.items():
            setattr(DefaultSerializer, k, v)

    return DefaultSerializer
