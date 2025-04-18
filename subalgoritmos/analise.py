from datetime import datetime

def analisar_cultura(dados, cultura_id):
    if cultura_id == 0:
        return analisar_impacto(dados, "Soja")
    elif cultura_id == 1:
        return analisar_impacto(dados, "Milho")
    else:
        return "Cultura não suportada para análise."

def analisar_impacto(dados, cultura):
    try:
        if not dados or "daily" not in dados:
            return "Dados insuficientes para análise."
        
        diarios = dados.get("daily", {})
        temp_max = diarios.get("temperature_2m_max", [])
        temp_min = diarios.get("temperature_2m_min", [])
        precipitacao = diarios.get("precipitation_sum", [])
        
        if not temp_max or not temp_min or not precipitacao:
            return "Dados insuficientes para análise."
        
        temp_media = sum([(max_t + min_t) / 2 for max_t, min_t in zip(temp_max, temp_min)]) / len(temp_max)
        precip_total = sum(precipitacao)
        precip_media = precip_total / len(precipitacao)
        
        analise = f"Análise de Impacto na Produção de {cultura}:\n\n"
        
        analise += analisar_temperatura(temp_media, cultura)
        analise += analisar_precipitacao(precip_total, precip_media, cultura)
        analise += "\nRecomendações:\n"
        analise += gerar_recomendacoes(temp_media, precip_total, precip_media, dados, cultura)
        
        return analise
    except Exception as e:
        print(f"Erro ao analisar impacto: {str(e)}")
        return "Erro ao analisar dados climáticos."

def analisar_temperatura(temp_media, cultura):
    if cultura == "Soja":
        if temp_media < 10:
            return f"⚠️ Temperatura média muito baixa ({temp_media:.1f}°C). Pode prejudicar a germinação e crescimento.\n"
        elif temp_media > 35:
            return f"⚠️ Temperatura média muito alta ({temp_media:.1f}°C). Pode causar aborto de flores e vagens.\n"
        else:
            return f"✅ Temperatura média ({temp_media:.1f}°C) favorável para o desenvolvimento.\n"
    else:  # Milho
        if 25 <= temp_media <= 30:
            return f"✅ Temperatura média ({temp_media:.1f}°C) está na faixa ideal para o desenvolvimento.\n"
        elif 20 <= temp_media < 25 or 30 < temp_media <= 35:
            return f"⚠️ Temperatura média ({temp_media:.1f}°C) está aceitável, mas não ideal para o desenvolvimento.\n"
        else:
            return f"⚠️ Temperatura média ({temp_media:.1f}°C) está fora da faixa ideal, podendo afetar o desenvolvimento.\n"

def analisar_precipitacao(precip_total, precip_media, cultura):
    if cultura == "Soja":
        if precip_total < 10:
            return f"⚠️ Precipitação total muito baixa ({precip_total:.1f} mm). Risco de déficit hídrico.\n"
        elif precip_total > 200:
            return f"⚠️ Precipitação total muito alta ({precip_total:.1f} mm). Risco de encharcamento e doenças fúngicas.\n"
        else:
            return f"✅ Precipitação total ({precip_total:.1f} mm) adequada para o desenvolvimento.\n"
    else:  # Milho
        if 4 <= precip_media <= 6:
            return f"✅ Precipitação média de {precip_media:.1f}mm/dia está na faixa ideal.\n"
        elif 2 <= precip_media < 4 or 6 < precip_media <= 8:
            return f"⚠️ Precipitação média de {precip_media:.1f}mm/dia está aceitável.\n"
        elif precip_media < 2:
            return f"⚠️ Precipitação média de {precip_media:.1f}mm/dia está abaixo do ideal.\n"
        else:
            return f"⚠️ Precipitação média de {precip_media:.1f}mm/dia está acima do ideal, podendo causar encharcamento.\n"

def gerar_recomendacoes(temp_media, precip_total, precip_media, dados, cultura):
    recomendacoes = []
    
    temp_atual = dados.get('current', {}).get('temperature_2m', 0)
    diarios = dados.get('daily', {})
    precipitacao = diarios.get('precipitation_sum', [])
    precip_recente = sum(precipitacao[-3:]) if len(precipitacao) >= 3 else sum(precipitacao)
    
    if cultura == "Soja":
        if temp_media < 10 or temp_media > 35:
            recomendacoes.append("Monitorar o desenvolvimento das plantas com maior frequência")
        
        if precip_total < 10:
            recomendacoes.append("Considerar irrigação suplementar se disponível")
            recomendacoes.append("Monitorar umidade do solo com sensores")
        elif precip_total > 200:
            recomendacoes.append("Verificar drenagem do solo")
            recomendacoes.append("Monitorar ocorrência de doenças fúngicas")
    else:  # Milho
        if temp_atual > 32:
            recomendacoes.append("Evite aplicação de defensivos nas horas mais quentes do dia")
        
        if precip_recente < 5:
            recomendacoes.append("Considerar irrigação suplementar nos próximos dias")
        elif precip_recente > 20:
            recomendacoes.append("Verificar a drenagem do solo para evitar encharcamento")
    
    if not recomendacoes:
        recomendacoes.append(f"Condições climáticas favoráveis para o desenvolvimento de {cultura.lower()}")
    
    return "- " + "\n- ".join(recomendacoes)
