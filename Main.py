import tkinter as tk
from tkinter import scrolledtext
from tkinter.filedialog import askopenfilename, asksaveasfilename
from printer import Printer
from lexer import tokenize_input
from parsear import Parser
from db import DB
from arbol import arbol

class ScrollText(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.text = tk.Text(
            self,
            bg="#f8f9fa",
            foreground="#343a40",
            insertbackground="#3b5bdb",
            selectbackground="blue",
            width=100,
            height=15,
            font=("Courier New", 13),
        )

        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.text.yview)
        self.text.configure(yscrollcommand=self.scrollbar.set)

        self.numberLines = TextLineNumbers(self, width=25, bg="#dee2e6")
        self.numberLines.attach(self.text)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.numberLines.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
        self.text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.text.bind("<Key>", self.onPressDelay)
        self.text.bind("<Button-1>", self.numberLines.redraw)
        self.scrollbar.bind("<Button-1>", self.onScrollPress)
        self.text.bind("<MouseWheel>", self.onPressDelay)

    def onScrollPress(self, *args):
        self.scrollbar.bind("<B1-Motion>", self.numberLines.redraw)

    def onScrollRelease(self, *args):
        self.scrollbar.unbind("<B1-Motion>", self.numberLines.redraw)

    def onPressDelay(self, *args):
        self.after(2, self.numberLines.redraw)

    def get(self, *args, **kwargs):
        return self.text.get(*args, **kwargs)

    def insert(self, *args, **kwargs):
        return self.text.insert(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.text.delete(*args, **kwargs)

    def index(self, *args, **kwargs):
        return self.text.index(*args, **kwargs)

    def redraw(self):
        self.numberLines.redraw()


class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs, highlightthickness=0)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        """redraw line numbers"""
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True:
            dline = self.textwidget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(
                2,
                y,
                anchor="nw",
                text=linenum,
                fill="#868e96",
                font=("Courier New", 13, "bold"),
            )
            i = self.textwidget.index("%s+1line" % i)


class Ventana():
    def __init__(self) -> None:
        self.ventana = tk.Tk()
        self.printer = Printer()
        self.db = DB()
        # self.parser = Parser()


        self.ventana.title("Proyecto 2")
        #titulo
        self.titulo = tk.Label(self.ventana, text="BizData", padx=10, pady=10, font=("Courier New", 20))
        
        #botones
        self.boton1 = tk.Button(self.ventana, text="Abrir", command=self.open_file,height=2, width=10,bg="#c3e88d", fg="black",font=("Courier New", 12))
        self.boton2 = tk.Button(self.ventana, text="Guardar", command=self.save_file,height=2, width=10,bg="#c3e88d", fg="black",font=("Courier New", 12))
        self.boton3 = tk.Button(self.ventana, text="Analizar", command=self.analizar_texto,height=2, width=10,bg="#c3e88d", fg="black",font=("Courier New", 12))
        # self.boton4 = tk.Button(self.ventana, text="Reportes", command=self.save_file,height=2, width=10,bg="#c3e88d", fg="black",font=("Courier New", 12))
        self.titulo.grid(row=0, column=1)
        self.boton1.grid(row=3, column=0)
        self.boton2.grid(row=3, column=1)
        self.boton3.grid(row=3, column=2)
        # self.boton4.grid(row=3, column=2)


        self.txtArea = scrolledtext.ScrolledText(self.ventana, wrap=tk.WORD, width=63, height=30, bg='#292d3e', fg='white')
        self.txtArea.grid(row=1, column=1)

        # self.consola = scrolledtext.ScrolledText(self.ventana, wrap=tk.WORD, width=60, height=30, bg='#292d3e', fg='white')
        # self.consola.config(state='disabled')
        # self.consola.grid(row=1, column=3, columnspan=3)

        screen_width = self.ventana.winfo_screenwidth()
        screen_height = self.ventana.winfo_screenheight()

        window_width = 740  # Ancho de la ventana
        window_height = 600  # Alto de la ventana
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        self.ventana.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def open_file(self):
        global filepath
        filepath = askopenfilename(
            filetypes=[("Archivos .bizdata", "*.bizdata")]
        )
        if not filepath:
            return
        
        self.txtArea.delete(1.0,tk.END)
        with open(filepath, "r") as input_file:
            text = input_file.read()
            self.txtArea.insert(tk.END, text)
        self.ventana.title(f"Proyecto 2 - {filepath.split('/')[-1]}")
        # tokens = tokenize_input(text)
        # parser = Parser(tokens)
        # parser.parse()
        # self.show_elements()
        


    def save_file(self):
        filepath = asksaveasfilename(
            defaultextension="json",
            filetypes=[("Archivos .bizdata", "*.bizdata")],
        )
        if not filepath:
            return
        with open(filepath, "w") as output_file:
            text = self.txtArea.get(1.0, tk.END)
            output_file.write(text)
        self.ventana.title(f"Proyecto 2 - {filepath.split('/')[-1]}")

    def show_elements(self):
        # print(parser.parse())
        print("holaassssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss")
        # print(self.db.imprimirRegistros())
        print("holaassssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss")
        # self.elements_label.config(text=str(.mostrar()))

    def analizar_texto(self):
        print("Analizando...")
        # self.txtArea.delete(1.0,tk.END)
        with open(filepath, "r") as input_file:
            text = input_file.read()
            # self.txtArea.insert(tk.END, text)
        tokens = tokenize_input(text)
        parser = Parser(tokens)
        parser.parse()
        arbol.generarGrafica()
        # self.show_elements()
    
    
    def start(self):
        self.ventana.mainloop()
    

if __name__ == '__main__':
    Ventana().start()
    