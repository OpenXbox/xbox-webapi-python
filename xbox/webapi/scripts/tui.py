import urwid
import logging
import argparse

from xbox.webapi.authentication.manager import AuthenticationManager, AuthenticationException


class UrwidLogHandler(logging.Handler):
    def __init__(self, callback):
        super(UrwidLogHandler, self).__init__()
        self.callback = callback

    def emit(self, record):
        try:
            self.callback(record)
        except Exception:
            self.handleError(record)


class LogListBox(urwid.ListBox):
    def __init__(self, app, size=10000):
        self.app = app
        self.size = size
        self.entries = urwid.SimpleFocusListWalker([])

        self.handler = UrwidLogHandler(self._log_callback)
        self.handler.setFormatter(app.log_fmt)
        logging.root.addHandler(self.handler)
        logging.root.setLevel(app.log_level)
        super(LogListBox, self).__init__(self.entries)

    def _log_callback(self, record):
        self.entries.append(LogButton(self.app, self.handler.format(record), record))
        if self.focus_position == len(self.entries) - 2:
            self.focus_position += 1

        if len(self.entries) > self.size:
            self.entries[:] = self.entries[len(self.entries) - self.size:]

    def keypress(self, size, key):
        # Prevents opening the log window multiple times
        if key in ('l', 'L'):
            pass
        else:
            return super(LogListBox, self).keypress(size, key)


class LogButton(urwid.Button):
    focus_map = {
        None: 'selected',
    }

    def __init__(self, app, text, record):
        super(LogButton, self).__init__('')
        self.app = app
        self.text = text
        self.record = record

        self.textwidget = urwid.AttrWrap(urwid.SelectableIcon(' {}'.format(self.text), cursor_position=0), None)
        self._w = urwid.AttrMap(self.textwidget, None, self.focus_map)


class WebAPIDisplay(object):
    palette = [
        ('bg', 'white', 'dark gray'),
        ('header', 'yellow', 'dark blue', 'standout'),

        # footer
        ('foot', 'dark cyan', 'dark blue', 'bold'),
        ('key', 'light cyan', 'dark blue', 'underline'),
    ]

    header_text = ('header', [
        "Xbox WebAPI"
    ])

    footer_main_text = ('foot', [
        ('key', 'L:'), "view log ",
        ('key', 'Q:'), "quit  "
    ])

    footer_log_text = ('foot', [
        ('key', 'Q:'), "quit "
    ])

    log_fmt = logging.Formatter(logging.BASIC_FORMAT)
    log_level = logging.DEBUG

    def __init__(self, tokenfile_path):
        self.tokenfile_path = tokenfile_path

        self.auth_mgr = AuthenticationManager()

        self.loop = None
        self.log = LogListBox(self)

        self.view_stack = []

        try:
            self.auth_mgr.load_tokens_from_file(self.tokenfile_path)
        except Exception as e:
            logging.debug('Tokens failed to load from file, Error: {}'.format(e))

        '''
        self.need_refresh = self.auth_mgr.refresh_token and \
            self.auth_mgr.refresh_token.is_valid and \
            self.auth_mgr.refresh_token.date_valid < (datetime.now(tzutc()) + timedelta(days=7))
        '''
        self.need_full_auth = not self.auth_mgr.refresh_token or not self.auth_mgr.refresh_token.is_valid

    def push_view(self, sender, view):
        self.view_stack.append(view)
        self.loop.widget = view
        self.loop.draw_screen()

    def pop_view(self, sender):
        if len(self.view_stack) > 1:
            top_widget = self.view_stack.pop()
            if hasattr(top_widget, 'close_view'):
                top_widget.close_view(sender)

            self.loop.widget = self.view_stack[-1]
            self.loop.draw_screen()
        else:
            self.do_quit()

    def view_main(self):
        if self.need_full_auth:
            self.view_authentication_menu()
        # elif self.need_refresh:
        #    self._authenticate(status_text='Refreshing tokens...\n')
        else:
            self._authenticate()

    def _authenticate(self, email=None, password=None, status_text='Authenticating...\n'):
        self.auth_mgr.email_address = email
        self.auth_mgr.password = password
        try:
            self.view_msgbox(status_text, 'Please wait', show_button=False)
            self.auth_mgr.authenticate(do_refresh=True)  # do_refresh=self.need_refresh
            self.view_msgbox('Authentication was successful, tokens saved!\n', 'Success')

        except AuthenticationException as e:
            logging.debug('Authentication failed, Error: {}'.format(e))
            self.view_msgbox('Authentication failed!\n{}\n'.format(e), 'Error')

        return self.auth_mgr.is_authenticated

    def _on_button_press(self, button, user_arg=None):
        label = button.get_label()
        if 'Authenticate' == label:
            email, pwd = (t.get_edit_text() for t in user_arg)
            self._authenticate(email, pwd)
        else:
            raise urwid.ExitMainLoop()

    def _view_menu(self, elements):
        header = urwid.AttrMap(urwid.Text(self.header_text), 'header')
        footer = urwid.AttrMap(urwid.Text(self.footer_main_text), 'foot')

        assert isinstance(elements, list)
        pile = urwid.Pile(elements)

        p = urwid.AttrWrap(pile, 'bg')
        padded = urwid.Padding(p, 'center', ('relative', 80))
        filler = urwid.Filler(padded)
        frame = urwid.Frame(filler, header=header, footer=footer)
        self.push_view(self, frame)

    def view_authentication_menu(self):
        info_label = urwid.Text(
            'Please authenticate with your Microsoft Account\n', align='center'
        )
        div = urwid.Divider()
        email_text = urwid.Edit('Email Address: ', align='center')
        password_text = urwid.Edit('Account Password: ', align='center', mask='*')
        authenticate_button = urwid.Button('Authenticate')
        cancel_button = urwid.Button('Cancel')
        pile = urwid.Pile(
            [info_label, div, email_text, div, password_text, div, authenticate_button, cancel_button]
        )
        box = urwid.LineBox(pile, title='Authentication required')

        urwid.connect_signal(authenticate_button, 'click', self._on_button_press,
                             user_arg=[email_text, password_text])
        urwid.connect_signal(cancel_button, 'click', self._on_button_press)

        self._view_menu([box])

    def view_msgbox(self, msg, title, show_button=True):
        text = urwid.Text(msg, align='center')

        if show_button:
            button = urwid.Button('OK')
            pad_button = urwid.Padding(button, 'center', ('relative', 10))
            pile = urwid.Pile([text, pad_button])
            box = urwid.LineBox(pile, title)

            # Clicking OK exits UI
            urwid.connect_signal(button, 'click', self._on_button_press)
        else:
            box = urwid.LineBox(text, title)

        self._view_menu([box])

    def view_log(self):
        header = urwid.AttrMap(urwid.Text(self.header_text), 'header')
        footer = urwid.AttrMap(urwid.Text(self.footer_log_text), 'foot')
        frame = urwid.Frame(self.log, header=header, footer=footer)
        self.push_view(self, frame)

    def return_to_main_menu(self):
        while len(self.view_stack) > 1:
            self.pop_view(self)

    def do_quit(self):
        raise urwid.ExitMainLoop()

    def run(self):
        self.loop = urwid.MainLoop(
            urwid.SolidFill('x'),
            handle_mouse=False,
            palette=self.palette,
            unhandled_input=self.unhandled_input
        )

        self.loop.set_alarm_in(0.0001, lambda *args: self.view_main())
        self.loop.run()
        return self.auth_mgr.is_authenticated

    def unhandled_input(self, input):
        if input in ('q', 'Q'):
            self.pop_view(self)
        elif input in ('l', 'L'):
            self.view_log()


def main():
    parser = argparse.ArgumentParser(description="Basic text user interface")
    parser.add_argument('--tokens', '-t', default='tokens.json',
                        help="Token file, created by xbox-authenticate script")
    args = parser.parse_args()

    ui = WebAPIDisplay(args.tokens)
    ui.run()

if __name__ == '__main__':
    main()
