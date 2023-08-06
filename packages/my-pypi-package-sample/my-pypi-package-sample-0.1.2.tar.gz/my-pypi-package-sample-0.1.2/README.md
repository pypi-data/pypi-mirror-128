# Package for PyPI

#### 1. update codes

#### 2. update the version

```
poetry version 0.1.2
```

#### 3. build

```
poetry build
```

#### 4. push to test pypi then test

```
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry publish -r testpypi
```

#### 5. push to pypi then test

```
poetry publish
```

#### 6. test

```
mkdir test_proj && cd test_proj
pyenv local 3.9.5
poetry init --no-interaction
poetry install
poetry shell
poetry add my-pypi-package-sample

# Create python file then run
vi exam.py
--------------------------------------------
from my_pypi_package_sample import print_hello
print_hello()
--------------------------------------------
python exam.py

# Run the package from script
poetry run my-pypi-package-sample
```
