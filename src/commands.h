#ifndef SHELL_COMMANDS_H
#define SHELL_COMMANDS_H

#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

inline std::unordered_map<std::string, std::string> executables_cache;

void build_executables_cache();

std::unordered_set<std::string> autocomplete_builtin(const std::string &input);
std::unordered_set<std::string> autocomplete_executable(const std::string &input);

void exit_builtin(const std::string &input, const std::vector<std::string> &args);
void type(const std::string &input, const std::vector<std::string> &args);
void echo(const std::string &input, const std::vector<std::string> &args);
void pwd(const std::string &input, const std::vector<std::string> &args);
void cd(const std::string &input, const std::vector<std::string> &args);

inline std::unordered_map<std::string, void (*)(const std::string &, const std::vector<std::string> &)> builtins = {
    {std::string("exit"), &exit_builtin},
    {std::string("echo"), &echo},
    {std::string("type"), &type},
    {std::string("pwd"), &pwd},
    {std::string("cd"), &cd},
};

#endif //SHELL_COMMANDS_H
