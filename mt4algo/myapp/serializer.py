from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    SYMBOL, GROUP, Broker, mt5_server, ClientDetail, Strategy,
    ClientSymbolSetting, ClientSignal, Client_SYMBOL_QTY, HelpMessage, MT4Account, 
    Trade, TradeHistory, ClientActivity, TradeStatus, OperationMessage, 
    MT5OperationLog, KYC, ClientStatus
)


# Get the custom user model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'is_staff', 'is_superuser']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

class SuperUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create_superuser(email=validated_data['email'], password=password)
        return user



class SYMBOLSerializer(serializers.ModelSerializer):
    class Meta:
        model = SYMBOL
        fields = ['id', 'user', 'SYMBOL', 'created_at']
        read_only_fields = ['created_at']

class GROUPSerializer(serializers.ModelSerializer):
    class Meta:
        model = GROUP
        fields = ['id', 'user', 'GROUP', 'min_quantity', 'max_quantity', 'created_at']
        read_only_fields = ['created_at']

class BrokerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Broker
        fields = ['id', 'user', 'broker', 'created_at']
        read_only_fields = ['created_at']

class MT5ServerSerializer(serializers.ModelSerializer):
    broker = serializers.StringRelatedField()  # Display the broker name

    class Meta:
        model = mt5_server
        fields = ['id', 'broker', 'mt5_server', 'created_at']
        read_only_fields = ['created_at']

class ClientDetailSerializer(serializers.ModelSerializer):
    client_Group = serializers.StringRelatedField()
    broker = serializers.StringRelatedField()

    class Meta:
        model = ClientDetail
        fields = [
            'id', 'user_id', 'user_active', 'name_first', 'name_last', 'email', 'password', 
            'phone_number', 'verify_code', 'date_joined', 'last_login', 'panel_last_login', 
            'clint_plane', 'client_Group', 'broker', 'is_staff', 'clint_status', 'country', 
            'city', 'mt5_login', 'mt5_password', 'mt5_server', 'account_type', 'sub_admin_id', 
            'paid_paln', 'Term_condition', 'ip_address', 'updated_by', 'selected_option'
        ]
        extra_kwargs = {'password': {'write_only': True}}  # Ensure the password is write-only

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        client = ClientDetail(**validated_data)
        if password:
            client.set_password(password)  # Use Django's password hashing
        client.save()
        return client

class StrategySerializer(serializers.ModelSerializer):
    class Meta:
        model = Strategy
        fields = ['id', 'Strategy', 'created_at']
        read_only_fields = ['created_at']


class ClientSymbolSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientSymbolSetting
        fields = ['id', 'client', 'symbol', 'quantity', 'trade_enabled']

class ClientSignalSerializer(serializers.ModelSerializer):
    SYMBOL = serializers.StringRelatedField()

    class Meta:
        model = ClientSignal
        fields = [
            'id', 'user', 'admin', 'client_id', 'message_id', 'ids', 
            'SYMBOL', 'TYPE', 'QUANTITY', 'ENTRY_PRICE', 'EXIT_PRICE', 
            'profit_loss', 'cumulative_pl', 'created_at'
        ]

class ClientSymbolQtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Client_SYMBOL_QTY
        fields = ['id', 'client_id', 'SYMBOL', 'QUANTITY', 'trade', 'created_at']

class HelpMessageSerializer(serializers.ModelSerializer):
    user_id = serializers.StringRelatedField()

    class Meta:
        model = HelpMessage
        fields = ['id', 'user_id', 'client_name', 'message', 'timestamp']

class MT4AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = MT4Account
        fields = ['id', 'login', 'password', 'server']

class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = [
            'id', 'ticket', 'symbol', 'volume', 'price_open', 
            'price_current', 'sl', 'tp', 'profit', 'time', 'type'
        ]

class TradeHistorySerializer(serializers.ModelSerializer):
    client = serializers.StringRelatedField()

    class Meta:
        model = TradeHistory
        fields = [
            'id', 'client', 'signal_time', 'symbol', 'trade_type', 'quantity', 
            'entry_price', 'exit_price', 'exit_time', 'ticket_id', 'p_l', 'cumulative_p_l'
        ]

class ClientActivitySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = ClientActivity
        fields = ['id', 'user', 'time', 'ip_address', 'action', 'symbol', 'quantity', 'updated_by']

class TradeStatusSerializer(serializers.ModelSerializer):
    client = serializers.StringRelatedField()

    class Meta:
        model = TradeStatus
        fields = ['id', 'client', 'symbol', 'quantity', 'status_message', 'timestamp']

class OperationMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationMessage
        fields = ['id', 'timestamp', 'operation_type', 'message']

class MT5OperationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MT5OperationLog
        fields = ['id', 'operation_type', 'client_login', 'symbol', 'message', 'timestamp']

class KYCSerializer(serializers.ModelSerializer):
    client = serializers.StringRelatedField()

    class Meta:
        model = KYC
        fields = [
            'id', 'client', 'national_id', 'national_id_number', 'national_id_name', 
            'national_id_issue_date', 'agreement_signed', 'terms_accepted', 'reference_text', 
            'kyc_completed', 'video_file', 'video_verification_done'
        ]

class ClientStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientStatus
        fields = [
            'id', 'sub_admin_id', 'clint_id', 'name', 'time', 'clint_email', 'clint_phone_number', 
            'service_name', 'quantity', 'strategy', 'login_date_time', 'panel_last_login', 
            'clint_plane', 'trading', 'ip_address', 'updated_by', 'client_status'
        ]
