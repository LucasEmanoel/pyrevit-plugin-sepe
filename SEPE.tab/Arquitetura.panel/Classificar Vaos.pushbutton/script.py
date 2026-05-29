# -*- coding: utf-8 -*-
#! ironpython3

"""Verifica se as paredes possuem vãos e atualiza o parâmetro do tipo Sim/Não."""

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
    param = wall.LookupParameter(PARAM_VAO)
    if param and not param.IsReadOnly:
        insercoes = wall.FindInserts(False, True, True, True)
        
        if len(insercoes) > 0:
            param.Set(1)
        else:
            param.Set(0)
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