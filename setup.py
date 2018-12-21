from setuptools import setup, find_packages

setup(
    name="resttest",
    version="0.2",
    packages=find_packages(exclude=["test*"]),
    include_package_data=True,
    install_requires=["fire", "requests"],
    entry_points="""
        [console_scripts]
        resttest=resttest.main:main
    """,
)
