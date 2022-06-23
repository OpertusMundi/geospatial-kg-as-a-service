from abc import ABC, abstractmethod
from typing import Union


class PIDServiceClient(ABC):
    @abstractmethod
    def get_custom_id(self, topio_id: str) -> Union[str, None]:
        pass

    @abstractmethod
    def get_topio_id(self, custom_id: str) -> Union[str, None]:
        pass

    @abstractmethod
    def register_asset(
            self, asset_local_id: str, user_id: int, description: str = None):
        pass

    @abstractmethod
    def register_user(self, user_name: str, user_namespace: str):
        pass


class DummyPIDServiceClient(PIDServiceClient):
    """
    Dummy PID service client which does not perform any lookups but serves the
    Topio ID-local ID mappings via a local dictionary
    """
    def __init__(self):
        # Nothing to do here
        self._id_mappings = {}
        self._assets = {}
        self._asset_cntr = 0
        self._users = {
            0: {
                'namespace': 'default',
                'name': 'Default User'
            }
        }
        self._users_cntr = 0
        self._default_asset_type = 'file'

    def _get_next_user_id(self):
        self._users_cntr += 1
        return self._users_cntr

    def _get_next_asset_id(self):
        self._asset_cntr += 1
        return self._asset_cntr

    def _get_topio_id(self, asset_id: int, user_id: int = 0):
        user_ns = self._users[user_id]['namespace']

        return f'topio.{user_ns}.{asset_id}.{self._default_asset_type}'

    def set_id_mappings(self, mappings: dict):
        self._id_mappings = mappings

    def register_user(self, user_name: str, user_namespace: str):
        user_id = self._get_next_user_id()

        self._users[user_id] = {
            'name': user_name,
            'namespace': user_namespace
        }

    def get_custom_id(self, topio_id: str) -> Union[str, None]:
        return self._id_mappings.get(topio_id, None)

    def get_topio_id(self, custom_id: str) -> Union[str, None]:
        for k, v in self._id_mappings.items():
            if v == custom_id:
                return k

        return None

    def register_asset(
            self,
            local_id: str,
            user_id: int = 0,
            description: str = None
    ):

        asset_id = self._get_next_asset_id()
        topio_id = self._get_topio_id(asset_id, user_id)

        self._assets[asset_id] = {
            'local_id': local_id,
            'owner_id': user_id,
            'asset_type': self._default_asset_type,
            'topio_id': topio_id
        }

        self._id_mappings[topio_id] = local_id
