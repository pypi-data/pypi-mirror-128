from setuptools import setup

readme = open("./README.md", "r")


setup(
    name='TMPPA',
    packages=['TMPPA'],  # this must be the same as the name above
    version='0.1',
    description='Transfomación para Evaluación de modelos predictivos de la progresión acelerada de la Enfermedad Renal Crónica',
    long_description=readme.read(),
    long_description_content_type='text/markdown',
    author='Juan Carlos Guevara - Luis Hermogenes',
    author_email='',
    # use the URL to the github repo
    #url='',
    #download_url='https://github.com/nelsonher019/nelsonsaludo/tarball/0.1',
    #keywords=['testing', 'logging', 'example'],
    classifiers=[ ],
    license='MIT',
    include_package_data=True
)