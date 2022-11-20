"""
All queries will be in a form of a function. The return of a function will be the result of the query.
"""
from typing import List

from schema import Schema
from document import Document
import file_managment as fm


class QueryObject:

    def __init__(self, schema: Schema) -> None:
        """
        Creates an object through which a set of queries can be executed.

        :param schema: (Schema) on which the operations will be carried on
        """
        assert isinstance(schema, Schema)
        self._schema = schema

    def save(self, document_atr: dict) -> None:
        """
        Saves a dictionary passed as a new document.
        The new document must follow the predefined schema.
        The inputted dictionary will be used to fill in the
        document according to the attributes present in a schema

        :param document_atr: (dict) Dictionary that corresponds to the schema set.
        """
        assert isinstance(document_atr, dict)
        document = Document(self._schema)
        for key, value in document_atr.items():
            document.set_attribute_value(key, value)
        document.save()

    def update_by_uid(self, uid: str, atr_name: str, atr_val: object) -> None:
        """
        Updates one attribute in a document using uuid to identify the document.

        :param uid: (str) uuid of a document
        :param atr_name: (str) name of an attribute that is present in the schema
        :param atr_val: (object) value which will be associated with the attribute

        :raises AttributeError if the attribute is not defined on the document
        """
        data = fm.read_file_content(uid, self._schema.get_document_folder_url())
        if data.get(atr_name, None) is None:
            raise AttributeError
        data[atr_name] = atr_val
        fm.rewrite_file(uid, data, self._schema.get_document_folder_url())

    def delete_by_uid(self, uid: str) -> bool:
        """
        Deletes a document by its uuid.

        :param uid: (str) uuid of a document
        :return: (bool) True if the document was deleted successfully, False if the file was not found.
        """
        try:
            fm.delete_file(uid, self._schema.get_document_folder_url())
            return True
        except FileNotFoundError:
            return False

    def find_by_uid(self, uid: str) -> dict:
        """
        Returns contents of a given document, which will be searched using uuid.

        :param uid:  (str) uuid of a document
        :return: (dict) contents of a document or an empty dictionary if the document does not exist.
        """
        if fm.file_exists(uid, self._schema.get_document_folder_url()):
            return fm.read_file_content(uid, self._schema.get_document_folder_url())
        return {}

    def find_all_where_attribute_eql(self, atr_name: str, atr_val: object) -> List[dict]:
        """
        Returns all documents that contain a given value associated with a given attribute.

        :param atr_name: (str) name of the attribute present on a schema
        :param atr_val: (object) value to which the the attribute must match

        :return: List[dict] containing all documents that qualify for the search
        """
        data = self.find_all()
        qualified_data = []
        for document in data:
            assert isinstance(document, dict)
            if document.get(atr_name, None) == atr_val:
                qualified_data.append(document)
        return qualified_data

    def find_all_where_attribute_contains(self, atr_name: str, atr_val: object) -> List[dict]:
        """
         Returns all documents that contain a given value in a given attribute (the attribute must be a list).

        :param atr_name: (str) name of the attribute present on a schema
        :param atr_val: (object) value must be in a list.
        :return: List[dict] containing all documents that qualify for the search
        """
        data = self.find_all()
        qualified_data = []
        for document in data:
            assert isinstance(document, dict)
            if atr_val in document.get(atr_name, []):
                qualified_data.append(document)
        return qualified_data

    def find_all(self) -> List[dict]:
        """
        Returns all documents associated with a given schema.

        :return: List[dict] containing all documents that use given schema
        """
        file_names = list(
            map(lambda filename: filename[0:-5], fm.get_all_file_names(self._schema.get_document_folder_url())))
        data = []
        for file_name in file_names:
            data.append(fm.read_file_content(file_name, self._schema.get_document_folder_url()))
        return data
