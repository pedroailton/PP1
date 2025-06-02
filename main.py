from tkinter import *

root = Tk()

class Funcoes:
    #lógica back-end decimal para binário, com tratamento de erro para dígitos invalidos
    # e valores negativos
    def dec_to_bin(self):
        valor = self.valor_entry.get()
        try:
            decimal = int(valor)
            if decimal < 0: #para valores negativos
                binario = '-' + bin(abs(decimal))[2:]
            else:
                binario = bin(decimal)[2:]
            self.lb_resultado.config(text=f"Resultado: {binario}")
        except ValueError:
            self.lb_resultado.config(text="Erro: valor decimal inválido")

    #lógica back-end binário para decimal, com tratamento de erro para dígitos invalidos
    # e valores negativos
    def bin_to_dec(self):
        valor = self.valor_entry.get()
        try:
            if valor.startswith('-'): #para valores negativos
                decimal = -int(valor[1:], 2)
            else:
                decimal = int(valor, 2)
            self.lb_resultado.config(text=f"Resultado: {decimal}")
        except ValueError:
            self.lb_resultado.config(text="Erro: valor binário inválido")


class Application(Funcoes): #front-end
    def __init__(self):
        self.root = root
        self.tela()
        self.frame_da_tela()
        self.widgets()
        root.mainloop()

    def tela(self):
        self.root.title("Calculadora Conversora Binario-Decimal | Decimal-Binario")
        self.root.configure(background='#4F4F4F')
        self.root.geometry("400x300")
        self.root.resizable(True, True)
        self.root.minsize(width = 400, height = 300)

    def frame_da_tela(self):
        self.frame = Frame(self.root, bd=4, bg='#1C1C1C',
                           highlightbackground='#F5F5DC', highlightthickness=4)
        self.frame.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

    def widgets(self):
        # Texto de instrução
        self.lb_texto_entrada = Label(self.frame, text="Insira o valor a ser convertido:", bg='#1C1C1C', fg='white')
        self.lb_texto_entrada.place(relx=0.1, rely=0.05, relwidth=0.8, relheight = 0.1)

        # Campo de entrada
        self.valor_entry = Entry(self.frame)
        self.valor_entry.place(relx=0.1, rely=0.16, relwidth=0.8, relheight=0.1)

        # Botão Decimal -> Binário
        self.bt_dec_to_bin = Button(self.frame, text="Decimal → Binário", command = self.dec_to_bin)
        self.bt_dec_to_bin.place(relx=0.1, rely=0.30, relwidth=0.35, relheight=0.12)

        # Botão Binário -> Decimal
        self.bt_bin_to_dec = Button(self.frame, text="Binário → Decimal", command = self.bin_to_dec)
        self.bt_bin_to_dec.place(relx=0.55, rely=0.30, relwidth=0.35, relheight=0.12)

        # Texto de resultado
        self.lb_resultado = Label(self.frame, text="Resultado:", bg='#1C1C1C', fg = 'white')
        self.lb_resultado.place(relx=0.1, rely=0.50, relwidth=0.8, relheight=0.12)

if __name__ == "__main__":
    Application()
