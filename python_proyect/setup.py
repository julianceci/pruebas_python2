# Se utiliza para poder crear un paquete y lugo instalarlo con pip
# Ejecutar esto para la creación: python3 setup.py sdist bdist_wheel
# Luego pip install con los archivos del directorio dist!

# Import needed function from setuptools
from setuptools import setup, find_packages

# Create proper setup to be used by pip
setup(
    name='my_package',
    version='0.0.1',
    description='Comportamiento a definir',
    author='My',
    packages=find_packages(),  # Automatically find all packages and subpackages
    install_requires=[
        'matplotlib>=3.0.0',
        # Puedes añadir más dependencias aquí
    ],
    extras_require={
        'dev': [
            'pytest>=6.0.0',  # Dependencias adicionales para desarrollo
            # Puedes añadir más herramientas para el desarrollo
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
