from schema import Schema
from file_managment import Paths
import file_managment as fm
import os
import uuid


# TODO: Change all references to paths in to using os.path.join()

class DocumentException(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class Document:
    def __init__(self, schema: Schema, uid: str = None) -> None:
        """
        Creates a document that will follow a given schema.

        Initially all values in the document are dummies and must be redefined to be sensible.

        :param schema: (Schema) object that defines all attribute fields for a given document to have
        :param uid: (str) unique id that is saved both in the data of the object and that acts as its unique filename
        """
        assert isinstance(schema, Schema)
        self._uuid = uuid.uuid4() if uid is None else uid
        self._schema = schema
        self._attributes = schema.get_attributes()
        self._attributes["uuid"] = self._uuid.__str__()

    def set_attribute_value(self, atr_name: str, atr_value: object) -> None:
        """
        Sets an attribute to the value passed.

        :param atr_name: (str) attribute name that is defined by the schema
        :param atr_value: (object) any value that will be associated with the attribute

        :raises DocumentException if the attribute is not defined by the schema
        """
        if self._attributes.get(atr_name, None) is None:
            raise DocumentException("Attribute name is not defined")
        self._attributes[atr_name] = atr_value

    def get_attribute_value(self, atr_name: str) -> object:
        """
        Returns value for the given attribute. The attribute must be defined by the schema

        :rtype: object

        :raises DocumentException if the attribute is not defined by the schema
        """
        if self._attributes.get(atr_name, None) is None:
            raise DocumentException("Attribute name is not defined")
        return self._attributes.get(atr_name)

    def save(self) -> None:
        """
        Saves the document as a JSON object in the appropriate folder.
        The document must not have been saved to call this method.

        :return: None
        """
        fm.save_new_file(self._uuid, self.to_json(), self._schema.get_document_folder_url())

    def update(self) -> None:
        """
        Updates a JSON file that contains the information for the given document.
        The document must be saved with save() method before calling this method.

        :return: None
        """
        fm.rewrite_file(self._uuid, self.to_json(), self._schema.get_document_folder_url())

    def to_json(self) -> dict:
        """
        Converts the document object into a JSON-serializable object

        :return: dict containing attributes of the object
        """
        return self._attributes
