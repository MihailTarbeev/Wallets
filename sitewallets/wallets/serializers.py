import io
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Wallet
import uuid


# class WalletSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Wallet
#         fields = ('uuid', 'balance')


# Ниже расписан базовый функционал сериализатора.
# Показано, как он сериализирует простейший класс WalletModel
# С помощью класса-сериализатора WalletSerializer
class WalletModel:
    'Пример модели, которую мы хоти сериализовать в JSON формат'

    def __init__(self, uuid, balance):
        self.uuid = uuid
        self.balance = balance


class WalletSerializer(serializers.Serializer):
    '''
    Класс сериализатор для преобразования класса WalletModel в JSON формат
    Имена должны совпадать в сериализаторе и преобразующем классе
    '''

    uuid = serializers.UUIDField(default=uuid.uuid4)
    balance = serializers.DecimalField(max_digits=20,
                                       decimal_places=2,
                                       default=0.00)


def encode():
    model = WalletModel("e33bd416dd9f43a984c7aabb334c8ce6", 20.11)
    model_sr = WalletSerializer(model)
    print(model_sr.data, type(model_sr.data), sep='\n')
    json = JSONRenderer().render(model_sr.data)
    print(json)


def decode():
    stream = io.BytesIO(
        b'{"uuid":"e33bd416dd9f43a984c7aabb334c8ce6","balance":"20.11"}')
    data = JSONParser().parse(stream)
    serializer = WalletSerializer(data=data)
    serializer.is_valid()
    print(serializer.validated_data)
