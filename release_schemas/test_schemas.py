"""
Validate each release schema and its examples.

Test all schemas and their related example files for validity.
ref: https://github.com/Julian/jsonschema
"""
import json
from os import listdir
from os.path import abspath, basename, dirname, isdir, isfile, join
import sys

import jsonschema

_CURRENT_DIR = dirname(abspath(__file__))
SCHEMA_FILENAME = 'release-schema.json'
SCHEMA_EXAMPLES_DIR = 'release-example-files'

# print functions
#
def msg(m): print(m)
def dashes(): msg('-' * 40)
def msgt(m): dashes(); print(m); dashes()
def msg_err(m): msg(f'ERROR!\n{m}'); dashes(); sys.exit(-1)

def validate_schemas_examples():
    """Read through each schema directory"""
    msgt('Validate Schemas')
    # Gather directories
    schema_dirs = [join(_CURRENT_DIR, x) \
                   for x in listdir(_CURRENT_DIR) \
                   if x.startswith('version-')]
    
    # Iterate through directories
    #
    cnt = 0 
    for schema_dir in schema_dirs:
        cnt += 1
        msgt(f'({cnt}) Checking schema: {schema_dir}')
        schema_file = join(schema_dir, SCHEMA_FILENAME)
        if not (isdir(schema_dir) and isfile(schema_file)):
            msg_err(f'Schema file not found: {schema_file}')
        
        # (1) Open the schema file
        #
        with open(schema_file, 'r') as ye_schema:
            try:
                report_schema = json.load(ye_schema)
            except json.JSONDecodeError as err_obj:
                msg_err(f'File not valid JSON: {schema_file}. {err_obj}')
            
            validate_examples(report_schema, schema_dir, schema_cnt=cnt)

def validate_examples(report_schema, schema_dir, schema_cnt=None):
    """Iterate through the schema examples in the 'schema_dir',
       validating each one"""     
    examples_dir = join(schema_dir, SCHEMA_EXAMPLES_DIR)
    example_files = [join(examples_dir, x) 
                        for x in listdir(examples_dir) 
                        if x.lower().endswith('.json')]

    rcnt = 0
    for report_example in example_files:
        rcnt += 1
        msg(f'\n({schema_cnt}-{rcnt}) validate report:\n{report_example}')
        if not isfile(report_example):
            continue
        with open(report_example, 'r') as report_file:
            try:
                report_data = json.load(report_file)
            except json.decoder.JSONDecodeError as err_obj:
                msg_err(f'Example file is not valid JSON: {report_example}.\n{err_obj}')

        try:
            jsonschema.validate(instance=report_data, schema=report_schema)
            msg('> VALID!')
        except jsonschema.ValidationError as err_obj:
            msg_err(f'> FAILED to validate JSON report: {report_example}.\n{err_obj}')


#    return validate(instance=instance, schema=schema)


if __name__ == '__main__':
    validate_schemas_examples()
 
 