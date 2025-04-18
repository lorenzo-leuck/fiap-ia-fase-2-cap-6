CULTURAS = {0: "Soja", 1: "Milho"}

def calcular_area(comprimento, largura):
    return comprimento * largura

def calcular_insumos(area, cultura):
    insumos_por_cultura = {
    0: {"nome": "Glifosato", "taxa": 1200, "descrição": "Herbicida para controle de ervas daninhas"},
    1: {"nome": "NPK 20-10-10", "taxa": 200, "descrição": "Fertilizante para desenvolvimento da planta"}
    }
    insumo_info = insumos_por_cultura[cultura]
    quantidade = area * insumo_info["taxa"]
    
    return {
        "nome": insumo_info["nome"],
        "taxa": insumo_info["taxa"],
        "quantidade_total": quantidade
    }
