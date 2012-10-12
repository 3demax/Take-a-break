from distutils.core import setup

setup(
    name='Take a Break',
    version='0.1dev',
    packages=['take_a_break',],
    package_data={'take_a_break': ['data/good.glade']},
    scripts = ['tb'],
    license='WTFPL (Do What The Fuck You Want To Public License)',
    long_description=open('README.md').read(),
)
