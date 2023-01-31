from setuptools import setup, find_packages

setup(
    name='celebrityvoiceai',
    version='0.0.1',
    description='Celebrity Voice AI',
    author='Homen Shum',
    author_email='homenshum@gmail.com',
    url='https://github.com/HomenShum/CelebrityVoiceAI-Heroku',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'celebrityvoiceai = celebrityvoiceai.__main__:main',
        ],
    },
)
