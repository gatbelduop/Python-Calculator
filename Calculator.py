from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout

class CalculatorApp(App):
    def build(self):
        self.icon = 'icon.png'
        self.operators = ['+', '-', '*', '/']
        self.last_was_operator = None
        self.last_button = None

        main_layout = BoxLayout(orientation='vertical')
        self.solution = TextInput(background_color="silver", foreground_color="black",
        multiline=False, halign='right', font_size=55, readonly=True)

        main_layout.add_widget(self.solution)
        buttons = [
            [' ',  'C'],
            ['7', '8', '9', '⌫'],
            ['4', '5', '6', '/'],
            ['1', '2', '3', '*'],
            ['.', '0', '-', '+']
        ]
        for row in buttons:
            h_layout = BoxLayout()
            for label in row:
                button = Button(text=label, font_size=32, background_color="lightgrey", pos_hint={'center_x': 0.5, 'center_y': 0.5})
                button.bind(on_press=self.on_button_press)
                h_layout.add_widget(button)
            main_layout.add_widget(h_layout)

        equals_button = Button(text='=', font_size=32, background_color="lightgrey", pos_hint={'center_x': 0.5, 'center_y': 0.5})

        equals_button.bind(on_press=self.on_solution)
        main_layout.add_widget(equals_button)

        return main_layout

    def on_button_press(self, instance):
        current = self.solution.text
        button_text = instance.text

        if button_text == 'C':
            self.solution.text = ''
            self.last_was_operator = None
        elif button_text == '⌫':
            self.solution.text = current[:-1]
            self.last_was_operator = False
        else:
            if current and (self.last_was_operator and button_text in self.operators):
                return
            elif current == '' and button_text in self.operators:
                return
            elif current == '' and button_text == '0':
                return
            elif current == '0' and button_text.isdigit() and button_text != '0':
                # prevent numbers like 05; keep just 5 if '0' exists as the only digit
                self.solution.text = button_text
            else:
                new_text = current + button_text
                self.solution.text = new_text
            self.last_was_operator = button_text in self.operators
        self.last_button = button_text

    def compute_solution(self, expression):
        try:
            # eval is simple for this basic calculator; input comes from buttons only
            return str(eval(expression))
        except (SyntaxError, ZeroDivisionError, NameError, TypeError):
            return 'Error'

    def clear_error(self, dt):
        if self.solution.text == 'Error':
            self.solution.text = ''

    def on_solution(self, instance):
        text = self.solution.text
        if text:
            self.solution.text = self.compute_solution(text)
            if self.solution.text == 'Error':
                Clock.schedule_once(self.clear_error, 1)


if __name__ == '__main__':
    app = CalculatorApp()
    app.run()