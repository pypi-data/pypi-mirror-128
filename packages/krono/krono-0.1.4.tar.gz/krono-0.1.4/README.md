# Krono

Krono é um aplicativo de linha de comando para rastrear tempo e gerar relatórios em formato de fatura.

## Instalação

Utilize o package manager [pip](https://pip.pypa.io/en/stable/) para instalar o krono.

```bash
pip install krono
```

## Utilização

Para iniciar a contagem de horas é preciso rodar o comando `track`
informado o nome da atividade em que se está trabalhando

```shell
krono track "Nome da atividade"
```

Para gerar uma fatura, é preciso utilizar o comando `report` informando a data de início do relatório 
no formato `%Y-%m-%d`

```shell
krono report -s "2021-11-01"
```

Mais informações estão disponíveis ao rodar o comando

```shell
krono --help
```

## Utilizando um arquivo de configuração

A fim de facilitar a utilização, é possível criar um arquivo de configuração na pasta raiz do projeto 
chamado `rastreador.json`, com as variáveis de valor hora (`hourly_rate`), solicitante (`requested_from`) e
solicitado (`bill_to`)

```json
{
  "hourly_rate": 1000,
  "requested_from": "rafael.matsumoto@catolicasc.org.br",
  "bill_to": "catolicasc@catolicasc.org.br"
}
```

## Licença
[MIT](https://choosealicense.com/licenses/mit/)