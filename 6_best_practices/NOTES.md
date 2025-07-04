**Links**
* [unit 6 repo](https://github.com/DataTalksClub/mlops-zoomcamp/tree/main/06-best-practices)
* This unit discusses various best practices in ML Ops, e.g. testing with Pytest, AWS service testing locally, 

**6.1 Testing Python code with Pytest**
* **Goal**: Integrate the streaming code from Unit 4 with unit test and integration test.
* **Setup**:
    * Create env:
        ```bash
        pipenv install boto3 mlflow scikit-learn
        pipenv install --dev pytest deepdiff pylint black isort pre-commit 
        ```
    * Activate env: `pipenv shell`. Cross check installed packages in virtual env using `pip list`.
    * Configure VSCode for running tests:
        * Download the `Python extension for VSCode` in extensions if you don't have it.
        * In Mac: `Cmd + Shift + P` > `Python: Select Interpreter`. Note to exit venv first before so.
        * In terminal, execute `pipenv --venv` and copy-paste the venv in this format `<venv>/bin/python` into the interpreter. This will add the venv's python env into your interpreter to be selected.
        * Try `Cmd + Shift + P` > `Python: Select Interpreter` again, you should be able to see `<venv>/bin/python`. Select this. 
        * Now you should see a few new icons including the `Testing` icon (flask icon) in the VSCode left panel. when you click on it, you can see buttons like `Configure Python Tests` and `Install Additional Test Extensions`.
    * Activate venv: `pipenv shell`.
    * Execute `which pytest`. You should see `<venv>/bin/pytest`.
    * Create new subfolder e.g. `tests` to contain your test scripts.
    * Go to `Testing` icon > `Configure Python Tests` > `pytest framework` > select the `tests` subfolder created earlier.
* **To prepare tests**, you could create test scripts in `tests` folder e.g. `model_test.py`. Each test case should:
    * In its own method with naming convention `test_`.
    * End with an assert statement to compare actual result and expected result.
* To execute tests,
    * In `Testing` icon, click on `Run Tests` icon.
* **To change the testing folder**,
    * `Cmd + Shift + P` > `Preferences: Open Workspace Settings (JSON)`.
    * Update or replace 
    ```bash
    "python.testing.pytestArgs": [
        "your_test_directory"
    ]
    ```
    * In `Testing` icon, click on refresh button to refresh the directory and retrieve the test cases defined there.
* **Note**: The lecture reuses codes from Unit 4 and uses AWS Lambda + Kinesis, then modified and ran tests in Docker. See references below for basics on test cases setup without all the complexities.
* **References**:
    * [Setting up unit tests in Python with VSCode](https://youtu.be/-PHBRzL80Lk?si=sGJFopXetcPdD8np)
    * [Python testing in Visual Studio Code](https://code.visualstudio.com/docs/python/testing)

**6.2 Integration tests with docker-compose**
* `DeepDiff`: Used for comparing 2 dictionaries of expected and actual responses.
    `DeepDiff(actual, expected)`.
* To compare numerical values to the closest decimal using DeepDiff, set `significant_digits=<closest decimal>`.
* Refer [`integration-test`](https://github.com/viviensiu/mlops-zoomcamp/tree/main/6_best_practices/code/integration-test) folder for the setup:
    * `run.sh`: main bash script to build docker image with a timestamp tag, export global env variable, bring up containers via docker-compose, and run `test_docker.py`. It will then log error code using `docker-compose logs` if any and brings down containers again using docker-compose.
    * `test_docker.py`: integration test with model to compare actual and expected predictions.
* To execute the integration test, navigate to `integration-test` folder and run `./run.sh`.

**6.3 Testing cloud services with LocalStack**
* [LocalStack](https://www.localstack.cloud/) is a fully functional local AWS cloud stack.
* Setup:
    * Create Kinesis stream `ride-predictions` via LocalStack in `run.sh`
    * Add Kinesis service with port=4566 in `integration-test` > `docker-compose.yaml` using `localstack` image. Add env variable in `docker-compose.yaml` to include Kinesis Endpoint URL.
    * Configure `model.py` to access local Kinesis endpoint (see function `create_kinesis_client`).
    * Create integration test cases, see `test_kinesis.py`.
* Start service with `./run.sh`. If all goes well the containers should be up and running, then delete automatically with docker-compose down, otherwise any error code not equals 0 will keep the containers running.

**6.4 Code quality: linting and formatting**
* [PEP 8](https://peps.python.org/pep-0008/) - Python style guide on how code should be formatted.
* `pylint` - a package that ensure code follows PEP 8 standard and checks for programming mistakes.
* Setup `pylint`: `pip install pylint` or `pipenv install pylint`.
* To check for code quality using pylint, `pylint <python script.py>`. It will output suggestions to improve code, e.g. missing-function-docstring and give an overall rating out of 10.
* To run pylint on all Python files in a directory, use `pylint --recursive=y
* Warnings can be disabled in `pylint` by: 
    * bundling them in a `.pylintrc` file, or 
    * globally using `pyproject.toml` as a config file. See example in [`pyproject.toml`](https://github.com/viviensiu/mlops-zoomcamp/blob/main/6_best_practices/code/pyproject.toml).
    * or just within a particular function, [example](https://pylint.pycqa.org/en/v2.12.2/faq.html#is-there-a-way-to-disable-a-message-for-a-particular-module-only):
    ```python
    def function1():
        # pylint: disable=<some-message>
    ```
* Note that pylint would cause error code greater than 0 if the code doesn't conform to standards, even though it is logically correct. Hence it should only be something in dev env and not in production.
* [`black`](https://pypi.org/project/black/) - takes care of PEP8 formatting.
* To run `black`:
    * `pip install black`.
    * `black --diff .` to show what the changes would be without applying them.
    * `black .` would actually apply the changes.
    * Could also be included into `pyproject.toml`.
* [`isort`](https://pypi.org/project/isort/) - sort imports alphabetically and automatically separate into sections and by type.
* To run `isort`:
    * `pip install isort`.
    * On specific file: `isort <original .py> <sorted .py>`
    * On all files in a directory: `isort .`

**6.5 Git pre-commit hooks**
* Git pre-commit hooks allows us to not forget running some cleaning steps, e.g. code linting, formatting and so on before we commit our code.
* Note that post-commit also exists to run some steps after commit.
* Package: [`pre-commit`](https://pre-commit.com/#intro)
* `pipenv install pre-commit`.
* In the main directory of Github workspace: `cd .git/`.
* Then `cd hooks`, there's a `pre-commit.sample` file. We can refer to this file (a shell script) to modify and include commands to execute before every commit.
* To run pre-commit for a sub-folder, 
    * Go to the sub-folder.
    * `git init` to create a standalone repo. This will create `.git` in here.
    * `pre-commit sample-config` to show how to create a sample script. This is copied and renamed as [`pre-commit-config.yaml`](https://github.com/viviensiu/mlops-zoomcamp/blob/main/6_best_practices/code/pre-commit-config.yaml).
    * Run `pre-commit install` in `.git/hooks/` to create a `pre-commit` file in `.git/hooks/` folder.
    * Note that this is local so every time the repo is cloned, it needs to be recreated.
* We can use pre-defined hooks or create our own. See [pre-defined hooks](https://github.com/pre-commit/pre-commit-hooks).
* Once setup is done, everytime when we run git commit, the hooks defined will run first.

**6.6 Makefiles and make**
* We use `make` to define aliases. E.g. We define `run` as an alias for a specific set of commands, and by calling `make run` we can execute these set of commands. So it is a convenient way to execute commands instead of having to type full commands everytime.
* We could also define dependencies between aliases to ensure some command sets are executed before another. 
* Steps:
    * Create a `Makefile`.
    ```bash
    hello:
        echo "hello world"
    ```
    * In command line, execute `make hello`. It will print:
    ```bash
    echo "hello world"
    hello world
    ```
    * To add dependencies, use `alias: depend1 depend2...` example:
    ```bash
    saymyname: 
        echo "I am Brian"
    hello: saymyname
        echo "hello world"
    ```
* For this unit, our Makefile will:
    * Runs test.
    * Perform quality checks
    * Build Docker image.
    * Run integration test.
