#include "commands.h"

#include <iostream>

#include "utils.h"

void exit_builtin(const std::string &input, const std::vector<std::string> &args) {
    exit(EXIT_SUCCESS);
}

void echo(const std::string &input, const std::vector<std::string> &args) {
    std::cout << join(args, " ") << std::endl;
}

void type(const std::string &input, const std::vector<std::string> &args) {
    for (auto &arg: args) {
        if (builtins.contains(arg)) {
            std::cout << arg << " is a shell builtin" << std::endl;
            continue;
        }

        if (auto full_path = find_executable(arg); !full_path.empty()) {
            std::cout << arg << " is " << full_path << std::endl;
            continue;
        }

        std::cout << args[0] << " not found" << std::endl;
    }
}

void pwd(const std::string &input, const std::vector<std::string> &args) {
    std::cout << getcwd(nullptr, 0) << std::endl;
}

void cd(const std::string &input, const std::vector<std::string> &args) {
    if (args.empty() || is_whitespace(input.substr(3))) {
        chdir(getenv("HOME"));
        return;
    }

    if (args.size() > 1) {
        std::cout << "cd: too many arguments" << std::endl;
        return;
    }

    if (args[0][0] == '~') {
        chdir(getenv("HOME"));
        return;
    }

    if (chdir(args[0].c_str()) != 0) {
        std::cout << "cd: " << args[0] << ": No such file or directory" << std::endl;
    }
}
