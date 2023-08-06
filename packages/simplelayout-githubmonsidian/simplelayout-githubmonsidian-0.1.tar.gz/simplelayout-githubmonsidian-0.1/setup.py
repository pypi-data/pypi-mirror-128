from setuptools import setup

setup(
    name='simplelayout-githubmonsidian',
    version='0.1',
    author='LongYutong',
    author_email='403216817@qq.com',
    url='https://github.com/idrl-assignment/3-simplelayout-package-monsidian',
    description='再来一碗',
    packages=['simplelayout'],
    install_requires=['numpy', 'scipy', 'argparse', 'matplotlib', 'pytest', 'Pillow'],
    entry_points={
        'console_scripts': [
            'simplelayout=simplelayout:main'
        ]
    }
)
