from setuptools import setup, find_packages

setup(name="message_client_part",
      version="0.1",
      description="message_client_part",
      author="Geor Nick",
      author_email="jeziro@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
