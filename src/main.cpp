#include <iostream>

#include "commands.h"
#include "utils.h"

void print_prompt() {
    std::cout << "$ ";
}

void eval(const std::string &input) {
    auto args = split(input, ' ');
    const std::string command = args[0];
    args.erase(args.begin());

    // handle built in commands
    if (builtins.contains(command)) {
        builtins[command](input, args);
        return;
    }

    // handle external executables
    if (const std::string full_path = find_executable(command); !full_path.empty()) {
        std::system(input.c_str());
        return;
    }

    std::cout << command << ": command not found" << std::endl;
}

int main() {
    std::cout << std::unitbuf;
    std::cerr << std::unitbuf;

    parse_path();

    // REPL
    print_prompt();

    std::string buffer;
    while (std::getline(std::cin, buffer)) {
        eval(buffer);
        buffer.clear();
        print_prompt();
    }

    return EXIT_SUCCESS;
}
