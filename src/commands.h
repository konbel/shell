#ifndef SHELL_COMMANDS_H
#define SHELL_COMMANDS_H

#include <string>
#include <unistd.h>
#include <unordered_map>
#include <unordered_set>
#include <vector>

inline std::vector<std::string> history_cache;
inline size_t history_index = 0;
inline std::string typed_command;
void read_history(const std::string &file_path);
void write_history(const std::string &file_path);
void append_history(const std::string &file_path);

inline std::unordered_map<std::string, std::string> executables_cache;
void build_executables_cache();

std::unordered_set<std::string> autocomplete_builtin(const std::string &input);
std::unordered_set<std::string> autocomplete_executable(const std::string &input);

void redirect_io(int output_fd, int input_fd, int error_fd);
void restore_io();

void exit_builtin(const std::string &input, const std::vector<std::string> &args);
void type(const std::string &input, const std::vector<std::string> &args);
void echo(const std::string &input, const std::vector<std::string> &args);
void pwd(const std::string &input, const std::vector<std::string> &args);
void cd(const std::string &input, const std::vector<std::string> &args);
void history(const std::string &input, const std::vector<std::string> &args);

inline std::unordered_map<std::string, void (*)(const std::string &, const std::vector<std::string> &)> builtins = {
    {std::string("exit"), &exit_builtin},
    {std::string("echo"), &echo},
    {std::string("type"), &type},
    {std::string("pwd"), &pwd},
    {std::string("cd"), &cd},
    {std::string("history"), &history},
};

int exec(const std::string &executable, const std::vector<std::string> &args, int output_fd, int input_fd);

#endif //SHELL_COMMANDS_H
