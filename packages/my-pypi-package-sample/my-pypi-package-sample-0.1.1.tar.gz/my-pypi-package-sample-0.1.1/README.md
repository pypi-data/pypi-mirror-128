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
mkdir exam-x && cd exam-x
pyenv local 3.9.5
poetry init --no-interaction
poetry install
poetry shell
poetry add hello-xxx
vi exam.py
    from hello_xxx import print_this, main
    print_this()
python exam.py
poetry run hello-xxx
```