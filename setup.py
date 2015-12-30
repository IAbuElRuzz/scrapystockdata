from setuptools import setup, find_packages

setup(
    name='top100bot',
    version='1.0',
    packages=find_packages(),
    entry_points={'scrapy': ['settings = top100bot.settings']},
)
