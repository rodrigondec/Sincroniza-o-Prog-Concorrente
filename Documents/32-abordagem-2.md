# Abordagem 2

## Descrição

Essa abordagem utiliza apenas os [Locks](https://docs.python.org/3/library/threading.html#lock-objects) e [Variáveis Condicionais](https://docs.python.org/3/library/threading.html#condition-objects) ofertados pela biblioteca threading de python3.

Quanto à estrutura de dados, apenas uma lista foi utilizada para armazenar as pessoas esperando na fila para entrar no banheiro.

Os locks são usados para garantir exclusão mútua e as variáveis condicionais para evitar processamente inútil, fazendo com que uma thread durma.

Resumindo a lógica: há uma fila única na qual entram homens e mulheres. O banheiro ou está vazio ou comportando pessoas de um dos gêneros. Quando a primeira pessoa na fila é de um gênero diferente, espera-se o banheiro esvaziar para que entre.

Problemas de deadlock e livelock foram evitados por adquirir-se os recursos ordenadamente, bem como fazer com que uma thread durma quando não for executar operações significativas. Starvation

## Classes

* [Banheiro](#banheiro)
* [Pessoa](#pessoa)

### Banheiro

#### Atributos

| Nome do atributo | Descrição | Tipo |
| :--- | :--- | :--- |
| limite\_pessoas | quantidade de pessoas que cabem no banheiro | inteiro |
| limite\_pessoas\_por\_genero | quantidade máxima de pessoas de um gênero que podem usar o banheiro antes de trocar de gênero | inteiro |
| pessoas | contador da quantidade de pessoas do mesmo gênero que usaram o banheiro. É zerado quando gênero é trocado | inteiro |
| genero\_atual | Gênero das pessoas usando o banheiro em um dado momento. Pode assumir apenas 3 valores: "" \(quando vazio\), "F" ou "M" | Char |
| pessoas\_usando | Pessoas atualmente dentro do banheiro | List de Pessoa |
| fila | Armazena as pessoas que estão na fila, esperando para entrar no banheiro | List de Pessoa |
| finish | Determina quando o banheiro deve parar o loop principal. Setado para verdadeiro no loop principal, após todas as threads de Pessoa terminarem execução | Bool |

#### Atributos sincronização

| Nome do atributo condicional | Descrição | Tipo |
| :--- | :--- | :--- |
| fila\_lk | Lock que será adquirido quando uma Pessoa tenta entrar ou sair da fila | Lock |
| banheiro\_lk | Lock adquirido quando uma Pessoa tenta entrar no banheiro | Lock |
| fila\_cv | Variável Condicional que usa o Lock fila\_lk. É usado para fazer a thread atual esperar por uma determinada ação na fila \(Pessoa entrando ou terminar o loop principal\) | Condition |
| banheiro\_cv | Variável Condicional que usa o lock banheiro\_lk. É usado para fazer a thread atual esperar por uma determinada ação no banheiro \(esperar uma Pessoa sair ou entrar no banheiro\) | Condition |

#### Métodos

| Nome do método | Descrição |
| :--- | :--- |
| run | Corresponde ao loop principal do Banheiro. Será responsável por escolher a ação apropriada de acordo com a quantidade de pessoas na fila e no banheiro, e.g. acordar o primeiro da fila, mudar de gênero, esperar alguém entrar na fila ou esperar o banheiro esvaziar. Termina quando finish = True |
| end\_loop | Chamado pela thread principal para terminar a execução do método run. Seta a variável finish para True |
| notificar\_proximo | Supõe que tem pelo menos uma pessoa na fila. Se o banheiro estiver vazio, muda o gênero atual para o gênero da primeira pessoa na fila. Acorda a próxima pessoa com gênero igual ao do banheiro, independentemente da posição na fila. Incrementa o contador "pessoas" toda vida que notificar alguém |
| find\_next | Retorna o índice da primeira pessoa na fila com o gênero passado por parâmetro |
| trocar\_genero | Verifica se o banheiro está vazio. Se estiver, atribui o valor "" à genero\_atual. Caso contrário não faz nada |

#### Condições e fluxo

1. O banheiro começa sem gênero
2. O banheiro só tem uma fila, não qual entrarão pessoas dos dois gêneros
3. Quando o banheiro está vazio \(sem gênero\)
   1. Se a fila estiver vazia, espera alguém chegar
   2. Se tiver alguém na fila, atribua seu gênero ao banheiro
4. Quando o banheiro está cheio espere alguém sair
5. Quando tem gente na fila
   1. Se a primeira pessoa é do mesmo gênero do banheiro, incremente o contador e acorde-a
   2. Senão se o contador **não** atingiu o valor máximo, acorde a próxima pessoa do gênero do banheiro
   3. Senão espera o banheiro esvaziar \(gênero será trocado\)

### Pessoa

#### Atributos

| Nome do atributo | Descrição | Tipo |
| :--- | :--- | :--- |
| id\_pessoa | identificador da pessoa | inteiro |
| sexo | sexo da pessoa. 'M' ou 'F' | char |
| banheiro | Referência ao objeto banheiro que será utilizado | \#Banheiro |

#### Atributos sincronização

| Nome do atributo condicional | Descrição | Tipo |
| :--- | :--- | :--- |
| cv | Variável condicional com lock da fila de \#Banheiro \(fila\_lk\). É usada para adquirir exclusão mútua quando vai tentar sair e/ou entrar na fila. Também é usada para esperar vez de entrar no banheiro, e.g. primeiro na fila | Condition |

#### Métodos

| Nome do método | Descrição |
| :--- | :--- |
| run | Simula o comportamento da pessoa no escritório |
| trabalhar | Pessoa trabalhará por um tempo aleatório \(thread dormirá\) |
| entrar\_fila | Adquire lock da fila e se adiciona à ela. Notifica o banheiro que irá tomar uma ação pertinente de acordo com a situação atual \(método banheiro.run\). Dorme, esperando sua vez de entrar no banheiro |
| entrar\_banheiro | Se remove da fila de espera e se adiciona no banheiro. Notifica o banheiro para que tome uma ação pertinente, se necessário. Se esse método foi chamado, supões que há pelo menos uma vaga no banheiro |
| usar\_banheiro | Pessoa usará o banheiro por um tempo aleatório \(thread dormirá\) |
| sair | Pessoa adquire lock do banheiro e se remove dele. Chama método trocar\_genero do Banheiro. Notifica o banheiro que tomará uma ação caso necessário, e.g. banheiro está vazio |

#### Condições e fluxo

1. Cada pessoa trabalha por um tempo aleatório antes de usar o banheiro
2. Pessoa entra na fila, notifica banheiro \(pode estar dormindo caso a fila esteja vazia\) e espera ser acordada para entrar no banheiro
3. Pessoa entra no banheiro
4. Pessoa usa o banheiro \(thread dorme por tempo aleatório\)
5. Pessoa sai do banheiro e notifica o banheiro \(que pode estar dormindo caso estiver cheio\)



