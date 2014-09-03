from rest_framework import serializers
from django.contrib.auth.models import Group, Permission

from devices.models import Room, Building, Manufacturer, Device, Template, Lending
from django.contrib.auth.models import  Group
from devicetypes.models import Type, TypeAttribute
from users.models import Lageruser, Department
from network.models import IpAddress

class UnicodeNameField(serializers.RelatedField):
    def to_native(self, value):
        return value.__unicode__()

class BuildingSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='building-api-detail')
    id = serializers.CharField(source="pk", read_only=True)

    class Meta:
        model = Building


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='room-api-detail')
    id = serializers.CharField(source="pk", read_only=True)
    building = BuildingSerializer()

    class Meta:
        model = Room


class ManufacturerSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='manufacturer-api-detail')
    id = serializers.CharField(source="pk", read_only=True)

    class Meta:
        model = Manufacturer


class TypeAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeAttribute
        exclude = ("devicetype", )


class TypeSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='type-api-detail')
    id = serializers.CharField(source="pk", read_only=True)
    typeattribute_set = TypeAttributeSerializer()

    class Meta:
        model = Type


class TemplateSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='template-api-detail')
    id = serializers.CharField(source="pk", read_only=True)

    class Meta:
        model = Template


class LendingDisplaySerializer(serializers.ModelSerializer):
    owner = UnicodeNameField()
    owner_url = serializers.HyperlinkedIdentityField(source="owner", view_name='user-api-detail')

    class Meta:
        model = Lending


class DeviceSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='device-api-detail')
    id = serializers.CharField(source="pk", read_only=True)
    manufacturer = serializers.SlugRelatedField(slug_field="name")
    room = serializers.SlugRelatedField(slug_field="name", queryset=Room.objects.select_related("building").all())
    devicetype = serializers.SlugRelatedField(slug_field="name")
    ip_addresses = serializers.SlugRelatedField(many=True, source='ipaddress_set', slug_field="address")
    creator = UnicodeNameField()
    creator_url = serializers.HyperlinkedIdentityField(view_name='user-api-detail')
    currentlending = LendingDisplaySerializer(required=False, read_only=True)
    bookmarked = serializers.BooleanField()

    class Meta:
        model = Device
        exclude = ("bookmarkers", )

class DeviceListSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='device-api-detail')
    id = serializers.CharField(source="pk", read_only=True)

    class Meta:
        model = Device
        fields = ("url", "id", "name")

class DeviceRoomSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='device-api-detail')
    id = serializers.CharField(source="pk", read_only=True)
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.select_related("building").all())

    class Meta:
        model = Device
        fields = ("url", "id", "room")


class LendingSerializer(serializers.ModelSerializer):
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.select_related("building").all(), required=False)

    class Meta:
        model = Lending
        exclude = ("lenddate", "duedate_email", "returndate")

    def validate(self, attrs):
        if "smalldevice" in attrs and "device" in attrs:
            if attrs["device"] and attrs["smalldevice"]:
                raise serializers.ValidationError("can not set both device and smalldevice")
            elif not attrs["device"] and not attrs["smalldevice"]:
                raise serializers.ValidationError("you have to either set device or smalldevice")
        elif not "smalldevice" in attrs and not "device" in attrs:
            raise serializers.ValidationError("you have to either set device or smalldevice")
        if "device" in attrs:
            if attrs["device"] != "" and attrs["device"] != None:
                if attrs["device"].currentlending:
                    raise serializers.ValidationError("this device is already lend.")
        return attrs

    def restore_object(self, attrs, instance=None):
        if self.context["request"].POST:
            del attrs["room"]
            del self.fields["room"]
        obj = super(LendingSerializer, self).restore_object(attrs, instance=instance)
        return obj

    def to_native(self, obj):
        if self.context["request"].POST:
            if "room" in self.fields:
                del self.fields["room"]
        return super(LendingSerializer, self).to_native(obj)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='user-api-detail')
    id = serializers.CharField(source="pk", read_only=True)
    groups = serializers.SlugRelatedField(many=True, slug_field="name", queryset=Group.objects.all())
    user_permissions = serializers.SlugRelatedField(many=True, slug_field="name", queryset=Permission.objects.all())
    main_department = serializers.SlugRelatedField(slug_field="name")
    departments = serializers.SlugRelatedField(many=True, slug_field="name", queryset=Department.objects.all())

    class Meta:
        model = Lageruser
        exclude = ("password", )


class UserAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lageruser
        fields = ("username", "avatar")


class UserListSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='user-api-detail')
    id = serializers.CharField(source="pk", read_only=True)

    class Meta:
        model = Lageruser
        fields = ("url", "id", "username", "first_name", "last_name", "email")


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='group-api-detail')
    id = serializers.CharField(source="pk", read_only=True)
    users = UserListSerializer(many=True, source="user_set")
    permissions = serializers.SlugRelatedField(slug_field="name", many=True)

    class Meta:
        model = Group

class IpAddressSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='ipaddress-api-detail')
    id = serializers.CharField(source="pk", read_only=True)
    user = UnicodeNameField()
    device = serializers.SlugRelatedField(slug_field="name")

    class Meta:
        model = IpAddress