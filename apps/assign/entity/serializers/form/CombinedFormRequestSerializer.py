from rest_framework import serializers


class EnterpriseSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    name = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    tax_id = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    address = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    email = serializers.EmailField(required=False, allow_null=True)
    phone = serializers.CharField(required=False, allow_blank=True, allow_null=True)


class BossSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    name = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    email = serializers.EmailField(required=False, allow_null=True)
    phone = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    position = serializers.CharField(required=False, allow_blank=True, allow_null=True)


class HumanTalentSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    name = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    email = serializers.EmailField(required=False, allow_null=True)
    phone = serializers.CharField(required=False, allow_blank=True, allow_null=True)


class RequestSerializer(serializers.Serializer):
    apprentice = serializers.IntegerField(required=False, allow_null=True)
    ficha = serializers.IntegerField(required=False, allow_null=True)
    contract_start_date = serializers.DateField(required=False, allow_null=True)
    contract_end_date = serializers.DateField(required=False, allow_null=True)
    sede = serializers.IntegerField(required=False, allow_null=True)
    modality_productive_stage = serializers.IntegerField(required=False, allow_null=True)


class CombinedFormRequestSerializer(serializers.Serializer):
    enterprise = EnterpriseSerializer()
    boss = BossSerializer()
    human_talent = HumanTalentSerializer()
    request = RequestSerializer()
