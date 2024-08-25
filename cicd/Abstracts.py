from abc import ABC
from dataclasses import dataclass


@dataclass
class Abstract(ABC):
    def __init__(self, properties_dict=None):
        """
        Constructs a new instance of the class.

        :param properties_dict: A dictionary containing properties to be set on the object. If provided, the properties will be set using the __set_properties method.
        """
        if properties_dict and isinstance(properties_dict, dict):
            for key, value in properties_dict.items():
                setattr(self, key, value)

    def __getattr__(self, attr):
        try:
            return self._properties[attr]
        except KeyError:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{attr}'")

    def to_dict(self):
        """
        Returns a dictionary representation of the object.

        :return: Dictionary containing the keys and values of the object's attributes.
        """
        return self.__dict__
