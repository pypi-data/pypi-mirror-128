import json
import os
import sys
from os.path import join, isfile, dirname

import avrogen

global top_package


def load_schema_definition():
    f = join(dirname(__file__), "schema", "schema.avsc")
    schema_contents = open(f, 'r').read()
    avro_schema = avrogen.schema.make_avsc_object(json.loads(schema_contents))

    global top_package
    top_package = f"strmprivacy_{avro_schema.namespace.replace('.', '_')}"

    return schema_contents, avro_schema


def create_schema_code():
    schema_contents, avro_schema = load_schema_definition()

    os.makedirs(top_package, exist_ok=True)
    if isfile(join(top_package, "schema_classes.py")):
        print("Already created schema_classes.py")
        sys.exit(1)

    with open(join(top_package, 'schema.avsc'), 'w') as _f:
        _f.write(schema_contents)
    avrogen.write_schema_files(schema_contents, top_package)

    classname = f"SchemaClasses.{avro_schema.fullname}Class"

    with open(join(top_package, "schema_classes.py"), "a") as _f:
        _f.write(f"""# STRM Privacy additions

def get_strm_schema_ref(self) -> str:
    return "strmprivacy/demo/1.0.2"

def get_strm_schema_id(self) -> str:
    return "strmprivacy/demo/1.0.2"

def get_strm_schema(self):
    return self.RECORD_SCHEMA

def get_strm_schema_type(self):
    return "avro"

setattr({classname}, "get_strm_schema_ref", get_strm_schema_ref)
setattr({classname}, "get_strm_schema_id", get_strm_schema_id)
setattr({classname}, "get_strm_schema", get_strm_schema)
setattr({classname}, "get_strm_schema_type", get_strm_schema_type)
""")

    with open('MANIFEST.in', 'w') as manifest:
        manifest.write(f"""recursive-include {top_package} *
include top_package * """)

    with open('top_package', 'w') as t:
        t.write(top_package)

def clean():
    import shutil

    load_schema_definition()
    try:
        print("removing directory", top_package)
        shutil.rmtree(top_package)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage {sys.argv[0]} build|clean")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "build":
        create_schema_code()
    elif cmd == "clean":
        clean()
