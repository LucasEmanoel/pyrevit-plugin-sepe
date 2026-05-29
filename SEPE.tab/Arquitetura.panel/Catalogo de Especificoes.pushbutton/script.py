# -*- coding: utf-8 -*-
import os
import webbrowser

from pyrevit import forms, script

usuario = os.environ.get("USERNAME")

# 1. Ajuste o nome e a extensão do arquivo Excel aqui (.xlsx ou .xls)
manual_path = "C:\\Users\\{}\\DC\\ACCDocs\\SEPE\\BIBLIOTECA\\Project Files\\REVIT\\ARQUITETURA\\01_TEMPLATE\\CATÁLOGO_SEPE_ARQUITETURA.xlsx".format(
    usuario
)

def main():
    """Abre a planilha Excel automaticamente no programa padrão."""
    try:
        if os.path.exists(manual_path):
            # O webbrowser detecta que é .xlsx e abre direto no Excel
            webbrowser.open(manual_path)
            script.exit()

        forms.alert(
            "Planilha não encontrada!\n\n"
            "Usuário atual: {}\n"
            "Caminho buscado:\n{}\n\n"
            "Verifique se o arquivo existe neste local.".format(usuario, manual_path),
            title="Erro - Planilha de modelagem",
        )
    except Exception as e:
        forms.alert("Erro ao abrir a planilha:\n{}".format(str(e)), title="Erro")


if __name__ == "__main__":
    main()