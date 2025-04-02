# pubsub.py
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

class AsyncConn:
    def __init__(self, id: str, channel_name: str) -> None:
        config = PNConfiguration()
        config.publish_key = 'pub-c-e146e5e2-7fb7-44b3-ac76-9eaca0cc110a'
        config.subscribe_key = 'sub-c-f7dedfee-2b67-4482-8d96-12380d34d3de'
        config.secret_key = 'sec-c-MTViZWM2MDctZjVhMi00NzA3LTk1ZmQtMjlhOTdlMDBiYmVm'
        config.user_id = id
        config.enable_subscribe = True
        config.daemon = True

        self.pubnub = PubNub(config)
        self.channel_name = channel_name

        print(f"Configurando conexão com o canal '{self.channel_name}'...")
        subscription = self.pubnub.channel(self.channel_name).subscription()
        subscription.subscribe()

    def publish(self, data: dict):
        print("Publicando mensagem no PubNub...")
        self.pubnub.publish().channel(self.channel_name).message(data).sync()
