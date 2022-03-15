
# Cadeias de Markov na Simulação de um Jogo de Tênis

  

Este trabalho busca simular um jogo de tênis através de uma representação utilizando cadeias de Markov. Para isso, usamos uma estrutura similar à de um grafo para representar a cadeia, com nós e arestas.

  

## Instalação

Para executar as funcionalidades deste trabalho, será necessário ter o Python instalado. Para isso, basta acessa a [página de dowloads do Python](https://www.python.org/downloads/) e escolher o sistema operacional adequado.

Além disso, será necessário a instalação da biblioteca NumPy. Para isso, basta executar o seguinte comando no terminal:

  

	pip install numpy

  
  
## Execução
Após instaladas as dependências, execute o programa com

	python ./index.py

## Estruturas

  

Criamos uma estrutura de dados chamada **Node**, que representa cada estado da cadeia de Markov. Cada nó/estado possui uma pontuação correspondente, a qual está guardada no atributo ***label***.

Há ainda os atributos ***p*** e ***q*** que representam, respectivamente, a probabilidade dos jogadores ***A*** e ***B*** marcarem um ponto. Chamamos esses atributos de **ponteiros**. Inicialmente os nós/estados são criados especificando apenas o ***label*** e posteriormente os dois ponteiros são *setados* para poder referenciar outros nós/estados através da função ***pointers***.

![enter image description here](https://i.imgur.com/1Ha0JcK.png)

Além disso, há outras três estruturas importantes para armazenar as informações geradas pela simulação. São três estruturas do tipo ***dictionary*** do Python chamadas ***games***, ***sets*** e ***matches*** que guardam o número de vitórias de cada jogador nesses conjuntos de mesmo nome através das chaves "***A***" e "***B***" que representam os jogadores.

## Funções
A seguir descrevemos as funções mais importantes do programa. As demais funções estão divididas nos módulos log.py e matchStatistics.py que utilizam funções da biblioteca padrão do Python.
  

### *main(p, q, n_simm)*

É a função principal do programa. Os parâmetros ***p*** e ***q*** representam as probabilidades de vitória dos jogadores A e B, respecticamente. O parâmetro ***n_simm*** representa o número de simulações/partidas a serem realizadas. A função é responsável por criar as estruturas de dados e fazer as conexões entre os nós/estados da cadeia. Além disso, cria as estruturas de repetição para simular várias partidas, com vários sets com vários games. Para isso, faz uma verificação a cada ponto (na função ***simulacao***) para verificar se um game chegou ao fim. Quando um game é finalizado, é feita uma verificação para saber se o set chegou ao fim (função ***setVerify***). Por fim, quando um set chega ao fim, é verificado se a partida chegou a fim (função ***matchVerify***). Sempre que cada um desses conjuntos é chega ao fim (pontos, games, sets e matches), suas respectivas estruturas são devidamente preenchidas e é realizada a persistência das informações relevantes em arquivos através do módulo ***log***.

### *simulacao(players, node0, p, q)*

Realiza efetivamente a simulação que representa um game. O parâmetro players possui apenas as letras "**P**" e "**Q**" que representam os jogadores **A** e **B**, respectivamente. ***p*** e ***q*** representam as probabilidades dos jogadores **A** e **B** marcarem um ponto, respectivamente. ***node0*** representa o estado inicial da cadeia/game, quando nenhum jogador pontuou ainda (label "0-0"). A função caminha pela cadeia/grafo até encontrar o estado "***A Wins***" ou "***B Wins***", que marca o fim de um game. A cada ponto, sorteia um dos jogadores para pontuar através da probabilidade ponderada com a função ***random.choice*** da biblioteca **NumPy**. Registra cada ponto no histórico da partida e retorna o vencedor do game.


### *setVerify(games)*

Realiza a verificação para saber se um set terminou, analisando o número de games ganhos por cada jogador. O parâmetro ***games*** armazena o número de games ganhos por cada jogador. Um set termina quando um dos jogadores ganha 6 (quando está pelo menos dois games na frente do adversário) ou 7 (quando o jogo termina em 7x6 ou 7x5) games. Retorna o vencedor do set quando há um ou **0** caso contrário.

### *matchVerify(sets)*

Realiza a verificação para saber se uma partida (match) terminou, analisando o número de sets ganhos por cada jogador. O parâmetro ***sets*** armazena o número de sets ganhos por cada jogador. Uma partida termina quando um dos jogadores ganha 2 sets. Retorna o vencedor da partida quando há um ou **0** caso contrário.

  
  

## Análise

  

- **Qual a probabilidade do Jogador A/B vencerem as Partidas 1 e as Partidas 2? Para responder, considere Xi uma VA que representa o número de vitórias do jogador i em cada caso, e que nosso espaço amostral contem 3 partidas. Mostre uma análise estatística baseada em média e desvio padrão em cada caso.**

Os resultados dos cálculos estatísticos estão na tabela match_statistics.csv, na pasta results. Analisando os dados, vemos que eles fazem sentido dado o contexto e as condições iniciais da simulação. Em geral, na situação de Partida 1, onde o jogador A é bastante superior ao jogador B, o jogador A sempre vence tanto as partidas quanto os sets mas chega a perder alguns games, sendo que em uma das simulações o jogador B chegou a vencer 7,69% dos games disputados. Com relação à probabilidade de vitória do jogador A, ele obteve 100% para os sets e 100% para as partidas além de 92,31% para os games.

No cenário B, os dois jogadores estão equiparados em habilidade e, consequentemente, os resultados também ficam equiparados, o que é um comportamento esperado nesse caso. Entretanto, se as probabilidades p e q forem ligeiramente alteradas, os resultados se tornam bem destoantes. Esse comportamento, porém, também é esperado, já que mesmo com as chances de ambos os jogadores pontuarem serem próximas, isso não reflete necessariamente o resultado de uma partida. Ainda que o jogador B consiga pontuar diversas vezes e consiga ganhar vários games e vários sets, é preciso que haja uma combinação de games de um mesmo set e sets de uma mesma partida para que consiga efetivamente vencer um desses dois. Por esse motivo, os percentuais de vitória não se aproximam da distribuição de probabilidade com relação aos pontos nessas situações. No cenário simulado por nós (p = 0.5 e q = 0.5), tivemos resultados equilibrados, considerando um espaço amostral de 3 partidas: 66.6% de vitórias para o jogador A e 33.3% para o jogador B.

- **Qual a distribuição do número de sets, games e pontos nas Partidas 1 e 2? Mostre uma análise estatística baseada em média e desvio padrão em cada caso.**

Os resultados dos cálculos estatísticos estão na tabela match_dataset.csv, na pasta results. Os motivos que justificam os valores estão explicitados no item anterior.

- **Selecione aleatoriamente, com distribuição uniforme, 10 simulações dentre as n existentes em seus datasets originais. Refaça as 2 análises anteriores e explique as diferenças e semelhanças entre os resultados obtidos.**

Nesta situação, das 10 partidas escolhidas aleatoriamente, o jogador A venceu 7 e o jogador B, 3. Podemos notar que os percentuais de vitória são bem similares ao caso com espaço amostral de 3 partidas. Com um espaço amostral maior (10 partidas), a tendência é que os resultados se aproximem mais da distribuição de 50% de vitórias para cada jogador. Entretanto, como as partidas são escolhidas aleatoriamente, é possível que os percentuais sejam um pouco diferentes desses valores, como foi o nosso caso. Se observarmos o número de games, porém, vemos que os resultados ficam bem mais equilibrados (53.55% x 46.44%).
Os resultados dos cálculos estatísticos estão na tabela match_random_10_statistics.csv.

  

## Formato do *log*
O log, ou dataset, gerado pela execução do programa está no formato csv. Ele é responsável por armazenar todas as informações da execução do programa.
Ele sempre é gerado com nome de 'match_statistics.csv'. A primeira linha contém os cabeçalhos das colunas separados por vírgula e, nas linhas seguintes, os respectivos valores.
As informações de cada linha representam a evolução a cada game. Por exemplo, na linha 2 o jogador A venceu o 1º Game do 1º Set da 1ª Simulação da Partida 1.
![Exemplo de dataset](https://i.imgur.com/4na8w0o.png)