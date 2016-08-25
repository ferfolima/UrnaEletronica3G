# Urna Eletronica 3G
Urna Eletronica de 3 Geracao

##Sobre a Urna
Esse Software foi desenvolvido como um Trabalho de Conclusão de Curso da Universidade Federal do ABC.

Para ler mais informações sobre o processo de desenvolvimento e sobre o funcionamento do software, faça download do [paper](https://github.com/ferfolima/UrnaEletronica3G/blob/master/Urna_Eletronica_de 3a_Geracao_TCC.pdf)

##Modulos
###Setup de Eleicao
Podem ser cadastrados partidos, cargos e candidatos.
###Setup de Urna
Geração de chaves assimétricas para assinatura do voto.
###Votação
Eleitor vota nos candidatos de sua preferência.
###Verificação
Eleitor pode verificar se o voto impresso é realmente o que foi escolhido através da leitura do QR code.
###Apuração
Contagem de votos e impressão do boletim de urna.

##Uso
Note que há um arquivo main.py na raíz do projeto.
Ele é utilizado para fazer a chamada dos módulos.
```
python main.py --modulo <modulo>
```
As opções de módulo são:
- setupEleicao
- setupUrna
- votar
- verificar
- apurar
