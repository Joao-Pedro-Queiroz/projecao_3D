from setuptools import setup, find_packages


setup(
    name="projecao_3D",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["pygame", "numpy"],
    author="João Pedro Queiroz Viana",
    author_email="joaopqv@al.insper.edu.br, ",
    description="Uma biblioteca de projeção 3D.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Joao-Pedro-Queiroz/projecao_3D",
    entry_points={
        'console_scripts': [
            'projecao_3D=projecao_3D.main:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)