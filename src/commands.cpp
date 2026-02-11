#include "commands.h"

#include <iostream>

#include "utils.h"

void exit_builtin(const std::string &input, const std::vector<std::string> &args) {
    int exit_code = EXIT_SUCCESS;

    if (args.size() == 2 && is_number(args[1])) {
        exit_code = std::stoi(args[1]);
    } else if (args.size() > 2) {
        std::cout << "exit: too many arguments" << std::endl;
        return;
    }

    exit(exit_code);
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
    if (args.size() > 1) {
        std::cout << "cd: too many arguments" << std::endl;
        return;
    }

    std::string dir = getenv("HOME");

    if (args[0][0] == '~') {
        if (args[0].length() > 1) {
            for (int i = 1; i < args[0].length(); i++) {
                dir += args[0][i];
            }
        }
    } else if (!args[0].empty()) {
        dir = args[0];
    }

    if (chdir(dir.c_str()) != 0) {
        std::cout << "cd: " << args[0] << ": No such file or directory" << std::endl;
    }
}
