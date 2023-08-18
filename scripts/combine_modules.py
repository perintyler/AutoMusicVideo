"""combine_modules.py

A python script for combining python modules into a single file. This code is a modified 
version of a script taken from: https://stackoverflow.com/a/76906690
"""

import os
import sys
import re
import argparse

def combine_python_modules(filename, depth = 0):
  with open(filename, "r") as python_module:
    combined_source_code = python_module.read()

  if depth != 0:
    combined_source_code = combined_source_code.replace(
      "if __name__ == '__main__':", 
      "if __name__ == '__main__' and False:"
    )

  import_statement_pattern = "from (\w+) import (.+)\n"
  matched_imports = re.findall(import_statement_pattern, combined_source_code)
  
  for imported_module, imported_property in matched_imports:
    path_to_module = imported_module + ".py"
    if os.path.exists(path_to_module):
      import_statement = import_statement_pattern \
                        .replace("(\\w+)", imported_module) \
                        .replace("(.+)", imported_property)
      module_source_code = combine_python_modules(path_to_module, depth + 1)
      combined_source_code = combined_source_code.replace(import_statement, module_source_code)

  return combined_source_code

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--main-module', required=True)
  parser.add_argument('--outfile', required=True)
  args = parser.parse_args()

  with open(args.outfile, "w") as combined_python_module:
    combined_source_code = combine_python_modules(args.main_module)
    combined_python_module.write(combined_source_code)
