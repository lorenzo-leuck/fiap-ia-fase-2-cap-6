# FarmTech Solutions: Agricultura de Precisão para Enfrentar Mudanças Climáticas na Produção de Soja

## Problema

As mudanças climáticas representam um desafio significativo para a produção de soja e milho, com eventos climáticos extremos como secas prolongadas e chuvas excessivas impactando negativamente as safras. Essa variabilidade climática, combinada com a heterogeneidade natural dos solos, cria um cenário complexo que exige soluções tecnológicas avançadas para manter a produtividade e sustentabilidade.

## Solução

Para enfrentar esse desafio, implementamos um sistema de Agricultura de Precisão (AP) focado na cultura da soja e milho. Nossa solução integra:

1. Rede de sensores inteligentes para monitoramento de:
   - Umidade do solo
   - pH do solo
   - Níveis de nutrientes

2. Sistema de coleta e análise de dados que permite:
   - Mapear a variabilidade espacial e temporal da lavoura
   - Identificar áreas com diferentes potenciais produtivos
   - Otimizar a aplicação de insumos conforme necessidade específica de cada área

3. Interface em Python que consome dados SQL do sistema de monitoramento, permitindo:
   - Visualização de dados em tempo real
   - Geração de mapas de recomendação
   - Suporte à tomada de decisão

## Benefícios

- Redução no uso de insumos agrícolas
- Aumento da produtividade
- Maior resiliência a eventos climáticos extremos
- Sustentabilidade ambiental e econômica

## Fundamentação Teórica

Como destacam Grego e Speranza et al. (2020), "a lavoura não é uniforme e possui variabilidade. Há regiões em lavouras com trechos que inundam com facilidade e outros que apresentam uma boa drenagem. Lavouras que podem variar de solo argiloso para solo arenoso, ou de solo mais ácido para menos ácido, e assim por diante, definindo características diferenciadas que implicam na variação da produtividade na mesma lavoura."

A Agricultura de Precisão permite superar essas limitações ao completar o ciclo fundamental de controle: leitura (sensores), análise (processamento de dados) e atuação (aplicação variável de insumos).

## Referência

Grego, C. R.; Speranza, E. A.; et al. Agricultura de precisão. In: BERNARDI, A. C. de C.; NAIME, J. de M.; RESENDE, A. V. de; BASSOI, L. H.; INAMASU, R. Y. (Ed.). Agricultura digital: pesquisa, desenvolvimento e inovação nas cadeias produtivas. Brasília, DF: Embrapa, 2020. p. 166-188. Disponível em: https://www.alice.cnptia.embrapa.br/handle/doc/1126213

## Observações
O Schema dos dados é o mesmo da atividade anterior. Contudo,o Database da oracle não foi utilizado pois o breve guia de acesso remoto, apresentado no meio de uma das vídeoaulas, não funciona.