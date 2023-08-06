## Informações
Este módulo foi desenvolvido com o intuito de auxiliar as pessoas de coletar informações relacionadas as suas aplicações hospedadas na https://squarecloud.app!

## Instalação
```
pip install squarecloud
```

## Forma de uso padrão em Python

```python
from squarecloud import Square

print(Square.ram())  # 23/100MB
print(Square.used_ram())  # 23
print(Square.total_ram())  # 100

```

## Forma de uso avançado em Python

```python
from squarecloud import Square

# Com conversão de MB(MegaBytes) para GB(GigaBytes) e com unidade de medida.
print(Square.ram(formatted=True))  # 1.23GB/2.50GB
print(Square.used_ram(formatted=True))  # 1.23GB
print(Square.total_ram(formatted=True))  # 2.50GB

# Sem conversão de B(Bytes) para MB(MegaBytes) e sem unidade de medida.
print(Square.used_ram(raw=True))  # 1320702443.52
print(Square.total_ram(raw=True))  # 2684354560

```

## Caso ocorra algum erro, será retornado o seguinte:

```python
print(Square.used_ram())  # [Errno 2] No such file or directory: 'Não foi possível encontrar os dados solicitados!'

```

## LICENSE
Este projeto está licenciado sob a Licença Apache License 2.0
