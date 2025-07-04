from rest_framework import serializers

class baseMixedSerializer:
    fdl =  serializers.IntegerField(required=False , read_only = True)
    cbu = serializers.IntegerField(required=False, read_only=True)
    cat = serializers.DateTimeField(required=False , read_only=True)
    uat =  serializers.DateTimeField(required=False , read_only= True)
    luu = serializers.IntegerField(required=False , read_only=True)

