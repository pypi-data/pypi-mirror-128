from setuptools import setup

setup(
    version='0.2.11',
    name = 'tradeanal',
    description='tradeanal',
    author='cherepanov_max95',
    author_email='cherepanov@ku66.ru',
    install_requires=[
        'multiprocess',
        'nevergrad',
        'pandas',
        'matplotlib'
    ],
    include_package_data=True,
    zip_safe=False,
    packages=['tradeanal']
)