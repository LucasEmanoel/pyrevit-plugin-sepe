# -*- coding: utf-8 -*-
#! ironpython3

"""Verifica se as paredes possuem vãos (portas, janelas, aberturas) e atualiza o parâmetro."""

from Autodesk.Revit.DB import (
    FilteredElementCollector,
    Transaction,
    Wall
)

doc = __revit__.ActiveUIDocument.Document

PARAM_VAO = "Contem Vão"

def get_walls(doc):
    """Lista com todas as paredes do projeto."""
    return (
        FilteredElementCollector(doc)
        .OfClass(Wall)
        .WhereElementIsNotElementType()
        .ToElements()
    )

def verificar_e_definir_vao(wall):
    """Verifica se a parede possui inserções (vãos) e define o parâmetro como Sim ou Não."""
    param = wall.LookupParameter(PARAM_VAO)
    if param and not param.IsReadOnly:
        # ENCONTRA JANELAS E ABERTURAS NA PAREDE
        insercoes = wall.FindInserts(False, True, True, True)
        
        # Se a lista de inserções tiver elementos, tem vão!
        if len(insercoes) > 0:
            param.Set("Sim")
        else:
            param.Set("Não")
        return True
    return False

def main(doc):
    """Função principal."""
    walls = get_walls(doc)

    with Transaction(doc, "SEPE - Verificar Vãos nas Paredes") as t:
        t.Start()
        try:
            for wall in walls:
                verificar_e_definir_vao(wall)

            t.Commit()
            print("Processamento concluído com sucesso!")

        except Exception as ex:
            t.RollBack()
            print("Erro durante o processamento: {}".format(str(ex)))
            raise

if __name__ == "__main__":
    main(doc)