import setuptools
import heroku


setuptools.setup(
    version=heroku.__version__,
    description="Heroku api connector",
    name="heroku_api",
    author="borisd93",
    author_email="x93bd0@gmail.com",
    url="https://github.com/borisd93/heroku",
    packages=["heroku"]
)
