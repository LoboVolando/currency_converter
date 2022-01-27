from rest_framework import serializers
from .models import Rate


class RateSerializer(serializers.ModelSerializer):
    """
    Сериалайзер записи обменных курсов
    """
    class Meta:
        model = Rate
        fields = ['date', 'eur', 'pln', 'czk']
