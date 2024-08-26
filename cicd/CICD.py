#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from functools import lru_cache
from typing import Any

from cicd.Utils import is_float, is_json_object


class CICD:
    """
    The `CICD` class represents a Continuous Integration/Continuous Deployment (CICD) pipeline. It provides methods for constructing and manipulating CICD objects.

    ## Constructor

    ```python
    def __init__(self, properties: Any = None)
    ```

    Constructs a new instance of the `CICD` class.

    ### Parameters

    - `properties` (optional): A dictionary containing properties to be set on the object. If provided, the properties will be set using the `__set_properties` method.

    ## Methods

    ### `__set_properties`

    ```python
    @classmethod
    def __set_properties(cls, properties)
    ```

    Sets the properties of the object based on the provided dictionary.

    ### Parameters

    - `properties`: A dictionary containing the properties to be set.

    ### `from_dict`

    ```python
    @classmethod
    def from_dict(cls, data: dict[str, Any])
    ```

    Converts a dictionary into an instance of the current class.

    ### Parameters

    - `data`: A dictionary containing the data to be used for creating the instance.

    ### `from_json`

    ```python
    @classmethod
    def from_json(cls, json_str: str)
    ```

    Converts a JSON string to an object of the current class.

    ### Parameters

    - `json_str`: The JSON string to be converted.

    ### `to_dict`

    ```python
    def to_dict(self)
    ```

    Returns a dictionary representation of the object.

    ### Return Value

    - A dictionary containing the keys and values of the object's attributes.

    ### `to_json`

    ```python
    def to_json(self, indent=4, separators=None, sort_keys=True)
    ```

    Converts the Python object to a JSON-formatted string.

    ### Parameters

    - `indent` (optional): An integer specifying the number of spaces used for indentation in the JSON string. Default is 4.
    - `separators` (optional): A tuple specifying the separators used in the JSON string. Default is None.
    - `sort_keys` (optional): A boolean specifying whether the keys in the JSON string should be sorted. Default is True.

    ### Return Value

    - A string containing the JSON representation of the Python object.

    ### `__getattr__`

    ```python
    def __getattr__(self, attr)
    ```

    Retrieves the value of a property attribute that may not be directly accessible.

    ### Parameters

    - `attr`: The name of the property attribute.

    ### Return Value

    - The value of the property attribute, if it exists.

    ### `__repr__`

    ```python
    def __repr__(self)
    ```

    Returns a string representation of the object.

    ### Return Value

    - A string representation of the object.
    """

    def __init__(self, properties: Any = None):
        """
        Constructs a new instance of the class.

        :param properties: A dictionary containing properties to be set on the object.
            If provided, the properties will be set using the __set_properties method.
        """
        if properties:
            self.__set_properties(properties)

    @classmethod
    def __set_properties(cls, properties):
        """Sets the properties of the object based on the provided dictionary.

        :param properties: A dictionary containing the properties to be set.
        :return: None
        """
        cls_fields: list[str] = sorted(list(cls.__dataclass_fields__.keys()))
        properties_dict_fields: list[str] = sorted(list(set(list(properties.keys()))
                                                        .intersection(cls_fields)))
        for key in properties_dict_fields:
            if key in cls_fields:
                value = properties[key]
                if isinstance(value, list):
                    result = [cls(item) if isinstance(item, dict) else item for item in value]
                elif isinstance(value, dict):
                    result = cls(value)
                elif str(value).lower() in ['true', 'false'] or isinstance(value, bool):
                    result = bool(value)
                elif str(value).isdigit() or isinstance(value, int):
                    result = int(value)
                elif is_float(value):
                    result = float(value)
                elif is_json_object(value):
                    result = cls.from_json(value)
                else:
                    result = value
                setattr(cls, key, result)

    @classmethod
    @lru_cache(maxsize=None)
    def __to_dict(cls):
        result: dict = {}
        cls_fields: list[str] = sorted(list(cls.__dataclass_fields__.keys()))
        print()
        for idx, key in enumerate(cls_fields):
            attribute_value: Any = getattr(cls, key)
            if isinstance(attribute_value, cls):
                to_dict_result = attribute_value.to_dict()
                result.update({key: to_dict_result})
            elif isinstance(attribute_value, list):
                list_result: list[any] = []
                for item in attribute_value:
                    if isinstance(item, cls):
                        list_result.append(item.to_dict())
                    else:
                        list_result.append(item)
                result.update({key: list_result})
            elif isinstance(attribute_value, bool):
                result[key] = bool(attribute_value)
            elif isinstance(attribute_value, int):
                result[key] = int(attribute_value)
            elif is_float(attribute_value):
                result[key] = float(attribute_value)
            elif is_json_object(attribute_value):
                result.update({key: json.loads(attribute_value)})
            else:
                result.update({key: attribute_value})
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        """
        Converts a dictionary into an instance of the current class.

        :param data: A dictionary containing the data to be used for creating the instance.
        :return: An instance of the current class with the data populated.
        """
        return cls(data)

    @classmethod
    def from_json(cls, json_str: str):
        """
        Converts a JSON string to an object of the current class.

        :param json_str: The JSON string to be converted.
        :return: An object of the current class created from the given JSON string.
        """
        data = json.loads(json_str)
        return cls.from_dict(data)

    def to_dict(self):
        """
        Returns a dictionary representation of the object.

        :return: Dictionary containing the keys and values of the object's attributes.
        """
        return self.__to_dict()

    def to_json(self, indent=4, separators=None, sort_keys=True):
        """
        Converts the Python object to a JSON-formatted string.

        :param indent: An optional integer specifying the number of spaces used for indentation in the JSON string.
            Default is 4.
        :param separators: An optional tuple specifying the separators used in the JSON string.
            Default is None.
        :param sort_keys: An optional boolean specifying whether the keys in the JSON string should be sorted.
            Default is True.
        :return: A string containing the JSON representation of the Python object.
        """
        return json.dumps(self.__dict__,
                          default=lambda o: o.__dict__,
                          separators=separators,
                          sort_keys=sort_keys,
                          indent=indent if separators is None else None)

    def __getattr__(self, attr):
        try:
            return self._properties[attr]
        except KeyError:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{attr}'")

    def __repr__(self):
        """
        Returns a string representation of the object.

        :return: A string representation of the object.
        """
        return f'{self.__class__.__name__}({self.__dict__})'
