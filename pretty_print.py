"""pretty_print.py"""

def print_header(title):
  title = ' '.join(word.title() for word in title.split(' '))
  header = f'<><><> {title} <><><>'
  indent = ' '*int((128 - len(header))/2 + 1)
  headerDivider = '-'*128
  print(f"\n{headerDivider}\n{indent}{header}\n{headerDivider}\n")

def print_divider():
  print('\n')
  print('-'*128)
  print('/'*64 + '\\'*64)
  print('\\'*64 + '/'*64)
  print('-'*128)
  print('')

def print_bullet(message):
  print (f'    - {message}')
  