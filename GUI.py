import PySimpleGUI as sg

import PdfHandler

class GUI():
    def __init__(self, filename):
        self.pdf = PdfHandler.PdfHandler(filename)

        self.cur_page = 0

        data = self.pdf.getImage(self.cur_page)

        self.image_elem = sg.Image(data=data)

        self.goto = sg.InputText(str(self.cur_page + 1), size=(5, 1), key="-PageNumber-")
        
        self.layout = [[
                sg.ReadButton('Next'),
                sg.ReadButton('Prev'),
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
        

    def mainloop(self):
        while True:
            event, value = self.window.read()
            if event == sg.WIN_CLOSED and (value is None or value['-PageNumber-'] is None):
                break
            if event in self.quit_buttons:
                break

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
            while self.cur_page < 0:         # pages > 0 look nicer
                self.cur_page += len(self.pdf.pdf)

            data = self.pdf.getImage(self.cur_page)
            self.image_elem.update(data=data)

            # update page number field
            if event in self.my_keys:
                self.goto.update(str(self.cur_page + 1))

        self.window.close()
