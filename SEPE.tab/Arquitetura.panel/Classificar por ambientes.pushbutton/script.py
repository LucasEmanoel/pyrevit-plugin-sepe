# -*- coding: utf-8 -*-
#! ironpython3

"""Classifica todas as paredes, pisos e telhados por ambiente."""

from Autodesk.Revit.DB import (
    XYZ,
    BuiltInParameter,
    FilteredElementCollector,
    Transaction,
    Wall,
    Floor,
    RoofBase
)

doc = __revit__.ActiveUIDocument.Document

OFFSET = 0.003
PARAM_AMBIENTE = "Ambiente"

##################################################################################
#####                                FLOOR                                  ######
##################################################################################
def get_floors(doc):
    """Lista com todos os pisos do projeto."""
    return (
        FilteredElementCollector(doc)
        .OfClass(Floor) # Corrigido para Floor
        .WhereElementIsNotElementType()
        .ToElements()
    )

def get_point_floor(floor):
    """Retorna um ponto levemente acima do centro do piso para entrar no ambiente."""
    bbox = floor.get_BoundingBox(None)
    if not bbox: return None
    
    x_mid = (bbox.Min.X + bbox.Max.X) / 2.0
    y_mid = (bbox.Min.Y + bbox.Max.Y) / 2.0
    # Usa o topo do Bounding Box e joga o offset para cima
    z_point = bbox.Max.Z + OFFSET 
    
    return XYZ(x_mid, y_mid, z_point)


##################################################################################
#####                                ROOF                                   ######
##################################################################################
def get_roofs(doc):
    """Lista com todos os telhados do projeto."""
    return (
        FilteredElementCollector(doc)
        .OfClass(RoofBase) # Corrigido para RoofBase
        .WhereElementIsNotElementType()
        .ToElements()
    )

def get_point_roof(roof):
    """Retorna um ponto levemente abaixo do centro do telhado para entrar no ambiente."""
    bbox = roof.get_BoundingBox(None)
    if not bbox: return None
    
    x_mid = (bbox.Min.X + bbox.Max.X) / 2.0
    y_mid = (bbox.Min.Y + bbox.Max.Y) / 2.0
    # Usa a base do Bounding Box e joga o offset para baixo
    z_point = bbox.Min.Z - OFFSET 
    
    return XYZ(x_mid, y_mid, z_point)


##################################################################################
#####                                WALLS                                  ######
##################################################################################
def get_walls(doc):
    """Lista com todas as paredes do projeto."""
    return (
        FilteredElementCollector(doc)
        .OfClass(Wall)
        .WhereElementIsNotElementType()
        .ToElements()
    )

def get_point(wall):
    """Retorna um ponto à frente da face externa da parede."""
    loc = wall.Location
    curve = loc.Curve

    tangent = curve.ComputeDerivatives(0.5, True).BasisX.Normalize()
    local_normal = XYZ(-tangent.Y, tangent.X, 0.0)

    if local_normal.DotProduct(wall.Orientation) < 0:
        local_normal = XYZ(-local_normal.X, -local_normal.Y, 0.0)

    offset = (wall.Width / 2.0) + OFFSET
    base_point = curve.Evaluate(0.5, True)
    point = base_point + local_normal.Multiply(offset)

    bbox = wall.get_BoundingBox(None)
    z_mid = (bbox.Min.Z + bbox.Max.Z) / 2.0

    return XYZ(point.X, point.Y, z_mid)

def get_phase(element, doc):
    """Pega fase de criação do elemento genérico."""
    phase_id = element.get_Parameter(BuiltInParameter.PHASE_CREATED).AsElementId()
    return doc.GetElement(phase_id)


def set_ambient(element, nome):
    """Define o parâmetro Ambiente do elemento."""
    param = element.LookupParameter(PARAM_AMBIENTE)
    if param and not param.IsReadOnly:
        param.Set(nome)
        return True
    return False

##################################################################################
#####                                AMBIENT                                ######
##################################################################################
def get_ambient(point, phase, doc):
    """Retorna o ambiente (room) no ponto dado."""
    return doc.GetRoomAtPoint(point, phase)


def get_element_level(room):
    """Retorna o nome do nível do ambiente."""
    level = room.Level
    if level:
        return level.Name
    return None


def get_element_name(element):
    """Retorna o nome do ambiente."""
    name_param = element.get_Parameter(BuiltInParameter.ROOM_NAME)
    if name_param and name_param.HasValue:
        return name_param.AsString()
    return "AMBIENTE SEM NOME"

##################################################################################
#####                               ENTRYPOINT                              ######
##################################################################################
def main(doc):
    """Função principal."""
    
    with Transaction(doc, "SEPE - Identificar Ambiente") as t:
        t.Start()
        try:
            # Dicionário de mapeamento: { Elementos: Função_para_pegar_ponto }
            element_map = {}
            
            for w in get_walls(doc): element_map[w] = get_point
            for f in get_floors(doc): element_map[f] = get_point_floor
            for r in get_roofs(doc): element_map[r] = get_point_roof

            for element, point_func in element_map.items():
                phase = get_phase(element, doc)
                if phase is None:
                    continue

                point = point_func(element)
                if point is None:
                    continue

                ambient = get_ambient(point, phase, doc)
                if ambient is None:
                    continue

                ambient_level = get_element_level(ambient)
                ambient_name = get_element_name(ambient)

                ambient_string = "{} - {}".format(ambient_level, ambient_name)
                set_ambient(element, ambient_string)

            t.Commit()

        except Exception as ex:
            t.RollBack()
            print("Erro durante o processamento: {}".format(str(ex)))
            raise


if __name__ == "__main__":
    main(doc)