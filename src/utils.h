#ifndef SHELL_UTILS_H
#define SHELL_UTILS_H

#include <algorithm>
#include <filesystem>
#include <ranges>
#include <unistd.h>
#include <regex>

inline std::vector<std::string> path;
inline std::regex ws_regex("\\s+");
inline std::regex trim_regex("^\\s+|\\s+$");

inline std::string find_executable(const std::string &executable) {
    for (const std::string &dir: path) {
        std::string full_path = std::filesystem::path(dir) / executable;
        if (access(full_path.c_str(), X_OK) == 0) {
            return full_path;
        }
    }
    return "";
}

inline std::vector<std::string> split(const std::string &str, const char delimiter) {
    std::string buffer;
    std::vector<std::string> parts;
    std::istringstream ss(str);

    while (std::getline(ss, buffer, delimiter)) {
        parts.push_back(buffer);
    }

    return parts;
}

inline std::string join(const std::vector<std::string> &parts, const std::string &delimiter) {
    std::string result;
    for (size_t i = 0; i < parts.size(); i++) {
        result += parts[i];
        if (i != parts.size() - 1) {
            result += delimiter;
        }
    }
    return result;
}

inline bool is_whitespace(const std::string &str) {
    return std::ranges::all_of(str, [](const char c) { return std::isspace(c); });
}

inline void parse_path() {
    const std::string path_env = std::getenv("PATH");
    path = split(path_env, ':');
}

inline std::string parse_command(const std::string &input) {
    std::string command;
    bool in_single_quotes = false;
    bool in_double_quotes = false;

    for (const char c : input) {
        if (isspace(c) && !in_single_quotes && !in_double_quotes) {
            break;
        }

        if (c == '\'' && !in_double_quotes) {
            in_single_quotes = !in_single_quotes;
            continue;
        }

        if (c == '"' && !in_single_quotes) {
            in_double_quotes = !in_double_quotes;
            continue;
        }

        command += c;
    }

    return command;
}

inline std::vector<std::string> parse_args(const std::string &arg_string) {
    const std::string trimmed = std::regex_replace(arg_string, trim_regex, "");

    std::vector<std::string> args;
    std::string buffer;
    bool in_single_quotes = false;
    bool in_double_quotes = false;
    bool escaped = false;

    for (const char c : trimmed) {
        // escaping
        if (escaped) {
            buffer += c;
            escaped = false;
            continue;
        }

        if (c == '\\' && !in_single_quotes) {
            escaped = true;
            continue;
        }

        // single quotes
        if (c == '\'' && !in_double_quotes) {
            in_single_quotes = !in_single_quotes;
            continue;
        }

        if (in_single_quotes) {
            buffer += c;
            continue;
        }

        // double quotes
        if (c == '"') {
            in_double_quotes = !in_double_quotes;
            continue;
        }

        if (in_double_quotes) {
            buffer += c;
            continue;
        }

        // whitespaces
        if (isspace(c)) {
            if (buffer.empty()) {
                continue;
            }
            args.push_back(buffer);
            buffer.clear();
            continue;
        }

        // default
        buffer += c;
    }

    args.push_back(buffer);
    return args;
}

#endif //SHELL_UTILS_H
