"""generate_notebook.py"""

import re
import os
from datetime import datetime
import nbformat

def unify_source_code(filename, depth = 0):
  """returns the source code for a single file module containing the combined
  source code of all imported modules
  """
  with open(filename, "r") as python_module:
    combined_source_code = python_module.read()

  if depth != 0:
    # hacky way to make sure every module's main function doesn't get run
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
      module_source_code = unify_source_code(path_to_module, depth + 1)
      combined_source_code = combined_source_code.replace(import_statement, module_source_code)

  return combined_source_code

def get_pip_installation_command():
  with open('requirements.txt') as requirements_file:
    requirements_file_contents = requirements_file.read()
  requirements = requirements_file_contents.strip().split('\n')

  upgrade_pip_command = f"{PIP} install --upgrade pip"
  install_requirements_command = f"{PIP} install {' '.join(requirements)} -y"

  pip_installation_command = f'{upgrade_pip_command} && {install_requirements_command}'

  return f'!{pip_installation_command}' if JUPITER_NOTEBOOK else pip_installation_command

def create_notebook():
  notebook = nbformat.v4.new_notebook()
  formatted_timestamp = datetime.now().strftime('%m-%d-%y_%H-%M-%S')
  notebook_name = f'AutoMusicVideo {formatted_timestamp}'
  text_header = f'# {notebook_name}'

  source_code = unify_source_code('main.py')
  jupiter_code = f'%pylab inline\n{source_code}'

  notebook['cells'] = [
    nbformat.v4.new_markdown_cell(text_header),
    nbformat.v4.new_code_cell(jupiter_code)
  ]

  # filename = f"./{notebook_name.replace(' ', '_').replace('/', '-').replace(':', '-')}.ipynb"
  filename = f"./{notebook_name}.ipynb"
  nbformat.write(notebook, filename)

if __name__ == '__main__':
  create_notebook('../storyboard/storybook/main.py')
