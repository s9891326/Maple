from rest_framework import serializers

from exchange.models import EquipLibrary, Equip


class EquipLibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipLibrary
        fields = '__all__'


class EquipSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Equip
        fields = '__all__'
