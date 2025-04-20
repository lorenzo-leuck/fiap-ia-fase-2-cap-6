# FarmTech Solutions: Agricultura de Precisão para Enfrentar Mudanças Climáticas na Produção de Soja e Milho

## Problema

As mudanças climáticas representam um desafio significativo para a produção de soja e milho, com eventos climáticos extremos como secas prolongadas e chuvas excessivas impactando negativamente as safras. Essa variabilidade climática, combinada com a heterogeneidade natural dos solos, cria um cenário complexo que exige soluções tecnológicas avançadas para manter a produtividade e sustentabilidade.

## Solução

Para enfrentar esse desafio, implementamos um sistema de Agricultura de Precisão (AP) focado na cultura da soja e milho. Nossa solução integra:

1. Rede de sensores inteligentes para monitoramento de:
   - Temperatura
   - Umidade relativa
   - Níveis de nutrientes
   - 
2. Interface em Python que consome dados SQL do sistema de monitoramento, permitindo:
   - Gerenciamento de dados da lavoura
   - Suporte à tomada de decisão

# Guia de instalação

## Windows

1. Instale o Python 3.8 ou superior:
   - Baixe o instalador em [python.org](https://www.python.org/downloads/windows/)
   - Durante a instalação, marque a opção "Add Python to PATH"

2. Crie um ambiente virtual:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

4. Execute a aplicação:
   ```
   python app.py
   ```

## Linux

1. Instale o Python e o Tkinter:
   ```
   sudo apt update
   sudo apt install python3 python3-pip python3-venv python3-tk
   ```

2. Crie um ambiente virtual:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

4. Execute a aplicação:
   ```
   python3 app.py
   ```
## Benefícios

- Maior resiliência a eventos climáticos extremos
- Sustentabilidade ambiental e econômica

## Fundamentação Teórica

Como destacam Grego e Speranza et al. (2020), "a lavoura não é uniforme e possui variabilidade. Há regiões em lavouras com trechos que inundam com facilidade e outros que apresentam uma boa drenagem. Lavouras que podem variar de solo argiloso para solo arenoso, ou de solo mais ácido para menos ácido, e assim por diante, definindo características diferenciadas que implicam na variação da produtividade na mesma lavoura."

A Agricultura de Precisão permite superar essas limitações ao completar o ciclo fundamental de controle: leitura (sensores), análise (processamento de dados) e atuação (aplicação variável de insumos).

## Referência

Grego, C. R.; Speranza, E. A.; et al. Agricultura de precisão. In: BERNARDI, A. C. de C.; NAIME, J. de M.; RESENDE, A. V. de; BASSOI, L. H.; INAMASU, R. Y. (Ed.). Agricultura digital: pesquisa, desenvolvimento e inovação nas cadeias produtivas. Brasília, DF: Embrapa, 2020. p. 166-188. Disponível em: https://www.alice.cnptia.embrapa.br/handle/doc/1126213

# Uso da Plataforma

A interface da aplicação FarmTech Solutions é dividida em quatro abas principais:

## Entrada de Dados
Nesta aba você pode criar novos registros de lotes para monitoramento. Utilize este espaço para inserir informações sobre novas áreas de cultivo que deseja acompanhar.

## Lotes
Aqui você pode visualizar, editar ou excluir dados existentes dos lotes cadastrados. Esta seção permite o gerenciamento completo das informações já registradas no sistema.

## Clima
Esta aba apresenta o histórico climático e a previsão para os próximos sete dias. Utilize estas informações para planejar atividades agrícolas com base nas condições meteorológicas esperadas.

## Análise
Nesta seção você pode avaliar se as condições atuais são adequadas para o plantio. O sistema analisa os dados coletados e fornece recomendações sobre a viabilidade do cultivo nas condições presentes.

# Observações
O Schema dos dados é o mesmo da atividade anterior. Contudo,o Database da oracle não foi utilizado pois o breve guia de acesso remoto, apresentado no meio de uma das vídeoaulas, não funciona.