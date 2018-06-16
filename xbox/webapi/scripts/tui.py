import urwid
import logging
import argparse

from xbox.webapi.authentication.manager import AuthenticationManager
from xbox.webapi.authentication.two_factor import TwoFactorAuthentication, TwoFactorAuthMethods
from xbox.webapi.common.exceptions import TwoFactorAuthRequired, AuthenticationException
from xbox.webapi.scripts import TOKENS_FILE


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


class TabSwitchingPile(urwid.Pile):
    def keypress(self, size, key):
        if key == 'tab':
            pos = self.focus_position + 1
            while pos != self.focus_position:
                if pos >= len(self.contents):
                    pos = 0
                widget, _ = self.contents[pos]
                if widget.base_widget.selectable():
                    self.focus_position = pos
                    return
                pos += 1
        else:
            return super(TabSwitchingPile, self).keypress(size, key)


class SelectableListBox(urwid.ListBox):
    def __init__(self, body, callback):
        super(SelectableListBox, self).__init__(body)
        self.callback = callback

    def keypress(self, size, key):
        if key == 'enter':
            self.callback(self.focus_position)
        else:
            return super(SelectableListBox, self).keypress(size, key)


class QuestionBox(urwid.Edit):
    def __init__(self, callback, **kwargs):
        super(QuestionBox, self).__init__(**kwargs)
        self.callback = callback

    def keypress(self, size, key):
        if key != 'enter':
            return super(QuestionBox, self).keypress(size, key)
        else:
            self.callback(self.edit_text)


class WebAPIDisplay(object):
    focus_map = {
        None: 'selected'
    }

    palette = [
        ('bg', 'white', 'dark gray'),
        ('header', 'yellow', 'dark blue', 'standout'),

        # footer
        ('foot', 'dark cyan', 'dark blue', 'bold'),
        ('key', 'light cyan', 'dark blue', 'underline')
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
        self.two_factor_auth = None

        # 2FA cache
        self.index = None
        self.proof = None
        self.otc = None

        self.loop = None
        self.log = LogListBox(self)

        self.view_stack = []

        try:
            self.auth_mgr.load(self.tokenfile_path)
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

    def _input_prompt(self, prompt, callback, entries=None):
        if entries:
            list_entries = [
                urwid.AttrWrap(urwid.SelectableIcon(e, cursor_position=0), None) for e in entries
            ]
            walker = urwid.SimpleFocusListWalker([urwid.AttrMap(e, None, self.focus_map) for e in list_entries])
            listbox = SelectableListBox(walker, callback)
            view = urwid.BoxAdapter(listbox, height=len(entries))
        else:
            edit_text = QuestionBox(callback, align='left')
            view = urwid.AttrMap(edit_text, None, self.focus_map)

        box = urwid.LineBox(view, title=prompt)
        self._view_menu([box])

    def view_main(self):
        if self.need_full_auth:
            self.view_authentication_menu()
        # elif self.need_refresh:
        #    self._authenticate(status_text='Refreshing tokens...\n')
        else:
            self._authenticate()

    def _two_factor_finish_auth(self, otc):
        self.otc = otc
        self.view_msgbox('Waiting for 2FA to complete', 'Please wait')

        access_token, refresh_token = None, None
        try:
            access_token, refresh_token = self.two_factor_auth.authenticate(
                self.index, self.proof, self.otc
            )
        except AuthenticationException as e:
            logging.debug('2FA Authentication failed, Error: {}'.format(e))
            self.view_msgbox('2FA Authentication failed!\n{}\n'.format(e), 'Error',
                             show_quit_button=True)

        self.auth_mgr.access_token = access_token
        self.auth_mgr.refresh_token = refresh_token
        self._authenticate()

    def _two_factor_auth_ask_otc(self, proof):
        self.proof = proof
        need_otc = self.two_factor_auth.check_otc(self.index, proof)
        if need_otc:
            self._input_prompt('Enter One-Time-Code (OTC)', self._two_factor_finish_auth)
        else:
            self._two_factor_finish_auth(None)

    def _two_factor_auth_verify_proof(self, index):
        self.index = index
        verification_prompt = self.two_factor_auth.get_method_verification_prompt(index)
        if verification_prompt:
            self._input_prompt(verification_prompt, self._two_factor_auth_ask_otc)
        else:
            self._two_factor_auth_ask_otc(None)

    def view_two_factor_auth(self, server_data):
        self.two_factor_auth = TwoFactorAuthentication(
            self.auth_mgr.session, self.auth_mgr.email_address, server_data
        )
        entries = ['{!s}, Name: {}'.format(
            TwoFactorAuthMethods(strategy.get('type', 0)), strategy.get('display'))
            for strategy in self.two_factor_auth.auth_strategies
        ]
        self._input_prompt('Choose desired auth method', self._two_factor_auth_verify_proof, entries)

    def _authenticate(self, email=None, password=None, status_text='Authenticating...\n'):
        self.auth_mgr.email_address = email
        self.auth_mgr.password = password
        try:
            self.view_msgbox(status_text, 'Please wait')
            self.auth_mgr.authenticate(do_refresh=True)  # do_refresh=self.need_refresh
            self.auth_mgr.dump(self.tokenfile_path)
            do_show_quit_button = True
            if not self.need_full_auth:
                # If authentication was done from tokens, auto close on success
                do_show_quit_button = False
                self.loop.set_alarm_in(2.0, lambda *args: self.do_quit())
            self.view_msgbox('Authentication was successful!\n', 'Success',
                             show_quit_button=do_show_quit_button)

        except TwoFactorAuthRequired as e:
            self.view_two_factor_auth(e.server_data)

        except AuthenticationException as e:
            logging.debug('Authentication failed, Error: {}'.format(e))
            self.view_msgbox('Authentication failed!\n{}\n'.format(e), 'Error',
                             show_quit_button=True)

    def _on_button_press(self, button, user_arg=None):
        label = button.get_label()
        if 'Authenticate' == label:
            email, pwd = (t.get_edit_text() for t in user_arg)
            self._authenticate(email, pwd)
        elif 'Quit' == label or 'Cancel' == label:
            self.do_quit()
        else:
            raise ValueError('tui: Unexpected button pressed: {}'.format(label))

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
        email_text = urwid.AttrMap(urwid.Edit('Email Address: '), None, self.focus_map)
        password_text = urwid.AttrMap(urwid.Edit('Account Password: ', mask='*'), None, self.focus_map)

        authenticate_button = urwid.Button('Authenticate')
        authenticate_button._label.align = 'center'
        authenticate_button = urwid.AttrMap(authenticate_button, None, self.focus_map)

        cancel_button = urwid.Button('Cancel')
        cancel_button._label.align = 'center'
        cancel_button = urwid.AttrMap(cancel_button, None, self.focus_map)

        authenticate_button = urwid.Padding(authenticate_button, align='center', width=('relative', 30))
        cancel_button = urwid.Padding(cancel_button, align='center', width=('relative', 23))

        pile = TabSwitchingPile(
            [info_label, div, email_text, div, password_text, div, authenticate_button, cancel_button]
        )
        box = urwid.LineBox(pile, title='Authentication required')

        urwid.connect_signal(authenticate_button.base_widget, 'click', self._on_button_press,
                             user_arg=[email_text.base_widget, password_text.base_widget])
        urwid.connect_signal(cancel_button.base_widget, 'click', self._on_button_press)

        self._view_menu([box])

    def view_msgbox(self, msg, title, show_quit_button=False):
        text = urwid.Text(msg, align='center')

        if show_quit_button:
            button = urwid.Button('Quit')
            button._label.align = 'center'
            button = urwid.AttrMap(button, None, self.focus_map)
            pad_button = urwid.Padding(button, 'center', ('relative', 10))
            pile = urwid.Pile([text, pad_button])
            box = urwid.LineBox(pile, title)

            # Clicking OK exits UI
            urwid.connect_signal(button.base_widget, 'click', self._on_button_press)
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
            self.do_quit()
        elif input in ('l', 'L'):
            self.view_log()


def main():
    parser = argparse.ArgumentParser(description="Basic text user interface")
    parser.add_argument('--tokens', '-t', default=TOKENS_FILE,
                        help="Token filepath, file gets created if nonexistent and auth is successful."
                             " Default: {}".format(TOKENS_FILE))
    args = parser.parse_args()

    ui = WebAPIDisplay(args.tokens)
    ui.run()


if __name__ == '__main__':
    main()
