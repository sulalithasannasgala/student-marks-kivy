from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import pandas as pd
import os

CSV_FILE = 'students.csv'

if not os.path.exists(CSV_FILE):
    columns = ['Student Name'] + [f'Subject{i+1}' for i in range(10)] + ['Total', 'Average', 'Rank']
    pd.DataFrame(columns=columns).to_csv(CSV_FILE, index=False)

class StudentForm(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(cols=2, spacing=5, padding=10, **kwargs)
        self.inputs = {}
        self.add_widget(Button(text='Student Name')); self.inputs['Student Name'] = TextInput(); self.add_widget(self.inputs['Student Name'])

        for i in range(10):
            self.add_widget(Button(text=f'Subject{i+1}'))
            self.inputs[f'Subject{i+1}'] = TextInput()
            self.add_widget(self.inputs[f'Subject{i+1}'])

        for field in ['Total', 'Average', 'Rank']:
            self.add_widget(Button(text=field))
            self.inputs[field] = TextInput()
            self.add_widget(self.inputs[field])

        for action in ['Calculate', 'Enter', 'Delete', 'Search']:
            btn = Button(text=action)
            btn.bind(on_press=self.handle_action)
            self.add_widget(btn)

    def handle_action(self, instance):
        action = instance.text
        values = {k: v.text for k, v in self.inputs.items()}

        if action == 'Calculate':
            subjects = [float(values[f'Subject{i+1}']) if values[f'Subject{i+1}'] else 0 for i in range(10)]
            total = sum(subjects)
            average = total / len(subjects)
            df = pd.read_csv(CSV_FILE)
            df['Total'] = pd.to_numeric(df['Total'], errors='coerce')
            df = df.sort_values(by='Total', ascending=False)
            rank = (df['Total'] > total).sum() + 1
            self.inputs['Total'].text = str(total)
            self.inputs['Average'].text = f'{average:.2f}'
            self.inputs['Rank'].text = str(rank)

        elif action == 'Enter':
            df = pd.read_csv(CSV_FILE)
            new_data = {k: v.text for k, v in self.inputs.items()}
            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            df.to_csv(CSV_FILE, index=False)

        elif action == 'Delete':
            df = pd.read_csv(CSV_FILE)
            df = df[df['Student Name'] != values['Student Name']]
            df.to_csv(CSV_FILE, index=False)

        elif action == 'Search':
            df = pd.read_csv(CSV_FILE)
            result = df[df['Student Name'] == values['Student Name']]
            if not result.empty:
                for col in result.columns:
                    if col in self.inputs:
                        self.inputs[col].text = str(result.iloc[0][col])

class StudentApp(App):
    def build(self):
        return StudentForm()

StudentApp().run()
