# Cadeias de Markov na Simulação de um Jogo de Tênis

Este trabalho busca simular um jogo de tênis através de uma representação utilizando cadeias de Markov. Para isso, usamos uma estrutura similar à de um grafo para representar a cadeia, com nós e arestas. 


## Estruturas

Criamos uma estrutura de dados chamada **Node**, que representa cada estado da cadeia de Markov. Cada nó/estado possui uma pontuação correspondente, a qual está guardada no atributo ***label***.
Há ainda os atributos ***p*** e ***q*** que representam, respectivamente, a probabilidade dos jogadores ***A*** e ***B*** marcarem um ponto. Chamamos esses atributos de **ponteiros**. Inicialmente os nós/estados são criados especificando apenas o ***label*** e posteriormente os dois ponteiros são *setados* para poder referenciar outros nós/estados através da função ***pointers***.

    class Node:
		def __init__(self, label):
		self.label = label
		self.p = None
		self.q = None
	def pointers(self, p, q):
		self.p = p
		self.q = q
Além disso, há outras três estruturas importantes para armazenar as informações geradas pela simulação. São três estruturas do tipo ***dictionary*** do Python chamadas ***games***, ***sets*** e ***matches*** que guardam o número de vitórias de cada jogador nesses conjuntos de mesmo nome através das chaves "***A***" e "***B***" que representam os jogadores.
## Funções

### *main(p, q, n_simm)*

É a função principal do programa. Os parâmetros ***p*** e ***q*** representam as probabilidades de vitória dos jogadores A e B, respecticamente. O parâmetro ***n_simm*** representa o número de simulações/partidas a serem realizadas. A função é responsável por criar as estruturas de dados e fazer as conexões entre os nós/estados da cadeia. Além disso, cria as estruturas de repetição para simular várias partidas, com vários sets com vários games. Para isso, faz uma verificação a cada ponto (na função ***simulacao***) para verificar se um game chegou ao fim. Quando um game é finalizado, é feita uma verificação para saber se o set chegou ao fim (função ***setVerify***). Por fim, quando um set chega ao fim, é verificado se a partida chegou a fim (função ***matchVerify***). Sempre que cada um desses conjuntos é chega ao fim (pontos, games, sets e matches), suas respectivas estruturas são devidamente preenchidas e é realizada a persistência das informações relevantes em arquivos através do módulo ***log***.

### *simulacao(players, node0, p, q)*
Realiza efetivamente a simulação que representa um game. O parâmetro players possui apenas as letras "**P**" e "**Q**" que representam os jogadores **A** e **B**, respectivamente. ***p*** e ***q*** representam as probabilidades dos jogadores **A** e **B** marcarem um ponto, respectivamente. A função caminha pela cadeia/grafo até encontrar o estado "***A Wins***" ou "***B Wins***", que marca o fim de um game.  A cada ponto, sorteia um dos jogadores para pontuar através da probabilidade ponderada com a função ***random.choice*** da biblioteca **NumPy**. Registra cada ponto no histórico da partida e retorna o vencedor do game.

### *setVerify(games)*
Realiza a verificação para saber se um set terminou, analisando o número de games ganhos por cada jogador. O parâmetro ***games*** armazena o número de games ganhos por cada jogador. Um set termina quando um dos jogadores ganha 6 (quando está pelo menos dois games na frente do adversário) ou 7 (quando o jogo termina em 7x6 ou 7x5) games. Retorna o vencedor do set quando há um ou **0** caso contrário.

### *matchVerify(sets)*
Realiza a verificação para saber se uma partida (match) terminou, analisando o número de sets ganhos por cada jogador. O parâmetro ***sets*** armazena o número de sets ganhos por cada jogador. Uma partida termina quando um dos jogadores ganha 2 sets. Retorna o vencedor da partida quando há um ou **0** caso contrário.


## Análise

 - **Qual a probabilidade do Jogador A/B vencerem as Partidas 1 e as Partidas 2? Para responder, considere Xi uma VA que representa o número de vitórias do jogador i em cada caso, e que nosso espaço amostral contem 3 partidas. Mostre uma análise estatística baseada em média e desvio padrão em cada caso.**
 Os resultados dos cálculos estatísticos estão na tabela X.
 
 - **Qual a distribuição do número de sets, games e pontos nas Partidas 1 e 2? Mostre uma análise estatística baseada em média e desvio padrão em cada caso.**
 Os resultados dos cálculos estatísticos estão na tabela Y.
 
 - **Selecione aleatoriamente, com distribuição uniforme, 10 simulações dentre as n existentes em seus datasets originais. Refaça as 2 análises anteriores e explique as diferenças e semelhanças entre os resultados obtidos.**
Os resultados dos cálculos estatísticos estão na tabela Z.

## Formato do *log*
