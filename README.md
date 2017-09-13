# Urna Eletrônica 3G

Urna Eletrônica de 3° Geração

## Sobre a Urna

Esse software foi desenvolvido como um Trabalho de Conclusão de Curso da Universidade Federal do ABC.

Para ler mais informações sobre o processo de desenvolvimento e sobre o funcionamento do software, faça download do [paper](https://github.com/ferfolima/UrnaEletronica3G/blob/master/Urna_Eletronica_de 3a_Geracao_TCC.pdf)

## Módulos

### Setup de Eleição

Podem ser cadastrados partidos, cargos e candidatos.

### Setup de Urna

Geração de chaves assimétricas para assinatura do voto.

### Votação

Eleitor vota nos candidatos de sua preferência.

### Verificação

Eleitor pode verificar se o voto impresso é realmente o que foi escolhido através da leitura do QR code.

### Apuração

Contagem de votos e impressão do boletim de urna.

## Uso

Note que há um arquivo `main.py` na raiz do projeto. Ele é utilizado para fazer a chamada dos módulos.

```
python main.py --modulo <modulo>
```

As opções de módulo são:

- `setupEleicao`
- `setupUrna`
- `votar`
- `verificar`
- `apurar`
