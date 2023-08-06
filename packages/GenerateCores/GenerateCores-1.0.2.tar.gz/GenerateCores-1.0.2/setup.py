from distutils.core import setup
setup(
    name='GenerateCores',
    version='1.0.2',
    description='The data generated',
    py_modules=['generation', 'synthetic_data'],
    package_data={'fits': ['*.fits'], 'FIT': ['*.FIT']},
    author='Zhou Guangrong',
    author_email='1971987925@qq.com',
    long_description='The simulation data generateion, including simulation data and synthetic data'
)
