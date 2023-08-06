# airflow-providers-siafi

Provider para interações com o SIAFI e seus sistemas derivados

## Instalação

```shell
pip install airflow-providers-siafi
```

## Conteúdo

- Hook e tipo de conexão "Conta do SIAFI"

![Imagem para conexão "Conta do SIAFI"](https://i.imgur.com/qA0kGB5.png)

## Uso

```python
from airflow.providers.siafi.hooks.siafi import SIAFIHook


with SIAFIHook('id_conexao') as hook:
    cpf = hook.cpf
    senha = hook.senha

    ...
```

