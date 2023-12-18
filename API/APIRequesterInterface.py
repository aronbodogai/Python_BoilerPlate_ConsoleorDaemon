from abc import ABC, abstractmethod
import requests

class APIRequesterInterface(ABC):
    @abstractmethod
    def get(self, endpoint: str, params: dict = None) -> dict:
        """Make a GET request to the given endpoint with the optional parameters."""
        pass

    @abstractmethod
    def post(self, endpoint: str, data: dict = None) -> dict:
        """Make a POST request to the given endpoint with the optional data."""
        pass

    @abstractmethod
    def put(self, endpoint: str, data: dict = None) -> dict:
        """Make a PUT request to the given endpoint with the optional data."""
        pass

    @abstractmethod
    def delete(self, endpoint: str) -> dict:
        """Make a DELETE request to the given endpoint."""
        pass
