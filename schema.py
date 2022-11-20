from enum import Enum
import file_managment as fm
from file_managment import Paths


class SchemaException(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class AttributeType(Enum):
    STRING = 1,
    INTEGER = 2,
    LIST = 3,

    def get_value(self):
        return self.value[0]


class Schema:
    def __init__(self, name: str, attributes: dict = None) -> None:
        """
        Creates a new Schema that will be used to create and work with documents.

        :param name: (str) a unique name (you will have to keep track of that on your own)
                          that identifies a given schema
        :param attributes: (dict) a dictionary that contains all attributes that a document must be following.
                                  When creating a new schema do not set this attribute
        """
        self._name = name
        self._attributes = {} if attributes is None else attributes

    def add_attribute(self, atr_name: str, atr_type: AttributeType) -> None:
        """
        Adds a new attribute to the schema. This method should not be called after
        a single document was created using this schema

        :param atr_name: (str) attribute name
        :param atr_type: (AttributeType) attribute type (does not really work now)

        :raises SchemaException if attribute with such name is already defined, or
                                 if atr_type is not in AttributeType enum
        """
        if self._attributes.get(atr_name, None) is not None:
            raise SchemaException("Attribute name is not unique")
        if atr_type not in AttributeType:
            raise SchemaException("Attribute type is not defined")
        self._attributes[atr_name] = atr_type.get_value()

    def update_attribute(self, atr_name: str, atr_type: AttributeType) -> None:
        """
        Chnages value type of an attribute. This method should not be called after
        a single document was created using this schema

        :param atr_name: (str) attribute name
        :param atr_type: (AttributeType) attribute type (does not really work now)

        :raises SchemaException if attribute with such name is not defined, or
                                 if atr_type is not in AttributeType enum
        """
        if self._attributes.get(atr_name, None) is None:
            raise SchemaException("Attribute name is not defined")
        if atr_type not in AttributeType:
            raise SchemaException("Attribute type is not defined")
        self._attributes[atr_name] = atr_type.get_value()

    def update(self) -> None:
        """
        Updates a JSON file that contains the information for the given schema.
        The schema must be saved with save() method before calling this method.

        :return: None
        """
        fm.rewrite_file(self._name, self.to_json(), Paths.SCHEMA.get_value())

    def save(self) -> None:
        """
        Saves the schema as a JSON object in the appropriate folder.
        The schema must not have been saved to call this method.

        Also, an associated folder inside the documents folder will be created,
         where all documents following the given schema will be saved.

        :return: None
        """

        fm.save_new_file(self._name, self.to_json(), Paths.SCHEMA.get_value())
        fm.create_folder(self._name, Paths.DOCUMENTS.get_value())

    def to_json(self) -> dict:
        """
        Converts the schema object into a JSON-serializable object

        :return: dict containing attributes of the object
        """
        return {"name": self._name, "attributes": self._attributes}

    def get_attributes(self) -> dict:
        """
        Getter for the attributes of the schema

        :return: (dict) all attributes of the schema
        """
        return self._attributes

    def get_name(self) -> str:
        """
        Getter for the name of the schema

        :return: (str) name of the schema
        """
        return self._name

    def get_document_folder_url(self) -> str:
        """
        Returns a path of the folder that stores all documents associated with the schema

        :return: (str) path to the folder with all the documents
        """
        return Paths.DOCUMENTS.get_value() + "/" + self.get_name() + "/"

    @staticmethod
    def get_schema(schema_name: str):
        """
        Returns a Schema object using the unique name to find it in the database.

        :param schema_name: (str) name of the schema

        :return: (Schema) an object of Schema containing all attributes
        """
        if fm.file_exists(schema_name, Paths.SCHEMA.get_value()):
            data = fm.read_file_content(schema_name, Paths.SCHEMA.get_value())
            return Schema(data["name"], data["attributes"])
        return None
