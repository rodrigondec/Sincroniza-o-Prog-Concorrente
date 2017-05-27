# Dificuldades Encontradas

Uma dificuldade encontrada foi dividir e separar os diferentes estados e condições das threads/objetos/rotinas/programa para fazer de fato a sincronização entre as threads. Como por exemplo a modelagem da montanha-russa, na qual os passageiros entrarem/saírem do carro em determinados estados do carro.



Outra dificuldade foi que durante a execução do programa no banheiro unissex. Um dos sexos do banheiro entrava em starvation caso o tempo de "trabalho" e a quantidade de trabalhadores fossem muito superior à quantidade de vagas do banheiro. Precisando por causa disso, implementar um algoritmo que garantisse a justiça entre a divisão do banheiro entre os dois possíveis gêneros.

