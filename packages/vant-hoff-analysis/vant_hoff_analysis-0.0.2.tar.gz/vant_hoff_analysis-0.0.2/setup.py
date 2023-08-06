from setuptools import setup

setup(
    name="vant_hoff_analysis",
    version="0.0.2",
    description="A small tool for performing van't Hoff analysis on PCT hydrogenation data",
    author="Max Gallant",
    packages=["vant_hoff_analysis", "tests"],
    install_requires=["numpy==1.20.2", "scipy==1.6.3"]
)