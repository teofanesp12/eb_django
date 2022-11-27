# Sistema do EB
**Software for Military**

INSTALAÇÃO
----------
DEPENDENCIAS:

    tablib, django, diff_match_patch, PyPDF2, Pillow

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

COMPILAR TRADUÇÃO
-----------------
Sempre que alteramos algum arquivo de tradução:

    python manage.py compilemessages

INICIAR
-------
Iniciamos o sistema:

    python manage.py runserver 0.0.0.0:80

Podemos Criar um SUPERUSER para o Admin:

    python manage.py createsuperuser

DATA DEFAULT
------------
Arquivos padrão para importação estão na pasta ´data/´

EXEMPLO
-------
Abra no navegador o seguinte link [Servidor PythonAnyWhere](http://teofanesp12.pythonanywhere.com)