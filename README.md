# Sistema do EB
**Software for Military**

INSTALAÇÃO
----------
DEP:

    tablib, django, diff_match_patch

PYTHON:

    pip install -r requirements.txt

INICIAR O BANCO DE DADOS
------------------------
Construir a migração do Banco de Dados:

    python manage.py makemigrations

Migrar os dados para o Banco de Dados:

    python manage.py migrate

CARREGAR OS ARQUIVOS
--------------------
Sempre que alteramos alguma arquivo media:

    python manage.py collectstatic

INICIAR
-------
Iniciamos o sistema:

    python manage.py runserver 0.0.0.0:80

Podemos Criar um SUPERUSER para o Admin:

    python manage.py createsuperuser

EXEMPLO
-------
Abra no navegador o seguinte link [Servidor PythonAnyWhere](http://teofanesp12.pythonanywhere.com)