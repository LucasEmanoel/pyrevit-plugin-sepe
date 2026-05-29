# -*- coding: utf-8 -*-
import os
import webbrowser

from pyrevit import forms, script

usuario = os.environ.get("USERNAME")
manual_path = "C:\\Users\\{}\\DC\\ACCDocs\\SEPE\\BIBLIOTECA\\Project Files\\REVIT\\ARQUITETURA\\01_TEMPLATE\\MANUAL_SEPE_ARQUITETURA.pdf".format(
    usuario
)


def main():
    """Abre o manual PDF automaticamente."""
    try:
        if os.path.exists(manual_path):
            webbrowser.open(manual_path)
            script.exit()

        forms.alert(
            "Manual não encontrado!\n\n"
            "Usuário atual: {}\n"
            "Caminho buscado:\n{}\n\n"
            "Verifique se o arquivo existe neste local.".format(usuario, manual_path),
            title="Erro - Manual de modelagem",
        )
    except Exception as e:
        forms.alert("Erro ao abrir o manual:\n{}".format(str(e)), title="Erro")


if __name__ == "__main__":
    main()
