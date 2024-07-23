from rest_framework import serializers

from areas.models import (
    Area,
    Contact,
    Photo,
)


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = [
            'contact',
            'contact_type',
        ]


class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = [
            'photo',
        ]


class AreaSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(
        many=True,
    )
    photos = PhotoSerializer(
        many=True,
    )

    class Meta:
        model = Area
        fields = [
            'pk',
            'name',
            'description',
            'address',
            'price',
            'capacity',
            'width',
            'length',
            'contacts',
            'photos',
            'created_at',
        ]