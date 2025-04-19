import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_path="db.sqlite"):
        self.db_path = db_path
        self.inicializar_banco_dados()
    
    def inicializar_banco_dados(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS FarmTechDados (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_lote TEXT NOT NULL,
                    cultura INTEGER NOT NULL,
                    comprimento INTEGER NOT NULL,
                    largura INTEGER NOT NULL
                )
            ''')
            

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS DadosClimaticos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data TEXT NOT NULL,
                    temperatura REAL,
                    umidade REAL,
                    precipitacao REAL,
                    codigo_clima INTEGER,
                    descricao_clima TEXT,
                    velocidade_vento REAL
                )
            ''')
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Erro ao inicializar banco de dados: {str(e)}")
            raise
    
    def carregar_dados(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            

            cursor.execute("SELECT id, nome_lote, cultura, comprimento, largura FROM FarmTechDados")
            registros = cursor.fetchall()
            

            dados = []
            for registro in registros:
                dados.append({
                    "id": registro[0],
                    "nome_lote": registro[1],
                    "cultura": registro[2],
                    "comprimento": registro[3],
                    "largura": registro[4]
                })
            
            conn.close()
            return dados
        except Exception as e:
            print(f"Erro ao carregar dados: {str(e)}")
            return []
    
    def salvar_dados(self, nome_lote, cultura, comprimento, largura):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO FarmTechDados (nome_lote, cultura, comprimento, largura)
                VALUES (?, ?, ?, ?)
            """, (nome_lote, cultura, comprimento, largura))
            

            novo_id = cursor.lastrowid
            
            conn.commit()
            conn.close()
            
            return {
                "id": novo_id,
                "nome_lote": nome_lote,
                "cultura": cultura,
                "comprimento": comprimento,
                "largura": largura
            }
        except Exception as e:
            print(f"Erro ao salvar dados: {str(e)}")
            raise
    
    def atualizar_dados(self, registro_id, nome_lote, cultura, comprimento, largura):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE FarmTechDados 
                SET nome_lote = ?, cultura = ?, comprimento = ?, largura = ? 
                WHERE id = ?
            """, (nome_lote, cultura, comprimento, largura, registro_id))
            
            conn.commit()
            conn.close()
            
            return True
        except Exception as e:
            print(f"Erro ao atualizar dados: {str(e)}")
            raise
    
    def deletar_dados(self, registro_id):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM FarmTechDados WHERE id = ?", (registro_id,))
            
            conn.commit()
            conn.close()
            
            return True
        except Exception as e:
            print(f"Erro ao deletar dados: {str(e)}")
            raise
    
    def salvar_dados_climaticos(self, dados_atuais, dados_historicos=None):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            

            data_hora = dados_atuais["data"]
            temperatura = dados_atuais["temperatura"]
            umidade = dados_atuais.get("umidade")
            precipitacao = dados_atuais["precipitacao"]
            codigo_clima = dados_atuais["codigo_clima"]
            descricao_clima = dados_atuais["descricao_clima"]
            velocidade_vento = dados_atuais.get("velocidade_vento")
            

            cursor.execute("SELECT id FROM DadosClimaticos WHERE data = ?", (data_hora,))
            resultado = cursor.fetchone()
            
            if resultado:

                cursor.execute("""
                    UPDATE DadosClimaticos 
                    SET temperatura = ?, umidade = ?, precipitacao = ?, 
                        codigo_clima = ?, descricao_clima = ?, velocidade_vento = ? 
                    WHERE data = ?
                """, (temperatura, umidade, precipitacao, codigo_clima, descricao_clima, velocidade_vento, data_hora))
                mensagem = "Dados climáticos atualizados com sucesso!"
            else:

                cursor.execute("""
                    INSERT INTO DadosClimaticos 
                    (data, temperatura, umidade, precipitacao, codigo_clima, descricao_clima, velocidade_vento)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (data_hora, temperatura, umidade, precipitacao, codigo_clima, descricao_clima, velocidade_vento))
                mensagem = "Dados climáticos salvos com sucesso!"
            

            if dados_historicos:
                for dado in dados_historicos:
                    data = dado["data"]
                    temperatura = dado["temperatura"]
                    precipitacao = dado["precipitacao"]
                    codigo_clima = dado["codigo_clima"]
                    descricao_clima = dado["descricao_clima"]
                    
                    cursor.execute("SELECT id FROM DadosClimaticos WHERE data = ?", (data,))
                    resultado = cursor.fetchone()
                    
                    if not resultado:  
                        cursor.execute("""
                            INSERT INTO DadosClimaticos 
                            (data, temperatura, precipitacao, codigo_clima, descricao_clima)
                            VALUES (?, ?, ?, ?, ?)
                        """, (data, temperatura, precipitacao, codigo_clima, descricao_clima))
            
            conn.commit()
            conn.close()
            
            return mensagem
        except Exception as e:
            print(f"Erro ao salvar dados climáticos: {str(e)}")
            raise
            
    def obter_dados_climaticos_historicos(self, limite=10):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT data, temperatura, umidade, precipitacao, codigo_clima, descricao_clima, velocidade_vento
                FROM DadosClimaticos
                ORDER BY data DESC
                LIMIT ?
            """, (limite,))
            
            registros = cursor.fetchall()
            
            dados = []
            for registro in registros:
                dados.append({
                    "data": registro[0],
                    "temperatura": registro[1],
                    "umidade": registro[2],
                    "precipitacao": registro[3],
                    "codigo_clima": registro[4],
                    "descricao_clima": registro[5],
                    "velocidade_vento": registro[6]
                })
            
            conn.close()
            return dados
        except Exception as e:
            print(f"Erro ao obter dados climáticos históricos: {str(e)}")
            return []
