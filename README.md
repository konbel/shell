# Shell

A custom POSIX-compliant shell written from scratch in C++. This project implements core shell functionality including
command execution, pipelines, I/O redirection, command history, and autocompletion. The features are based on
the [Codecrafters Shell Challenge](https://app.codecrafters.io/courses/shell/overview) with some own additions.

## Features

- [x] REPL Loop
- [x] Basic builtin commands ("exit", "echo", "type", ...)
- [x] Locate and run external executables form PATH
- [x] Navigating the file system
- [x] Parsing input with quotes and backslashes
- [x] Redirecting and appending stdout and stderr
- [x] Autocompletion for builtin and external commands
- [x] Partial autocompletion for commands
- [x] Pipelines with multiple builtin and external commands
- [x] History with up and down arrow navigation
- [x] Automatic saving and loading of history

## Motivation and Learnings

The main motivation was to use C++ for a real project to get a bit more familiar with it and learn how the internals of
a tool I use every day work.

While implementing the shell, I learned a lot about how shells parse the complex user input and evaluate the commands.
I also got practical experience how unix like systems handle their process creation and management, how file descriptors
work and how to use them for redirection and pipelines.

## Dependencies

- **C++ Compiler**: Supporting C++20 or later (tested with g++ 13.3.0)
- **CMake**: Version 4.1 or higher
- **Operating System**: Unix-like system (tested on Ubuntu)
- **Python 3**: Required for running tests (optional, tested with Python 3.12.3)

## How to build

To build the shell, make sure you have all the required dependencies installed.

1. Clone the repository:

```shell
git clone https://github.com/konbel/shell.git
```

2. Navigate to the project directory and create a build directory:

```shell
cd shell
mkdir build
cd build
```

3. Run `cmake` to configure the project:

```shell
cmake ..
```

4. Build the project using `cmake`:

```shell
cmake --build .
```

5. The compiled binary will be located at `./shell` in the build directory. You can run it with:

```shell
./shell
```

## Testing

This project includes comprehensive black-box test cases written in Python to verify shell functionality. The tests
create temporary directories and files under `/tmp`, and clean up automatically after completion. If a test fails,
debugging information is printed showing which test failed and why.

### Running Tests

To run the tests, follow these steps from the project root directory:

1. Navigate to the `tests` directory:

```shell
cd tests
```

2. Run the test runner with the path to the compiled shell executable:

```shell
python3 test_runner.py ../build/shell
```

### Adding New Tests

To add new test cases:

1. Create a new Python file in the `tests` directory starting with `test_` (e.g., `test_myfeature.py`)
2. Define test functions that start with `test_` (e.g., `test_my_functionality()`)
3. The test runner will automatically discover and execute your tests
4. Each test function receives the shell executable path as a parameter

For test utilities and examples, refer to `shell_test_utils.py` or take a look at the existing test cases.
