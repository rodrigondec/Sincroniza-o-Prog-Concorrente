# Análise

## BoundedSemaphore

A utilização de BoundedSemaphore é uma boa prática quando é necessário o controle da quantidade de utilização de um recurso. 

Porém por si só não elimina a possibilidade de starvation caso haja uma grande requisição do recurso, pois ele libera um processo bloqueado aleatório independente da ordem de bloqueio. 

## Event

O Event é uma ótima solução para casos nos quais é necessário esperar uma condição específica para continuar seu fluxo. Não garante exclusão mútua e é utilizado apenas para sincronização entre as situações.   
Para implementar um 'lock' de região crítica com event, é necessário dois Events \('sua\_vez' e 'job\_done', por exemplo\) para cada processo juntamente com uma lista ou fila dos processos bloqueados. 

## Lock

O Lock é a solução ideal quando apenas um processo pode fazer uma operação\_x ao mesmo tempo. Porém não garante que o próximo processo a ser liberado seja o que foi bloqueado primeiro. Caso a ordem de chegada importe recomenda-se a utilização de uma fila.

## Condition



