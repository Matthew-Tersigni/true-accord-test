# Usage
```
python3 -m venv .venv

source .venv/bin/activate

make test
```

To run the script as designed for the exercise, run `python3 main.py`. This will output the JSON Lines to stdout.

# Solution Explanation
The solution is a simple python script that takes the data from the mocked
API and outputs it to stdout in JSON Lines format.  The script is
designed to be run from the command line and takes no arguments. The script
can also be invoked using Docker. The docker container logs will need to be
tailed in order to see the output of the script.

I have included some coding standards that I like to abide by, these include
pycodestyle, pylint, and tests using pytest.  The test suite runs and provides any
style warnings or errors.  The test suite also provides a reasonable coverage of
the codebase, and it's functionality.

## Time Spent
I spent about 3 hours on this project.  I spent about 30 minutes bootstrapping the
project, ensuring the Makefile was correct and set up the project correctly, some
time was also spent testing and all scripts ran without any issues.

The rest of the time was spent writing the code, and testing it. I did some cleanup and
refactoring, and then wrote the README.md file.

## Outstanding Issue
There is a known issues, and had I understood what the business need was I would
have attempted to address it. The Currency needs to be handled better, specifically there 
are rounding issues. If the currency needed to be handled in the standard python means, it
would be using the decimal package and more specifically, the HALF_ROUND_UP rounding method.

This is something I am happy to discuss further.
