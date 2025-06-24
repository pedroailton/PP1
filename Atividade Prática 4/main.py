import tkinter as tk
from tkinter import messagebox

# Função para tooltip (dica ao passar o mouse)
def criar_tooltip(widget, texto):
    tooltip = tk.Toplevel(widget)
    tooltip.withdraw()
    tooltip.overrideredirect(True)
    label = tk.Label(tooltip, text=texto, background="#ffffe0", relief='solid', borderwidth=1, font=("Segoe UI", 9))
    label.pack()

    def mostrar(event):
        x, y, cx, cy = widget.bbox("insert")
        x += widget.winfo_rootx() + 30
        y += widget.winfo_rooty() + 10
        tooltip.geometry(f"+{x}+{y}")
        tooltip.deiconify()

    def esconder(event):
        tooltip.withdraw()

    widget.bind('<Enter>', mostrar)
    widget.bind('<Leave>', esconder)

# Função principal de cálculo
def calcular_estatisticas():
    try:
        nome = entry_nome.get()
        idade = int(entry_idade.get())
        cidade = entry_cidade.get()
        estado = entry_estado.get()
        digitais = int(entry_digitais.get())
        fisicos = int(entry_fisicos.get())
        estudo = float(entry_estudo.get())
        lazer = float(entry_lazer.get())
        preferencia = var_preferencia.get()
        area = entry_area.get()

        if not nome or not cidade or not estado or not area:
            raise ValueError("Todos os campos devem estar preenchidos.")

        total_livros = digitais + fisicos
        livros_5_anos = total_livros * 5
        horas_estudo_ano = estudo * 52
        horas_lazer_ano = lazer * 52
        paginas_ano = total_livros * 250

        if livros_5_anos >= 100:
            nivel = "Ávido(a)"
            blocos_coloridos = 10
        elif livros_5_anos >= 50:
            nivel = "Frequente"
            blocos_coloridos = 7
        elif livros_5_anos >= 20:
            nivel = "Regular"
            blocos_coloridos = 4
        else:
            nivel = "Iniciante"
            blocos_coloridos = 2

        mensagem = f"\n🎉 Olá, {nome} de {cidade}-{estado}!\n"
        if idade < 18:
            mensagem += "Você está em uma fase essencial para adquirir hábitos de leitura.\n"
        elif idade < 30:
            mensagem += "Leitura pode ser seu maior diferencial nessa fase profissional.\n"
        else:
            mensagem += "Nunca é tarde para mergulhar em bons livros.\n"

        mensagem += f"\n📚 Nível de leitura: {nivel}\n"
        mensagem += f"📖 Você informou que leu {total_livros} livros no último ano. Isso equivale a {livros_5_anos} livros em 5 anos.\n"
        mensagem += f"📘 Estudo anual: {horas_estudo_ano:.0f} horas | Lazer anual: {horas_lazer_ano:.0f} horas\n"
        mensagem += f"📄 Estimativa de leitura: {paginas_ano} páginas/ano\n"
        mensagem += f"🎯 Preferência: {preferencia} | Área: {area}"

        resultado_text.config(state='normal')
        resultado_text.delete("1.0", tk.END)
        resultado_text.insert(tk.END, mensagem)
        resultado_text.config(state='disabled')

        # Atualiza barra de progresso
        canvas_barra.delete("all")
        cores = ["#6a0dad", "#8a2be2", "#9370db", "#4b0082"]  # tons de roxo
        cor_nivel = {"Iniciante": "#6a0dad", "Regular": "#8a2be2", "Frequente": "#9370db", "Ávido(a)": "#4b0082"}.get(nivel, "gray")

        for i in range(10):
            x0 = 5
            y0 = 195 - i * 20
            x1 = 45
            y1 = y0 + 18
            if i < blocos_coloridos:
                canvas_barra.create_rectangle(x0, y0, x1, y1, fill=cor_nivel, outline="black")
            else:
                canvas_barra.create_rectangle(x0, y0, x1, y1, fill="#3a3a3a", outline="black")

        criar_tooltip(canvas_barra, f"Nível: {nivel}\n{livros_5_anos} livros/5 anos")

    except ValueError as e:
        messagebox.showerror("Erro de entrada", f"⚠️ Dados inválidos ou incompletos: {str(e)}")

# Interface principal
root = tk.Tk()
root.title("Relatório de Leitura 📚")
root.geometry("650x600")
root.configure(bg="#1e1a1a")

# Área superior (Entradas)
top_frame = tk.Frame(root, height=300, bg="#1a1a1a")
top_frame.pack(fill="both", expand=False)

canvas_top = tk.Canvas(top_frame, bg="#2d2d2d")
top_scrollbar = tk.Scrollbar(top_frame, orient="vertical", command=canvas_top.yview)
entry_container = tk.Frame(canvas_top, bg="#2d2d2d")

entry_container.bind("<Configure>", lambda e: canvas_top.configure(scrollregion=canvas_top.bbox("all")))
canvas_top.create_window((0, 0), window=entry_container, anchor="nw")
canvas_top.configure(yscrollcommand=top_scrollbar.set)

canvas_top.pack(side="left", fill="both", expand=True)
top_scrollbar.pack(side="right", fill="y")

# Área inferior (Resultados)
bottom_frame = tk.Frame(root, bg="#1a1a1a")
bottom_frame.pack(fill="both", expand=True)

left_result = tk.Frame(bottom_frame, bg="#1a1a1a")
left_result.pack(side="left", fill="both", expand=True)
right_barra = tk.Frame(bottom_frame, width=50, bg="#1a1a1a")
right_barra.pack(side="right", fill="y")

canvas_bottom = tk.Canvas(left_result, bg="#2d2d2d")
bottom_scrollbar = tk.Scrollbar(left_result, orient="vertical", command=canvas_bottom.yview)
result_container = tk.Frame(canvas_bottom, bg="#2d2d2d")

result_container.bind("<Configure>", lambda e: canvas_bottom.configure(scrollregion=canvas_bottom.bbox("all")))
canvas_bottom.create_window((0, 0), window=result_container, anchor="nw")
canvas_bottom.configure(yscrollcommand=bottom_scrollbar.set)

canvas_bottom.pack(side="left", fill="both", expand=True)
bottom_scrollbar.pack(side="right", fill="y")

# Labels e campos de entrada
labels = ["Nome", "Idade", "Cidade", "Estado", "Livros digitais (último ano)", "Livros físicos (último ano)",
          "Horas de estudo/semana", "Horas de lazer/semana", "Preferência de leitura", "Área de interesse"]
entries = []

for i, label in enumerate(labels):
    tk.Label(entry_container, text=label+":", anchor="w", bg="#2d2d2d", fg="white", font=("Segoe UI", 10, "bold"))\
        .grid(row=i, column=0, sticky="w", padx=10, pady=5)
    if label == "Preferência de leitura":
        var_preferencia = tk.StringVar(value="Digital")
        menu = tk.OptionMenu(entry_container, var_preferencia, "Digital", "Físico")
        menu.config(bg="#6a0dad", fg="white")
        menu.grid(row=i, column=1, sticky="ew", padx=10, pady=5)
    else:
        entry = tk.Entry(entry_container, bg="#ffffff", fg="#000000")
        entry.grid(row=i, column=1, sticky="ew", padx=10, pady=5)
        entries.append(entry)

entry_nome, entry_idade, entry_cidade, entry_estado, entry_digitais, entry_fisicos, \
entry_estudo, entry_lazer, entry_area = entries[:9]

# Botão de ação
tk.Button(entry_container, text="🔍 Analisar Perfil", bg="#6a0dad", fg="white",
          font=("Segoe UI", 11, "bold"), command=calcular_estatisticas).grid(row=len(labels), column=0, columnspan=2, pady=10)

# Campo de resultado
resultado_text = tk.Text(result_container, wrap=tk.WORD, font=("Segoe UI", 10), bg="#3a3a3a", fg="white", height=15)
resultado_text.pack(fill="both", expand=True, padx=10, pady=10)
resultado_text.config(state='disabled')

# Barra de progresso visual
canvas_barra = tk.Canvas(right_barra, width=50, height=220, bg="#1a1a1a", highlightthickness=0)
canvas_barra.pack(pady=20)

root.mainloop()
