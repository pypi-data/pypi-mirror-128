from typing import Any, Dict
import json

from airflow.exceptions import AirflowFailException
from airflow.hooks.base import BaseHook
from airflow.models import Connection
from airflow.settings import Session


class SIAFIHook(BaseHook):
    '''Hook base para conexão com o SIAFI.

    :param id_conexao: referência para conexão
    :type id_conexao: str

    Uso
    ---
    O hook pode ser instanciado de duas formas, através de atribuição direta
    ou com a utilização de palavra-chave `with`. Aconselha-se utilizar a
    última por envolver rotina que verifica se a conta está ativa ou não.

    Importante destacar que o usuário é o responsável por informar ao banco de
    dados do Airflow as alterações que possam ocorrer na conta, incluindo
    alterações de senha, de nível e de autorização (ou bloqueio).

    .. code-block:: python
        :linenos:
        :caption: Exemplo de uso

        # Modo de instanciação 1
        hook = SIAFIHook('id_conexao')

        # Modo de instanciação 2
        with SIAFIHook('id_conexao') as hook2:
            # Realiza operações

        # Alteração de senha, nível e ativação
        hook.senha = 'nova senha'
        hook.nivel = 9
        hook.esta_ativo = False
    ---
    '''
    conn_name_attr = 'siafi_conn_id'
    default_conn_name = 'siafi_default'
    conn_type = 'siafi'
    hook_name = 'Conta do SIAFI'

    id_conexao: str

    def __init__(self, id_conexao: str) -> None:
        super().__init__()

        connection = self.get_connection(id_conexao)

        if connection.conn_type != self.conn_type:
            raise AirflowFailException(
                f'ID da conexão não é do tipo {self.conn_type}'
            )

        self.id_conexao = id_conexao

    def __enter__(self) -> 'SIAFIHook':
        if self.esta_ativo:
            return self

        raise AirflowFailException(
            f'Conta com CPF "{self.cpf}" não está ativa'
        )

    def __exit__(self, *args, **kwargs) -> None:
        return

    @property
    def cpf(self) -> str:
        connection = self.get_connection(self.id_conexao)
        return connection.login

    @property
    def senha(self) -> str:
        connection = self.get_connection(self.id_conexao)
        return connection.password

    @senha.setter
    def senha(self, valor: str) -> None:
        sessao = Session()

        conexao = sessao.query(Connection).filter(
            Connection.conn_id == self.id_conexao
        ).first()
        conexao.set_password(valor)

        sessao.add(conexao)
        sessao.commit()
        sessao.close()

    @property
    def nome(self) -> str:
        connection = self.get_connection(self.id_conexao)
        return connection.extra_dejson.get('extra__siafi__nome')

    @property
    def ug(self) -> str:
        connection = self.get_connection(self.id_conexao)
        return connection.extra_dejson.get('extra__siafi__ug')

    @property
    def nivel(self) -> int:
        connection = self.get_connection(self.id_conexao)
        return int(connection.extra.get('extra__siafi__nivel'), 0) or None

    @nivel.setter
    def nivel(self, valor: int) -> None:
        sessao = Session()

        conexao = sessao.query(Connection).filter(
            Connection.conn_id == self.id_conexao
        ).first()

        extra = conexao.extra_dejson
        extra.update({'extra__siafi__nivel': valor})

        conexao.set_extra(json.dumps(extra))

        sessao.add(conexao)
        sessao.commit()
        sessao.close()

    @property
    def esta_ativo(self) -> bool:
        connection = self.get_connection(self.id_conexao)
        return connection.extra_dejson.get('extra__siafi__esta_ativo')

    @esta_ativo.setter
    def esta_ativo(self, valor: bool) -> None:
        sessao = Session()

        conexao = sessao.query(Connection).filter(
            Connection.conn_id == self.id_conexao
        ).first()

        extra = conexao.extra_dejson
        extra.update({'extra__siafi__esta_ativo': valor})

        conexao.set_extra(json.dumps(extra))

        sessao.add(conexao)
        sessao.commit()
        sessao.close()

    @staticmethod
    def get_connection_form_widgets() -> Dict[str, Any]:
        '''Retorna formulário de conexão siafi'''
        from flask_appbuilder.fieldwidgets import BS3TextFieldWidget
        from flask_babel import lazy_gettext
        from wtforms import BooleanField, IntegerField, StringField, widgets

        return {
            'extra__siafi__nome': StringField(
                lazy_gettext('Nome Completo'),
                widget=BS3TextFieldWidget()
            ),
            'extra__siafi__ug': StringField(
                lazy_gettext('UG'),
                widget=BS3TextFieldWidget()
            ),
            'extra__siafi__nivel': IntegerField(
                lazy_gettext('Nível'),
                widget=BS3TextFieldWidget(),
            ),
            'extra__siafi__esta_ativo': BooleanField(
                lazy_gettext('Está ativo'),
                widget=widgets.CheckboxInput()
            )
        }

    @staticmethod
    def get_ui_field_behaviour() -> Dict:
        '''Customiza comportamento dos formulários.'''
        return {
            'hidden_fields': ['host', 'port', 'schema', 'extra',
                              'description'],
            'relabeling': {
                'conn_id': 'ID da conexão',
                'conn_type': 'Tipo de conexão',
                'login': 'CPF',
                'password': 'Senha'
            }
        }
