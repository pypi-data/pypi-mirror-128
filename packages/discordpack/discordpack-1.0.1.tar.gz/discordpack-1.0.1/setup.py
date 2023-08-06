from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='discordpack',
    version='1.0.1',
    license='MIT',
    url='https://github.com/DarthOCE/discordpack',
    author='DarthOCE',
    author_email = 'darthocelogging@gmail.com',
    description='Installs nessersary and useful packages for discord bot python development.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=[],
    install_requires=['discord.py>=1.7.3', 'discord_components', 'discord-py-slash-command'],
    classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
