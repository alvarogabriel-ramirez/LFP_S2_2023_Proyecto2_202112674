import os
from datetime import datetime
import webbrowser
from prettytable import PrettyTable

class DB:
    def __init__(self):
        self.claves = {}

    def agregarClave(self, clave):
        self.claves[clave] = []

    def agregarValor(self, pos, valor):
        clave = list(self.claves.keys())[pos]
        self.claves[clave].append(valor)

    def conteo(self):
        clave = list(self.claves.keys())[0]
        return len(self.claves[clave])

    def contarsi(self, clave, valor):
        return self.claves[clave].count(valor)

    def max(self, clave):
        return max(self.claves[clave])

    def min(self, clave):
        return min(self.claves[clave])

    def promedio(self, clave):
        return sum(self.claves[clave])/len(self.claves[clave])

    def daatos(self):
        x = PrettyTable()
        x.field_names = list(self.claves.keys())
        for i in range(len(self.claves[list(self.claves.keys())[0]])):
            row = []
            for clave in self.claves:
                row.append(self.claves[clave][i])
            x.add_row(row)
        print(x)
    
    def datos(self):
        for clave in self.claves:
            print(clave, end="\t")
        print()
        for i in range(len(self.claves[list(self.claves.keys())[0]])):
            for clave in self.claves:
                print(self.claves[clave][i], end="\t")
            print()

        

    def sumar(self, clave):
        return sum(self.claves[clave])

    def exportarReporte(self, titulo):
        x = PrettyTable()
        x.field_names = list(self.claves.keys())
        for i in range(len(self.claves[list(self.claves.keys())[0]])):
            row = []
            for clave in self.claves:
                row.append(self.claves[clave][i])
            x.add_row(row)

        now = datetime.now()
        # filename = f"{titulo}_{now.strftime('%Y-%m-%d_%H-%M-%S')}.html"
        filename = f"{titulo}.html"

        style="style.css"
        with open(filename, "w") as f:
            f.write(f"<html><head><title>{titulo}</title></head><body>")
            f.write(f"<h1>{titulo}</h1>")
            f.write(f"<br><link rel='stylesheet' href='{style}'>")
            f.write(x.get_html_string())
            f.write("</body></html>")

        reporte =os.path.abspath(filename)
        print(f"Reporte generado en {reporte.split('/')[-1]}")
        # webbrowser.open('file://' + reporte)


    def imprimirRegistros(self):
        print("*"*50)
        print("valores:")
        for clave in self.claves:
            print(clave, self.claves[clave])
        print("*"*50)
