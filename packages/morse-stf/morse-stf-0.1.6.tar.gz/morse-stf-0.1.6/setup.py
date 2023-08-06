import setuptools
import subprocess
from setuptools.command.install import install
import os

def _copy_cops():
    print("_compile_cops:", os.getcwd())
    home = os.environ['HOME']
    os.makedirs(home + '/stf_cops', exist_ok=True)
    subprocess.check_call('cp -r ./cops/* ~/stf_cops/', shell=True)
    cops_path = home + '/stf_cops/'
    print("cops_path=", cops_path)


class MorseSTFInstall(install):
    def run(self):
        super().run()
        _copy_cops()


setuptools.setup(
    name="morse-stf",
    version="0.1.6",
    author="Antchain-MPC Team",
    author_email="morse-stf@service.alipay.com",
    description="A Privacy Preserving Computation System",
    url="https://github.com/alipay/Antchain-MPC/morse-stf",
    license="Apache 2.0",
    install_requires=[
        'matplotlib==3.3.2',
        'tensorflow==2.2.0',
        'pandas==1.0.5',
        'sympy==1.6',
        'scikit-learn==0.23.1'
    ],


    entry_points={
        'console_scripts': [
            'morse-stf-server=stensorflow.engine.start_server:main',
        ],
    },
    cmdclass={
        'install': MorseSTFInstall,
    },
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    packages=setuptools.find_packages(include=['stensorflow', 'stensorflow.*']),
    python_requires=">=3.6",
)
