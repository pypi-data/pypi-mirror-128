from setuptools import setup,find_packages

classifiers = [
    '',
    ''
]

setup(
    name='uitools',
    version='0.0.2',
    description='UITools project',
    long_description= open('CHANGELOG.txt').read,
    url='https://github.com/criojag/UITools',
    author='César Rioja García',
    author_email='criojag1200@alumno.ipn.mx',
    license='MIT',
    classifiers=classifiers,
    keywords='seaborn',
    packages=find_packages(),
    install_requires=['seaborn','scikit-learn','matplotlib'],
)