import PySimpleGUI as sg
import os

import PdfHandler


class GUI:
    def __init__(self, filename):
        self.pdf = PdfHandler.PdfHandler(filename)

        self.cur_page = 0

        data = self.pdf.getImage(self.cur_page)

        self.image_elem = sg.Image(data=data)

        self.goto = sg.InputText(str(self.cur_page + 1), size=(5, 1), key="-PageNumber-")

        self.menu_def = [['&File', ['&Open     Ctrl-O', '&Save       Ctrl-S', '&Properties', 'E&xit']],
                         ['&Edit', ['&Paste', ['Special', 'Normal', ], 'Undo'], ],
                         ['&Toolbar', ['---', 'Command &1', 'Command &2',
                                       '---', 'Command &3', 'Command &4']],
                         ['&Help', '&About...'], ]

        self.layout = [
            [sg.Menu(self.menu_def, tearoff=False, pad=(200, 1))],
            [
                sg.ReadButton('Prev'),
                sg.ReadButton('Next'),
                sg.Text('Page:'),
                self.goto,
                sg.Text('(%i)' % len(self.pdf.pdf)),
            ],
            [self.image_elem],
        ]

        title = "OmniPDF"
        self.window = sg.Window(title, self.layout, return_keyboard_events=True,
                                location=(0, 0), use_default_focus=False, no_titlebar=False)

        # now define the buttons / events we want to handle
        self.enter_buttons = [chr(13), "Return:13"]
        self.quit_buttons = ["Escape:27", chr(27)]
        self.next_buttons = ["Next", "Next:34", "MouseWheel:Down"]
        self.prev_buttons = ["Prev", "Prior:33", "MouseWheel:Up"]

        # all the buttons we will handle
        self.my_keys = self.enter_buttons + self.next_buttons + self.prev_buttons

    def onAbout(self):
        self.window.disappear()
        sg.popup('About this program', 'Version 1.0',
                 'PySimpleGUI Version', sg.version, grab_anywhere=True)
        self.window.reappear()

    def onOpen(self):
        filename = sg.popup_get_file('File to Open', no_window=True)
        if os.path.isfile(filename):
            self.pdf = PdfHandler.PdfHandler(filename)
            self.cur_page = 0

            data = self.pdf.getImage(self.cur_page)
            self.image_elem.update(data=data)
            self.goto.update(str(self.cur_page + 1))
    
    def onSaveAs(self):
        filename = sg.popup_get_file('Save As', no_window=True, save_as=True)
        self.pdf.saveAs(filename)

    def mainloop(self):
        while True:
            event, value = self.window.read()

            if event in self.enter_buttons:
                try:
                    self.cur_page = int(value['-PageNumber-']) - 1  # check if valid
                    while self.cur_page < 0:
                        self.cur_page += len(self.pdf.pdf)
                except:
                    self.cur_page = 0  # this guy's trying to fool me

            elif event in self.next_buttons:
                self.cur_page += 1
            elif event in self.prev_buttons:
                self.cur_page -= 1

            # sanitize page number
            if self.cur_page >= len(self.pdf.pdf):  # wrap around
                self.cur_page = 0
            while self.cur_page < 0:  # pages > 0 look nicer
                self.cur_page += len(self.pdf.pdf)

            data = self.pdf.getImage(self.cur_page)
            self.image_elem.update(data=data)

            # update page number field
            if event in self.my_keys:
                self.goto.update(str(self.cur_page + 1))

            """ --- Menu Events --- """
            if event == "About...":
                self.onAbout()
            elif event == 'Open     Ctrl-O':
                self.onOpen()
            elif event == 'Save       Ctrl-S':
                self.onSaveAs()
            elif event == 'Properties':
                pass

            """ --- Exit Events --- """
            if event == sg.WIN_CLOSED and (value is None or value['-PageNumber-'] is None):
                break
            if event in self.quit_buttons:
                break

        self.window.close()
