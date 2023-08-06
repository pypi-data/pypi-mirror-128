import logging

from datetime import datetime
import random

import tkinter as tk
from . import MODULES_VERBOSE
from . import RootWindow, FrameUnlabelled, FrameLabelled, FrameStateful, Notebook, NotebookUniform
from . import Button, Checkbox, Entry, Label, Listbox, Combobox, ComboboxMap, EntryMultiline, Tree
from . import var, spec
from .model import CP, BindingGlobal, Timeout, TimeoutIdle


logger = logging.getLogger(__name__)


class LuftBaloons(FrameUnlabelled):
    layout = 'xE'

    def setup_widgets(self, howmany=16 - 3):
        widgets = {}
        for widx in range(howmany):
            idx = 'lb:%d' % widx
            widget = Checkbox(self, label='%02d' % widx)
            widget.trace(self.onClick_lb, idx=idx)
            widgets[idx] = widget
        return widgets

    def onClick_lb(self, vobj, etype, *, idx):
        pass
        # logger.debug('Clicked on "%s" @ %s:%s', idx, vobj, etype)
        # logger.debug('- State: %r', vobj.get())


class ListFrame_Inner(FrameStateful):
    def __init__(self, *args, label, **kwargs):
        super().__init__(*args, label=label, labelInner=label, **kwargs)

    def setup_widgets(self, labelInner):
        self.lbl = Label(self, label=f'Label: {labelInner}')
        self.e = Entry(self)  # label=f'Entry: {labelInner}'


class ListFrame_Outer(FrameStateful):
    label = 'Outer Frame'
    layout = 'R2,1'

    def setup_widgets(self, *, cbox1):
        self.left = ListFrame_Inner(self, label='Left', cvariableDefault=True)
        self.right = ListFrame_Inner(self, label='Right', cvariableDefault=False)
        self.bottom = ListFrame_Inner(self, label='Bottom',
                                      cvariable=cbox1)


class ListFrame(FrameLabelled):
    layout = 'R2,1,1,1,1,1'

    def setup_widgets(self, *, cbox1):
        i_choices: spec.StaticMap[int] = spec.StaticMapValues(lambda i: 'I%d' % i, range(10), defaultValue=7)

        self.bFill = Button(self, label='Fill Me!')
        self.bCheck = Button(self, label='Check')

        vLst = var.StringList(name='lst')  # Alternative: self.var(var.StringList, name='lst')
        self.lstS = Listbox(self,
                            variable=vLst,
                            selectable=True)  # Selectable
        self.lstRO = Listbox(self, label='Unselectable',
                             maxHeight=3, expand=True,  # Varying Height, Expanded
                             variable=vLst,
                             selectable=False,
                             style=Listbox.Style(altbg=True),
                             )  # Not Selectable

        self.bChoice = Button(self, label='CB=2')
        self.i_choice = ComboboxMap(self, values=i_choices)  # label='CB(int)'

        self.rstateful = ListFrame_Outer(self, labelAnchor=CP.N,
                                         cbox1=cbox1)

    def setup_layout(self, layout):
        self.rowconfigure(self.lstS.grid_info().get('row'), weight=0)

    def setup_defaults(self):
        self.fill_lst()
        # Events
        self.bFill.onClick = self.fill_lst
        self.bCheck.onClick = self.check_lst
        self.bChoice.onClick = self.i_choice.eSetValue(2)

        self.i_choice.trace(self.onChosen, spec=self.i_choice.specValues)

        BindingGlobal(self.bChoice, '<F1>', self.globalHelp,
                      immediate=True, description='Nothing, just showing the event object')

    def setup_adefaults(self):
        # Why not verify some invariants?
        assert self.wroot_search() == self.wroot, 'Invalid Root calculation'

    def fill_lst(self):
        ctime = str(datetime.now())
        self.lstS.wstate = ['A', 'List', 'Of', 'Letters', '@', ctime]

    def check_lst(self):
        sel = self.lstS.wselection()
        logger.debug('S: %r', sel)

    def onChosen(self, variable, etype, *, spec):
        logger.debug('V: %r', variable)
        label = variable.get()
        logger.debug('   Label: %s[%r]', label, spec.value(label))

    def globalHelp(self, event=None):
        if event:
            logger.debug('Event: %r', event)


class UpstreamBool(FrameLabelled):
    layout = 'x1N'  # Bottom-Up
    # Comment the following line to change the state
    isNoneable = False  # Don't skip this widget, even when its state is `None`

    def setup_widgets(self, what_bool):
        self.bNoOp = Button(self, label='noop')
        self.u_bool = Checkbox(self, variable=what_bool, label='Upstream "bool"')
        self.bNoOp_Big = Button(self, label='No Operation')


class NB_Child_Simple(FrameUnlabelled):
    layout = 'Rx,1'

    def setup_widgets(self, label):
        w = {}
        for n in range(5):
            w[f'n{n}'] = Label(self, label=f'{n}: {label}')
        w['e'] = Entry(self)  # label=f'Entry #{n}'
        return w


class NB_Child_Complex(NotebookUniform):
    tabids = {f'TC{d}': f'Tab Complex {d}' for d in range(5)}

    def setup_tab(self, tid: str, tname: str):
        return NB_Child_Simple(self, label=tid)


class NB_Child_Timeout(FrameLabelled):
    label = 'Timeout'

    def __init__(self, *args, **kwargs):
        self.t = Timeout(self, self.onTimeout, 1000, immediate=False)
        super().__init__(*args, **kwargs)

    def setup_widgets(self):
        self.cScheduled = Checkbox(self, label='Scheduled?', readonly=True)
        self.cTriggered = Checkbox(self, label='Triggered?', readonly=True)
        self.bToggle = Button(self, label='Toggle\nasync')

        self.bToggle.onClick = self.onToggle

    def setup_defaults(self):
        self.update()

    def update(self):
        self.cScheduled.wstate = self.t.isScheduled()
        self.cTriggered.wstate = self.t.isTriggered()

    def onToggle(self):
        self.t.toggle()
        self.update()

    def onTimeout(self):
        logger.debug('Timeout!')
        self.update()


class NB_Child_Timeout_Delay(FrameLabelled):
    label = 'Timeout (Delayed)'

    def __init__(self, *args, **kwargs):
        self.t = Timeout(self, self.onTimeout, 1000, immediate=False)
        super().__init__(*args, **kwargs)

    def setup_widgets(self):
        self.cScheduled = Checkbox(self, label='Scheduled?', readonly=True)
        self.cTriggered = Checkbox(self, label='Triggered?', readonly=True)
        self.bToggle = Button(self, label='  Toggle\nasync-ish')

        self.bToggle.onClick = self.onToggle

    def setup_defaults(self):
        self.update()

    def update(self):
        self.cScheduled.wstate = self.t.isScheduled()
        self.cTriggered.wstate = self.t.isTriggered()

    def onToggle(self):
        self.t.toggle()
        self.update()

    def onTimeout(self):
        logger.debug('Timeout!')
        self.update()
        logger.debug('Delay ...')
        self.after(1000)
        logger.debug('... Done!')


class NB_Child_TimeoutIdle_Delay(FrameLabelled):
    label = 'TimeoutIdle (Delayed)'

    def __init__(self, *args, **kwargs):
        self.t = TimeoutIdle(self, self.onTimeout, immediate=False)
        self.tsleep = TimeoutIdle(self, lambda: self.after(1000), immediate=False)  # Pretend this is a long calculation
        super().__init__(*args, **kwargs)

    def setup_widgets(self):
        self.cScheduled = Checkbox(self, label='Scheduled?', readonly=True)
        self.cTriggered = Checkbox(self, label='Triggered?', readonly=True)
        self.bToggle = Button(self, label='Toggle\n sync')

        self.bToggle.onClick = self.onToggle

    def setup_defaults(self):
        self.update()

    def update(self):
        self.cScheduled.wstate = self.t.isScheduled()
        self.cTriggered.wstate = self.t.isTriggered()

    def onToggle(self):
        ts = [self.tsleep, self.t]
        # (un)schedule both timeouts in tandem
        if self.t.isScheduled():
            for t in ts:
                t.unschedule()
        else:
            for t in ts:
                t.schedule()
        self.update()

    def onTimeout(self):
        logger.debug('TimeoutIdle!')
        self.update()


class NB_Child_TimeoutIdle_Chain(FrameLabelled):
    label = 'TimeoutIdle (Chained)'

    def __init__(self, *args, **kwargs):
        self.tsleep = TimeoutIdle(self, self.onTimeoutSleep, immediate=False)
        self.t = TimeoutIdle(self, self.onTimeout, immediate=False)
        super().__init__(*args, **kwargs)

    def setup_widgets(self):
        self.cScheduled = Checkbox(self, label='Scheduled?', readonly=True)
        self.cTriggered = Checkbox(self, label='Triggered?', readonly=True)
        self.bToggle = Button(self, label='Toggle\n sync')

        self.bToggle.onClick = self.onToggle

    def setup_defaults(self):
        self.update()

    def update(self):
        self.cScheduled.wstate = self.t.isScheduled()
        self.cTriggered.wstate = self.t.isTriggered()

    def onToggle(self):
        ts = [self.tsleep, self.t]
        # (un)schedule both timeouts in tandem
        if self.t.isScheduled():
            for t in ts:
                t.unschedule()
        else:
            for t in ts:
                t.schedule()
        self.update()

    def onTimeoutSleep(self):
        logger.debug('Chain Delay ...')
        self.after(1000)
        logger.debug('... Done!')
        self.t.schedule()
        self.update()

    def onTimeout(self):
        logger.debug('TimeoutIdle!')
        self.update()


class NB_Child_Timeouts(FrameUnlabelled):
    # layout = tk.HORIZONTAL

    def setup_widgets(self):
        self.timeout = NB_Child_Timeout(self)
        self.timeout_d = NB_Child_Timeout_Delay(self)
        self.timeout_idle_d = NB_Child_TimeoutIdle_Delay(self)
        self.timeout_idle_c = NB_Child_TimeoutIdle_Chain(self)


class NB(Notebook):
    def setup_tabs(self):
        logger.debug('» %r', self)
        # TODO: Test images, etc.
        return {
            'tt': Notebook.Tab('Timeouts', NB_Child_Timeouts(self)),
            'tc': Notebook.Tab('Tab Complex', NB_Child_Complex(self)),
            't1': Notebook.Tab('Tab 1', NB_Child_Simple(self, label='Tab 1')),
            't2': Notebook.Tab('Tab 2', NB_Child_Simple(self, label='Tab 2')),
        }


class TextEditor(FrameStateful):
    label = 'LTML'
    layout = 'Rx,1'

    def setup_widgets(self):
        self.bTxtClean = Button(self, label='Clean TXT')
        self.bTxtReset = Button(self, label='Reset TXT')
        self.bTxtSet = Button(self, label='Set TXT')
        self.txt = EntryMultiline(self, setgrid=False)
        # Setup events
        self.bTxtClean.onClick = self.txt.style_reset
        self.bTxtReset.onClick = self.txt_reset
        self.bTxtSet.onClick = self.txt_set
        self.txt.onClickTag = self.txt_clicked

    def setup_layout(self, layout):
        self.txt.grid(sticky=tk.NS)

    def setup_defaults(self):
        self.rowconfigure(0, weight=0)  # Buttons

    def setup_adefaults(self):
        self.txt_set(cnt=20)

    def txt_reset(self, event=None):
        self.txt.wstate = ''

    def txt_set(self, event=None, *, cnt=None):
        texts = []
        if cnt is None:
            cnt = 20 + random.choice(range(-10, 5))
        for r in range(cnt):
            texts.append(f'Line {"%02d" % r}/{cnt} ')
            if r % 2 == 0:
                _txt = 'EVEN'
            else:
                _txt = '    '
            texts.append(f'<a>[{_txt}]</a>')
            texts.append('<br/>')
            if r % 5 == 0:
                texts.append('<br/>')
        self.txt.wstate = ''.join(texts)

    def txt_clicked(self, tag, tag_id, tags_other):
        logger.debug(f'Clicked on {tag} {tag_id} :: {tags_other}')


class TreeExample(Tree):
    pass


class ComboboxCB(Combobox):
    pass


class RW(RootWindow):
    def setup_widgets(self):
        choices = spec.StaticList(('Choice %d' % n for n in range(5)), defaultIndex=3)
        vc = self.var(var.Boolean, name='bool', value=True)

        self.b1 = Button(self, label='B1')
        self.c1 = Checkbox(self, label='Checkbox1')
        self.bE1 = Button(self, label='Set "example"')
        self.b2 = Button(self, label='Debug')
        self.c2ro = Checkbox(self, label='RO "bool"', readonly=True, variable=vc)
        self.c2rw = Checkbox(self, label='RW "bool"', readonly=False, variable=vc)
        self.e1 = Entry(self)  # label='Entry1'
        self.lbs = LuftBaloons(self)
        self.ubox = UpstreamBool(self, label='Upstream', labelAnchor=CP.S,
                                 what_bool=vc)
        self.choice = ComboboxCB(self, values=choices)  # label='CB'
        self.choice_reset = Button(self, label='CB: Set Last')
        self.lf = ListFrame(self, label='List Box', cbox1=self.c1.variable)

        self.txt = TextEditor(self)
        self.nb = NB(self)
        self.arbre = TreeExample(self, label='Label', columns={
            'number': 'Number',
        })

        # Setup events
        self.b1.onClick = self.c1.toggle
        self.bE1.onClick = self.ask_contents
        self.b2.onClick = self.debug
        self.choice_reset.onClick = self.choice.eSet(choices[-1])

    def setup_defaults(self):
        BindingGlobal(self, '<F4>', lambda e: self.debug(),
                      immediate=True, description='Debug')

    def setup_adefaults(self):
        logger.debug('Setup arbre state:')
        self.arbre.wstate = [
            Tree.Element('First', ['1']),
            Tree.Element('Second', ['2'], children=[
                Tree.Element('Second.One', ['21']),
            ]),
            Tree.Element('Third', ['3'], children=[
                Tree.Element('Third.One', ['31']),
                Tree.Element('Third.Two', ['32'], children=[
                    Tree.Element('Third.Two.One', ['321']),
                    Tree.Element('Third.Two.Two', ['322']),
                    Tree.Element('Third.Two.3', ['323']),
                ]),
                Tree.Element('Third.Tee', ['33']),
            ]),
            Tree.Element('Tenth', ['10']),
        ]
        logger.debug('Global Bindings:')
        for bname, B in self._bindings_global.items():
            logger.debug('- %s: %s%s', bname, '' if B else '[Disabled] ', B.description)

    def ask_contents(self):
        string = tk.simpledialog.askstring('Set Contents', f'Set the "{self.e1.label}" contents')
        if string is not None:
            self.e1.wstate = string

    def debug(self):
        from pprint import pformat
        logging.info('=> State @ %s[%r]', self, self)
        for line in pformat(self.wstate).splitlines():
            logging.info('%s', line)
        logging.info('=> State @ ubox')
        for line in pformat(self.ubox.wstate).splitlines():
            logging.info('%s', line)
        logging.info('=> State Set')
        new = self.wstate
        for b in ('0', '12'):
            new['lbs'][f'lb:{b}'] = not new['lbs'][f'lb:{b}']
        self.wstate = new
        logging.info('=> GUI States')
        logging.info('   GUI State @ %s[%r]', self, self)
        for line in pformat(self.gstate).splitlines():
            pass  # logging.info('  %s', line)
        logging.info('   GUI State @ c2ro')
        for line in pformat(self.c2ro.gstate).splitlines():
            pass  # logging.info('  %s', line)
        logging.info('   GUI State @ c2rw')
        for line in pformat(self.c2rw.gstate).splitlines():
            pass  # logging.info('  %s', line)
        logging.info('   GUI State @ choice')
        for line in pformat(self.choice.gstate).splitlines():
            pass  # logging.info('  %s', line)
        logging.info('   GUI State @ e1')
        for line in pformat(self.e1.gstate).splitlines():
            pass  # logging.info('  %s', line)
        logging.info('   GUI State @ txt.txt')
        for line in pformat(self.txt.txt.gstate).splitlines():
            pass  # logging.info('  %s', line)
        # self.set_gui_state(enabled=True, valid=True)  # Invalid Target
        logging.info('=> NB')
        for tn, ti in self.nb.wtabs.items():
            logging.info(f'   | {tn}: {ti}')


def entrypoint():
    import argparse
    parser = argparse.ArgumentParser(description='Showcase for tkmilan module')

    # parser.add_argument('--version', action='version', version=PROJECT_VERSION)
    parser.add_argument('-v', '--verbose', dest='loglevel',
                        action='store_const', const=logging.DEBUG, default=logging.INFO,
                        help='Add more details to the standard error log')
    parser.add_argument('--debug', action='store_true',
                        help=argparse.SUPPRESS)
    args = parser.parse_args()

    # Logs
    logs_fmt = '%(levelname)-5.5s %(name)s@%(funcName)s| %(message)s'
    try:
        import coloredlogs  # type: ignore
        coloredlogs.install(level=args.loglevel, fmt=logs_fmt)
    except ImportError:
        logging.basicConfig(level=args.loglevel, format=logs_fmt)
    logging.captureWarnings(True)
    # # Silence spammy modules, even in verbose mode
    if not args.debug and args.loglevel == logging.DEBUG:
        for dmodule in MODULES_VERBOSE:
            logging.getLogger(f'{__package__}.{dmodule}').setLevel(logging.INFO)

    # Widget Tester / Showcase
    r = RW()
    logger.debug('Screen Size: %r', r.size_screen)
    logger.debug('         /2: %r', r.size_screen.reduce(2))
    r.mainloop()


if __name__ == '__main__':
    import sys
    sys.exit(entrypoint() or 0)
