import setuptools

def load_long_description():
    with open('README.md') as readme:
        return readme.read()

setuptools.setup(
    name="pytest_agent",
    description="Service that exposes a REST API that can be used to interract remotely with Pytest. It is shipped with a dashboard that enables running tests in a more convenient way.",
    version="0.0.5",
    packages=setuptools.find_packages(),
    install_requires=["click", "fastapi", "uvicorn", "sqlalchemy"],
    entry_points={"console_scripts": ["pytest-agent=pytest_agent.__main__:cli"]},
    long_description=load_long_description(),
    long_description_content_type='text/markdown',
    include_package_data=True
)
