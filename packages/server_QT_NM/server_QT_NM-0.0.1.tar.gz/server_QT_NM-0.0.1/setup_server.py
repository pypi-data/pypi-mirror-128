from setuptools import setup, find_packages

setup(name="server_QT_NM",
      version="0.0.1",
      description="server",
      author="Mamicheva Natalya",
      author_email="mamicheva.natalya@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
