"""get_pip_oneliner.py

prints out a one line `pip install` command that includes all the 
dependencies from 'requirements.txt'
"""

PIP = 'pip'

JUPITER_NOTEBOOK = True

def get_pip_command():
  with open('requirements.txt') as requirements_file:
    requirements_file_contents = requirements_file.read()
  requirements = requirements_file_contents.strip().split('\n')

  upgrade_pip_command = f"{PIP} install --upgrade pip"
  install_requirements_command = f"{PIP} install {' '.join(requirements)} -y"

  pip_installation_command = f'{upgrade_pip_command} && {install_requirements_command}'

  return f'!{pip_installation_command}' if JUPITER_NOTEBOOK else pip_installation_command

if __name__ == '__main__':
  print(get_pip_command())

