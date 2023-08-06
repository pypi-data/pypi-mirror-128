from setuptools import setup


def readme():
    with open("README.rst", encoding="utf-8") as f:
        return f.read()


setup(name="simplelayout-github-onelazyfish", version="1.0.0",
      description="This is the assignment of IDRL",
      packages=["simplelayout", "simplelayout.generator", "simplelayout.cli"],
      author="onelazyfish", author_email="326042208@qq.com",
      url="https://github.com/onelazyfish", license="MIT",
      long_description=readme(),
      install_requires=["numpy", "matplotlib", "scipy"], entry_points={
        "console_scripts": ["simplelayout=simplelayout.__main__:main"],
    })
