from setuptools import setup, find_packages


setup(
    name             = 'hanbert_tokenizer',
    version          = '0.1.6',
    description      = 'Hanbert Tokenizer',
    long_description = open('README.md').read(),
    author           = 'TwoBlockAI',
    author_email     = 'indexxlim@gmail.com',
    url              = 'https://github.com/tbai2019/HanBARTT',
    install_requires = [
        'torch>=1.7.1',
        'transformers>=4.3.3'],
    packages         = find_packages(),
    keywords         = ['hanbert', 'tokenizer', 'moran'],
    python_requires  = '>=3',
    zip_safe=False,
    include_package_data=True
)
