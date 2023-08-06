import random

def random_color():
  r = lambda: random.randint(0,255)
  hex_string = '#%02X%02X%02X' % (r(),r(),r())
  return hex_string
