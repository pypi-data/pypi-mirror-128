import urwid

from ui.commands import check_command

palette = [('I say', 'default,bold', 'default', 'bold')]

command = urwid.Edit(('I say', u"Command:\n"))
reply = urwid.Text(u"")
essential_help = urwid.Text(u'Press q to quit, h for help.')
version_info = urwid.Text(u'architools v. 0.0.1')

div = urwid.Divider()
pile = urwid.Pile([command, div, reply, div, essential_help, version_info])
top = urwid.Filler(pile, valign='top')

def on_command_change(edit, new_edit_text):
  # trigger command lookup on space
  if u' ' in new_edit_text:
    trigger_command()

def handle_extra_input(input):
  # trigger commands on enter and tab
  if input in ['enter', 'tab']:
    trigger_command()

def trigger_command():
  cmd = command.get_edit_text()
  msg = check_command(cmd)
  reply.set_text(msg)
  command.set_edit_text(u'')


urwid.connect_signal(command, 'change', on_command_change)
#urwid.connect_signal(button, 'click', on_exit_clicked)

urwid.MainLoop(top, palette, unhandled_input=handle_extra_input).run()
