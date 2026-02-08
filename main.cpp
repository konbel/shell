#include <iostream>
#include <vector>
#include <sstream>
#include <unordered_set>
#include <unistd.h>

std::vector<std::string> path;

void print_prompt() {
    std::cout << "$ ";
}

#pragma region builtins

std::unordered_set builtins = {
    std::string("exit"),
    std::string("echo"),
    std::string("type"),
};

void echo(const std::vector<std::string> &args) {
    std::stringstream output;
    for (int i = 0; i < args.size(); i++) {
        output << args[i];
        if (i != args.size() - 1) {
            output << " ";
        }
    }
    output << std::endl;
    std::cout << output.str();
}

void type(const std::vector<std::string> &args) {
    if (args.empty()) {
        std::cout << "type: not enough arguments" << std::endl;
        return;
    }

    if (builtins.contains(args[0])) {
        std::cout << args[0] << " is a shell builtin" << std::endl;
        return;
    }

    for (const std::string &dir : path) {
        std::string full_path = dir + "/" + args[0];
        if (access(full_path.c_str(), X_OK) == 0) {
            std::cout << args[0] << " is " << full_path << std::endl;
            return;
        }
    }

    std::cout << args[0] << " not found" << std::endl;
}

#pragma endregion

void eval(const std::string &command, const std::vector<std::string> &args) {
    if (command == "exit") {
        exit(EXIT_SUCCESS);
    }

    if (command == "echo") {
        echo(args);
    } else if (command == "type") {
        type(args);
    } else {
        std::cout << command << ": command not found" << std::endl;
    }
}

int main() {
    std::cout << std::unitbuf;
    std::cerr << std::unitbuf;

    std::string buffer;

    std::string path_env = std::getenv("PATH");
    std::stringstream path_stream(path_env);

    while (std::getline(path_stream, buffer, ':')) {
        path.push_back(buffer);
        buffer.clear();
    }

    print_prompt();

    std::istringstream input(buffer);
    std::string command;
    std::vector<std::string> args;

    while (std::getline(std::cin, buffer)) {
        input.str(buffer);
        buffer.clear();

        input >> command;
        while (input) {
            input >> buffer;
            args.push_back(buffer);
            buffer.clear();
        }

        args.pop_back();
        eval(command, args);

        buffer.clear();
        input.clear();
        command.clear();
        args.clear();

        print_prompt();
    }

    return EXIT_SUCCESS;
}