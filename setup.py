from setuptools import setup, find_packages

setup(
    name='algo_async_api',
    version='0.0.1',
    description='Algoritmika Student API\nАсинхронная библиотека для Работы с Бекэндом платформы Algoritmika',
    long_description="Algoritmika Student API\nАсинхронная библиотека для Работы с Бекэндом платформы Algoritmika\nСозданна на Основе Algo_api Sync Version: https://github.com/moontr3/algo_api/",
    author='VOLT_SYNAPSE, moontr3, justdont0',
    packages=find_packages(),
    install_requires=['aiohttp'],
    zip_safe=False
)