import requests
from datetime import datetime

API_URL = "https://api.open-meteo.com/v1/forecast"

def traduzir_codigo_clima(codigo):
    traducoes = {
        0: "céu limpo",
        1: "principalmente limpo",
        2: "parcialmente nublado",
        3: "nublado",
        45: "neblina",
        48: "neblina com depósito de geada",
        51: "garoa leve",
        53: "garoa moderada",
        55: "garoa intensa",
        56: "garoa congelante leve",
        57: "garoa congelante intensa",
        61: "chuva fraca",
        63: "chuva moderada",
        65: "chuva forte",
        66: "chuva congelante leve",
        67: "chuva congelante forte",
        71: "queda de neve leve",
        73: "queda de neve moderada",
        75: "queda de neve forte",
        77: "grãos de neve",
        80: "pancadas de chuva leves",
        81: "pancadas de chuva moderadas",
        82: "pancadas de chuva violentas",
        85: "pancadas de neve leves",
        86: "pancadas de neve fortes",
        95: "tempestade",
        96: "tempestade com granizo leve",
        99: "tempestade com granizo forte"
    }
    
    if codigo in traducoes:
        return traducoes[codigo]
    else:
        return f"Código desconhecido: {codigo}"

def obter_dados_climaticos(latitude, longitude):
    try:
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m",
            "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum",
            "timezone": "America/Sao_Paulo",
            "past_days": 7,
            "forecast_days": 7
        }
        
        response = requests.get(API_URL, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erro ao obter dados climáticos: {response.status_code}")
            return None
    except Exception as e:
        print(f"Erro ao conectar à API de clima: {str(e)}")
        return None

def formatar_dados_atuais(dados):
    try:
        atual = dados["current"]
        

        codigo_clima = atual["weather_code"]
        descricao = traduzir_codigo_clima(codigo_clima)
        data_hora = datetime.fromisoformat(atual["time"].replace('Z', '+00:00')).strftime("%d/%m/%Y %H:%M")
        
        texto = f"Data e hora: {data_hora}\n"
        texto += f"Condição: {descricao}\n"
        texto += f"Temperatura: {atual['temperature_2m']}°C\n"
        texto += f"Umidade: {atual['relative_humidity_2m']}%\n"
        texto += f"Precipitação: {atual['precipitation']} mm\n"
        texto += f"Velocidade do vento: {atual['wind_speed_10m']} km/h\n"
        

        dados_formatados = {
            "data": atual["time"],
            "temperatura": atual["temperature_2m"],
            "umidade": atual["relative_humidity_2m"],
            "precipitacao": atual["precipitation"],
            "codigo_clima": codigo_clima,
            "descricao_clima": descricao,
            "velocidade_vento": atual["wind_speed_10m"]
        }
        
        return texto, dados_formatados
    except Exception as e:
        print(f"Erro ao formatar dados atuais: {str(e)}")
        return "Erro ao processar dados climáticos", None

def formatar_dados_historicos(dados):
    try:
        diarios = dados["daily"]
        datas = diarios["time"]
        temp_max = diarios["temperature_2m_max"]
        temp_min = diarios["temperature_2m_min"]
        precipitacao = diarios["precipitation_sum"]
        codigos_clima = diarios["weather_code"]
        
        dados_tabela = []
        dados_banco = []
        
        # Pegar apenas os dados históricos (primeiros 7 dias)
        for i in range(7):
            data_formatada = datetime.fromisoformat(datas[i]).strftime("%d/%m/%Y")
            descricao = traduzir_codigo_clima(codigos_clima[i])
            
            dados_tabela.append({
                "data": data_formatada,
                "temp_max": f"{temp_max[i]:.1f}",
                "temp_min": f"{temp_min[i]:.1f}",
                "precipitacao": f"{precipitacao[i]:.1f}",
                "clima": descricao
            })
            
            dados_banco.append({
                "data": datas[i],
                "temperatura": (temp_max[i] + temp_min[i]) / 2,  # Média das temperaturas
                "precipitacao": precipitacao[i],
                "codigo_clima": codigos_clima[i],
                "descricao_clima": descricao
            })
        
        return dados_tabela, dados_banco
    except Exception as e:
        print(f"Erro ao formatar dados históricos: {str(e)}")
        return [], []

def formatar_dados_previsao(dados):
    try:
        diarios = dados["daily"]
        datas = diarios["time"]
        temp_max = diarios["temperature_2m_max"]
        temp_min = diarios["temperature_2m_min"]
        precipitacao = diarios["precipitation_sum"]
        codigos_clima = diarios["weather_code"]
        
        dados_tabela = []
        
        for i in range(7, len(datas)):
            data_formatada = datetime.fromisoformat(datas[i]).strftime("%d/%m/%Y")
            descricao = traduzir_codigo_clima(codigos_clima[i])
            
            dados_tabela.append({
                "data": data_formatada,
                "temp_max": f"{temp_max[i]:.1f}",
                "temp_min": f"{temp_min[i]:.1f}",
                "precipitacao": f"{precipitacao[i]:.1f}",
                "clima": descricao
            })
        
        return dados_tabela
    except Exception as e:
        print(f"Erro ao formatar dados de previsão: {str(e)}")
        return []

def analisar_impacto_soja(dados):
    try:
        if not dados or "daily" not in dados:
            return "Dados insuficientes para análise."
        
        diarios = dados["daily"]
        temp_max = diarios["temperature_2m_max"]
        temp_min = diarios["temperature_2m_min"]
        precipitacao = diarios["precipitation_sum"]
        

        temp_media = sum([(max_t + min_t) / 2 for max_t, min_t in zip(temp_max, temp_min)]) / len(temp_max)
        precip_total = sum(precipitacao)
        precip_media = precip_total / len(precipitacao)
        

        analise = "Análise de Impacto na Produção de Soja:\n\n"
        

        if temp_media < 10:
            analise += "⚠️ Temperatura média muito baixa (%.1f°C). Pode prejudicar a germinação e crescimento da soja.\n" % temp_media
        elif temp_media > 35:
            analise += "⚠️ Temperatura média muito alta (%.1f°C). Pode causar aborto de flores e vagens na soja.\n" % temp_media
        else:
            analise += "✅ Temperatura média (%.1f°C) favorável para o desenvolvimento da soja.\n" % temp_media
        

        if precip_total < 10:
            analise += "⚠️ Precipitação total muito baixa (%.1f mm). Risco de déficit hídrico para a soja.\n" % precip_total
        elif precip_total > 200:
            analise += "⚠️ Precipitação total muito alta (%.1f mm). Risco de encharcamento e doenças fúngicas.\n" % precip_total
        else:
            analise += "✅ Precipitação total (%.1f mm) adequada para o desenvolvimento da soja.\n" % precip_total
        

        analise += "\nRecomendações:\n"
        if temp_media < 10 or temp_media > 35:
            analise += "- Monitorar o desenvolvimento das plantas com maior frequência\n"
        
        if precip_total < 10:
            analise += "- Considerar irrigação suplementar se disponível\n"
            analise += "- Monitorar umidade do solo com sensores\n"
        elif precip_total > 200:
            analise += "- Verificar drenagem do solo\n"
            analise += "- Monitorar ocorrência de doenças fúngicas\n"
        
        return analise
    except Exception as e:
        print(f"Erro ao analisar impacto na soja: {str(e)}")
        return "Erro ao analisar dados climáticos."
