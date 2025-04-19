import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime

import subalgoritmos.clima as clima
import subalgoritmos.db as db

class AnaliseTab(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.db_manager = db.DatabaseManager()
        self.configurar_aba()
    
    def configurar_aba(self):
        frame = ttk.LabelFrame(self, text="Análise de Condições Climáticas")
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ttk.Label(frame, text="Resultado da Análise:").grid(row=0, column=0, sticky=tk.NW, padx=10, pady=5)
        self.analise_text = scrolledtext.ScrolledText(frame, width=80, height=20, wrap=tk.WORD)
        self.analise_text.grid(row=1, column=0, columnspan=2, sticky=tk.EW, padx=10, pady=5)
        self.analise_text.config(state=tk.DISABLED)
        
        self.after(100, self.realizar_analise_clima)
    
    def realizar_analise_clima(self):
        try:
            dados_previsao = clima.obter_dados_climaticos(self.app.latitude, self.app.longitude)
            if not dados_previsao:
                return
            
            self.analise_text.config(state=tk.NORMAL)
            self.analise_text.delete(1.0, tk.END)
            
            
            self.analise_text.insert(tk.END, "Histórico climático\n\n")
            
            temp_atual = dados_previsao.get('current', {}).get('temperature_2m', 0)
            umidade_atual = dados_previsao.get('current', {}).get('relative_humidity_2m', 0)
            
            self.analise_text.insert(tk.END, f"Sensores de temperatura e umidade relativa apresentam uma média de {temp_atual:.1f}°C e {umidade_atual:.1f}%\n")
            
            estado_ideal = True
            if temp_atual > 35 or temp_atual < 10 or umidade_atual > 90 or umidade_atual < 20:
                estado_ideal = False
            
            if estado_ideal:
                self.analise_text.insert(tk.END, "Estado das plantações: ideal\n")
            else:
                self.analise_text.insert(tk.END, "Estado das plantações: em alerta\n")
            
            self.analise_text.insert(tk.END, "\n\nAnálise baseada na previsão do tempo\n\n")
            resultado_previsao = self.analisar_previsao_tempo(dados_previsao)
            self.analise_text.insert(tk.END, resultado_previsao)
            
            self.analise_text.config(state=tk.DISABLED)
        except Exception as e:
            print(f"Erro ao realizar análise: {str(e)}")
    
    def analisar_dados_historicos(self, dados_historicos):
        temp_total = 0
        umidade_total = 0
        precip_total = 0
        count = 0
        
        for dado in dados_historicos:
            if dado["temperatura"] is not None:
                temp_total += dado["temperatura"]
                count += 1
            
            if dado["umidade"] is not None:
                umidade_total += dado["umidade"]
            
            if dado["precipitacao"] is not None:
                precip_total += dado["precipitacao"]
        
        if count == 0:
            return "Não há dados históricos suficientes para análise."
        
        temp_media = temp_total / count
        umidade_media = umidade_total / count if count > 0 else 0
        
        resultado = ""
        avisos = []
        
        if temp_media > 35:
            avisos.append(f"⚠️ Temperatura média muito alta ({temp_media:.1f}°C). Pode prejudicar o desenvolvimento das plantas.")
        elif temp_media < 10:
            avisos.append(f"⚠️ Temperatura média muito baixa ({temp_media:.1f}°C). Pode retardar o crescimento das plantas.")
        else:
            avisos.append(f"✅ Temperatura média ({temp_media:.1f}°C) favorável para o plantio.")
        
        if precip_total > 50:
            avisos.append(f"⚠️ Precipitação acumulada alta ({precip_total:.1f}mm). Risco de encharcamento do solo.")
        elif precip_total < 10:
            avisos.append(f"⚠️ Precipitação acumulada baixa ({precip_total:.1f}mm). Pode ser necessário irrigação.")
        else:
            avisos.append(f"✅ Precipitação acumulada ({precip_total:.1f}mm) favorável para o plantio.")
        
        if umidade_media > 90:
            avisos.append(f"⚠️ Umidade relativa média muito alta ({umidade_media:.1f}%). Risco de doenças fúngicas.")
        elif umidade_media < 20:
            avisos.append(f"⚠️ Umidade relativa média muito baixa ({umidade_media:.1f}%). Pode ser necessário irrigação.")
        else:
            avisos.append(f"✅ Umidade relativa média ({umidade_media:.1f}%) favorável para o plantio.")
        
        resultado = "\n".join(avisos)
        
        if any("⚠️" in aviso for aviso in avisos):
            resultado += "\n\nRecomendação: Não é o momento ideal para plantio. Monitore as condições climáticas."
        else:
            resultado += "\n\nRecomendação: Condições favoráveis para plantio."
        
        return resultado
    
    def analisar_previsao_tempo(self, dados):
        if not dados or "daily" not in dados:
            return "Dados insuficientes para análise."
        
        diarios = dados["daily"]
        temp_max = diarios["temperature_2m_max"]
        temp_min = diarios["temperature_2m_min"]
        precipitacao = diarios["precipitation_sum"]
        
        temp_media = sum([(max_t + min_t) / 2 for max_t, min_t in zip(temp_max[:3], temp_min[:3])]) / 3
        precip_total = sum(precipitacao[:3])
        
        resultado = ""
        avisos = []
        
        if temp_media > 35:
            avisos.append(f"⚠️ Previsão de temperatura média alta ({temp_media:.1f}°C) para os próximos dias.")
        elif temp_media < 10:
            avisos.append(f"⚠️ Previsão de temperatura média baixa ({temp_media:.1f}°C) para os próximos dias.")
        else:
            avisos.append(f"✅ Previsão de temperatura média favorável ({temp_media:.1f}°C) para os próximos dias.")
        
        if precip_total > 50:
            avisos.append(f"⚠️ Previsão de precipitação acumulada alta ({precip_total:.1f}mm) para os próximos dias.")
        elif precip_total < 10:
            avisos.append(f"⚠️ Previsão de precipitação acumulada baixa ({precip_total:.1f}mm) para os próximos dias.")
        else:
            avisos.append(f"✅ Previsão de precipitação acumulada favorável ({precip_total:.1f}mm) para os próximos dias.")
        
        resultado = "\n".join(avisos)
        
        if any("⚠️" in aviso for aviso in avisos):
            resultado += "\n\nRecomendação: Não é o momento ideal para plantio. Aguarde condições mais favoráveis."
        else:
            resultado += "\n\nRecomendação: Previsão indica condições propícias para plantio nos próximos dias."
        
        return resultado
