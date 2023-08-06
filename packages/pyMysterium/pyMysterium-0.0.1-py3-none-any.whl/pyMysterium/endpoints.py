import urllib.parse

class EndPoints:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.access_policies = self.__join_url("access-policies")
        self.connection = self.__join_url("connection")
        self.current_ip = self.__join_url("connection/ip")
        self.connection_location = self.__join_url("connection/location")
        self.connection_stats = self.__join_url("connection/statistics")
        self.exchange = self.__join_url("exchange/myst/{currency}")
        self.identities = self.__join_url("identities")
        self.current_identity = self.__join_url("identities/current")
        self.get_identity = self.__join_url("identities/{id}")
        self.beneficiary_address = self.__join_url("identities/{id}/beneficiary")
        self.register_identity = self.__join_url("identities/{id}/register")
        self.registration_status = self.__join_url("identities/{id}/registration")
        self.unlock_identity = self.__join_url("identities/{id}/unlock")
        self.import_identity = self.__join_url("identities-import")
        self.get_all_orders = self.__join_url("identities/{id}/payment-order")
        self.get_order_info = self.__join_url("identities/{id}/payment-order/{order_id}")
        self.payment_order_options = self.__join_url("payment-order-options")
        self.payment_order_currencies = self.__join_url("payment-order-currencies")
        self.host_location = self.__join_url("location")
        self.proposals = self.__join_url("proposals")
        self.terms = self.__join_url("terms")

    def __join_url(self, url: str) -> str:
        return urllib.parse.urljoin(self.base_url, url)
