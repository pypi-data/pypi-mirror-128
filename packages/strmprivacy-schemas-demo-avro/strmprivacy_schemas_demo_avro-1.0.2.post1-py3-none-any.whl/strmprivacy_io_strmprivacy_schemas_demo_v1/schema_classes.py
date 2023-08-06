import json
import os.path
import decimal
import datetime
import six
from avrogen.dict_wrapper import DictWrapper
from avrogen import avrojson
from avro import schema as avro_schema
if six.PY3:    from avro.schema import SchemaFromJSONData as make_avsc_object
    
else:
    from avro.schema import make_avsc_object
    


def __read_file(file_name):
    with open(file_name, "r") as f:
        return f.read()

def __get_names_and_schema(file_name):
    names = avro_schema.Names()
    schema = make_avsc_object(json.loads(__read_file(file_name)), names)
    return names, schema

__NAMES, SCHEMA = __get_names_and_schema(os.path.join(os.path.dirname(__file__), "schema.avsc"))
__SCHEMAS = {}
def get_schema_type(fullname):
    return __SCHEMAS.get(fullname)
__SCHEMAS = dict((n.fullname.lstrip("."), n) for n in six.itervalues(__NAMES.names))


class SchemaClasses(object):
    
    
    pass
    class io(object):
        class strmprivacy(object):
            class schemas(object):
                class demo(object):
                    class v1(object):
                        
                        class DemoEventClass(DictWrapper):
                            
                            """
                            
                            """
                            
                            
                            RECORD_SCHEMA = get_schema_type("io.strmprivacy.schemas.demo.v1.DemoEvent")
                            
                            
                            def __init__(self, inner_dict=None):
                                super(SchemaClasses.io.strmprivacy.schemas.demo.v1.DemoEventClass, self).__init__(inner_dict)
                                if inner_dict is None:
                                    self.strmMeta = SchemaClasses.io.strmprivacy.schemas.demo.v1.StrmMetaClass()
                                    self.uniqueIdentifier = SchemaClasses.io.strmprivacy.schemas.demo.v1.DemoEventClass.RECORD_SCHEMA.fields[1].default
                                    self.consistentValue = str()
                                    self.someSensitiveValue = SchemaClasses.io.strmprivacy.schemas.demo.v1.DemoEventClass.RECORD_SCHEMA.fields[3].default
                                    self.notSensitiveValue = SchemaClasses.io.strmprivacy.schemas.demo.v1.DemoEventClass.RECORD_SCHEMA.fields[4].default
                            
                            
                            @property
                            def strmMeta(self):
                                """
                                :rtype: SchemaClasses.io.strmprivacy.schemas.demo.v1.StrmMetaClass
                                """
                                return self._inner_dict.get('strmMeta')
                            
                            @strmMeta.setter
                            def strmMeta(self, value):
                                #"""
                                #:param SchemaClasses.io.strmprivacy.schemas.demo.v1.StrmMetaClass value:
                                #"""
                                self._inner_dict['strmMeta'] = value
                            
                            
                            @property
                            def uniqueIdentifier(self):
                                """
                                :rtype: str
                                """
                                return self._inner_dict.get('uniqueIdentifier')
                            
                            @uniqueIdentifier.setter
                            def uniqueIdentifier(self, value):
                                #"""
                                #:param str value:
                                #"""
                                self._inner_dict['uniqueIdentifier'] = value
                            
                            
                            @property
                            def consistentValue(self):
                                """
                                :rtype: str
                                """
                                return self._inner_dict.get('consistentValue')
                            
                            @consistentValue.setter
                            def consistentValue(self, value):
                                #"""
                                #:param str value:
                                #"""
                                self._inner_dict['consistentValue'] = value
                            
                            
                            @property
                            def someSensitiveValue(self):
                                """
                                :rtype: str
                                """
                                return self._inner_dict.get('someSensitiveValue')
                            
                            @someSensitiveValue.setter
                            def someSensitiveValue(self, value):
                                #"""
                                #:param str value:
                                #"""
                                self._inner_dict['someSensitiveValue'] = value
                            
                            
                            @property
                            def notSensitiveValue(self):
                                """
                                :rtype: str
                                """
                                return self._inner_dict.get('notSensitiveValue')
                            
                            @notSensitiveValue.setter
                            def notSensitiveValue(self, value):
                                #"""
                                #:param str value:
                                #"""
                                self._inner_dict['notSensitiveValue'] = value
                            
                            
                        class StrmMetaClass(DictWrapper):
                            
                            """
                            
                            """
                            
                            
                            RECORD_SCHEMA = get_schema_type("io.strmprivacy.schemas.demo.v1.StrmMeta")
                            
                            
                            def __init__(self, inner_dict=None):
                                super(SchemaClasses.io.strmprivacy.schemas.demo.v1.StrmMetaClass, self).__init__(inner_dict)
                                if inner_dict is None:
                                    self.eventContractRef = str()
                                    self.nonce = SchemaClasses.io.strmprivacy.schemas.demo.v1.StrmMetaClass.RECORD_SCHEMA.fields[1].default
                                    self.timestamp = SchemaClasses.io.strmprivacy.schemas.demo.v1.StrmMetaClass.RECORD_SCHEMA.fields[2].default
                                    self.keyLink = SchemaClasses.io.strmprivacy.schemas.demo.v1.StrmMetaClass.RECORD_SCHEMA.fields[3].default
                                    self.billingId = SchemaClasses.io.strmprivacy.schemas.demo.v1.StrmMetaClass.RECORD_SCHEMA.fields[4].default
                                    self.consentLevels = list()
                            
                            
                            @property
                            def eventContractRef(self):
                                """
                                :rtype: str
                                """
                                return self._inner_dict.get('eventContractRef')
                            
                            @eventContractRef.setter
                            def eventContractRef(self, value):
                                #"""
                                #:param str value:
                                #"""
                                self._inner_dict['eventContractRef'] = value
                            
                            
                            @property
                            def nonce(self):
                                """
                                :rtype: int
                                """
                                return self._inner_dict.get('nonce')
                            
                            @nonce.setter
                            def nonce(self, value):
                                #"""
                                #:param int value:
                                #"""
                                self._inner_dict['nonce'] = value
                            
                            
                            @property
                            def timestamp(self):
                                """
                                :rtype: int
                                """
                                return self._inner_dict.get('timestamp')
                            
                            @timestamp.setter
                            def timestamp(self, value):
                                #"""
                                #:param int value:
                                #"""
                                self._inner_dict['timestamp'] = value
                            
                            
                            @property
                            def keyLink(self):
                                """
                                :rtype: str
                                """
                                return self._inner_dict.get('keyLink')
                            
                            @keyLink.setter
                            def keyLink(self, value):
                                #"""
                                #:param str value:
                                #"""
                                self._inner_dict['keyLink'] = value
                            
                            
                            @property
                            def billingId(self):
                                """
                                :rtype: str
                                """
                                return self._inner_dict.get('billingId')
                            
                            @billingId.setter
                            def billingId(self, value):
                                #"""
                                #:param str value:
                                #"""
                                self._inner_dict['billingId'] = value
                            
                            
                            @property
                            def consentLevels(self):
                                """
                                :rtype: list[int]
                                """
                                return self._inner_dict.get('consentLevels')
                            
                            @consentLevels.setter
                            def consentLevels(self, value):
                                #"""
                                #:param list[int] value:
                                #"""
                                self._inner_dict['consentLevels'] = value
                            
                            
                        pass
                        
__SCHEMA_TYPES = {
'io.strmprivacy.schemas.demo.v1.DemoEvent': SchemaClasses.io.strmprivacy.schemas.demo.v1.DemoEventClass,
    'io.strmprivacy.schemas.demo.v1.StrmMeta': SchemaClasses.io.strmprivacy.schemas.demo.v1.StrmMetaClass,
    
}
_json_converter = avrojson.AvroJsonConverter(use_logical_types=False, schema_types=__SCHEMA_TYPES)

# STRM Privacy additions

def get_strm_schema_ref(self) -> str:
    return "strmprivacy/demo/1.0.2"

def get_strm_schema_id(self) -> str:
    return "strmprivacy/demo/1.0.2"

def get_strm_schema(self):
    return self.RECORD_SCHEMA

def get_strm_schema_type(self):
    return "avro"

setattr(SchemaClasses.io.strmprivacy.schemas.demo.v1.DemoEventClass, "get_strm_schema_ref", get_strm_schema_ref)
setattr(SchemaClasses.io.strmprivacy.schemas.demo.v1.DemoEventClass, "get_strm_schema_id", get_strm_schema_id)
setattr(SchemaClasses.io.strmprivacy.schemas.demo.v1.DemoEventClass, "get_strm_schema", get_strm_schema)
setattr(SchemaClasses.io.strmprivacy.schemas.demo.v1.DemoEventClass, "get_strm_schema_type", get_strm_schema_type)
