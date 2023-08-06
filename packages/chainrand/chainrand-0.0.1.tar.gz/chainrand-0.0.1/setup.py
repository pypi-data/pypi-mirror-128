from setuptools import setup, find_packages


setup(
    name='chainrand',
    version='0.0.1',
    license='MIT',
    author="Kang Yue Sheng Benjamin",
    author_email='chainrand@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/chainrand/chainrand-py',
    keywords='chainrand chainlink vrf provenance crypto blockchain nft opensea ethereum eth matic polygon academic integrity ipfs sha256 aes256',
    install_requires=[
        'pycrypto',
    ],
)

