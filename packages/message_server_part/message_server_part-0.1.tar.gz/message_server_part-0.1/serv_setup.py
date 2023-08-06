from setuptools import setup, find_packages

setup(name="message_server_part",
      version="0.1",
      description="message_server_part",
      author="Geor Nick",
      author_email="jeziro@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )