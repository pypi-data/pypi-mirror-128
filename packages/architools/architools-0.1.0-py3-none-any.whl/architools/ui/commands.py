import urwid
from ui.state import state
# from ui.viewer import start_occ_display

def notfound():
  return 'COMMAND NOT FOUND'

def terminate():
  raise urwid.ExitMainLoop()

def show_help():
  return 'HELP NOT IMPLEMENTED YET'

def start_display():
  # start_occ_display()
  return 'DISPLAY NOT IMPLEMENTED'

def stop_display():
  return 'DISPLAY NOT IMPLEMENTED'

registered_commands = {
  'q': terminate,
  'showhelp': show_help,
  'h': show_help,
  'd': start_display,
  'sd': stop_display,
}

def check_command(cmd, args=[]):
  cmd_handler = registered_commands.get(cmd, notfound)
  msg = cmd_handler(*args)
  return msg
