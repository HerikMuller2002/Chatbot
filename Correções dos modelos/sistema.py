import tkinter as tk
import pandas as pd

df = pd.read_excel(r'Correções dos modelos\teste.xlsx')
df = df.drop(['Unnamed: 0'], axis=1)
df_filtrado = df.loc[:, ['cause_pt', 'cause_en']]

class AvaliacaoApp:
    def __init__(self, df):
        self.row = None
        self.cols = df.columns
        self.df = df
        self.index = 0
        self.root = tk.Tk()
        self.root.title("Avaliação de Linhas")
        self.label1 = tk.Label(self.root, text=self.cols[0])
        self.label1.pack()
        self.textbox1 = tk.Text(self.root, height=5, width=150)
        self.textbox1.pack()
        self.label2 = tk.Label(self.root, text=self.cols[1])
        self.label2.pack()
        self.textbox2 = tk.Text(self.root, height=5, width=150)
        self.textbox2.pack()
        self.ok_button = tk.Button(self.root, text="OK", command=self.ok_button_clicked)
        self.ok_button.pack(side=tk.LEFT)
        self.nok_button = tk.Button(self.root, text="NOK", command=self.nok_button_clicked)
        self.nok_button.pack(side=tk.LEFT)
        self.back_button = tk.Button(self.root, text="Voltar", command=self.back_button_clicked)
        self.back_button.pack(side=tk.LEFT)
        self.next_line()
        self.root.mainloop()

    def next_line(self):
        if self.index < len(self.df):
            row = self.df.iloc[self.index]
            self.row = row
            self.textbox1.delete('1.0', tk.END)
            self.textbox2.delete('1.0', tk.END)
            self.textbox1.insert(tk.END, str(row['cause_pt']))
            self.textbox2.insert(tk.END, str(row['cause_en']))
            self.index += 1
        else:
            self.root.destroy()

    def ok_button_clicked(self):
        self.register_line('OK')

    def nok_button_clicked(self):
        self.register_line('NOK')

    def back_button_clicked(self):
        if self.index > 1:
            self.index -= 2
            self.next_line()

    def register_line(self, situation):
        df_correct = pd.read_excel(r'Correções dos modelos\sistem_correct.xlsx')
        if len(df_correct) < self.index:
            new_df = pd.DataFrame(self.row).transpose()
            new_df['situation'] = situation
            df_correct = pd.concat([df_correct, new_df], axis=0).reset_index()
            df_correct = df_correct.drop(['index'], axis=1)
        else:
            df_correct.loc[self.index-1, 'situation'] = situation
        try:
            df_correct = df_correct.drop(['Unnamed: 0'], axis=1)
        except:
            pass
        df_correct.to_excel(r'Correções dos modelos\sistem_correct.xlsx')
        self.next_line()

app = AvaliacaoApp(df_filtrado)
