#include <iostream>
#include <vector>
#include <sstream>
#include <unordered_set>

std::unordered_set builtins = {
    std::string("exit"),
    std::string("echo"),
    std::string("type"),
};

void print_prompt() {
    std::cout << "$ ";
}

void eval(const std::string &command, const std::vector<std::string> &args) {
    if (command == "exit") {
        exit(EXIT_SUCCESS);
    }

    if (command == "echo") {
        std::stringstream output;
        for (int i = 0; i < args.size(); i++) {
            output << args[i];
            if (i != args.size() - 1) {
                output << " ";
            }
        }
        output << std::endl;
        std::cout << output.str();
        return;
    }

    if (command == "type") {
        if (args.empty()) {
            std::cout << "type: not enough arguments" << std::endl;
            return;
        }

        if (builtins.contains(args[0])) {
            std::cout << args[0] << " is a shell builtin" << std::endl;
        } else {
            std::cout << args[0] << " not found" << std::endl;
        }
        return;
    }

    std::cout << command << ": command not found" << std::endl;
}

int main() {
    std::cout << std::unitbuf;
    std::cerr << std::unitbuf;

    print_prompt();

    std::string buffer;
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