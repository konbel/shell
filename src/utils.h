#ifndef SHELL_UTILS_H
#define SHELL_UTILS_H

#include <algorithm>
#include <filesystem>
#include <unistd.h>

inline std::vector<std::string> path;

inline void parse_path() {
    const std::string path_env = std::getenv("PATH");
    std::stringstream path_stream(path_env);
    std::string buffer;
    while (std::getline(path_stream, buffer, ':')) {
        path.push_back(buffer);
        buffer.clear();
    }
}

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

inline bool is_whitespace(const std::string &str) {
    return std::ranges::all_of(str, [](const char c) { return std::isspace(c); });
}

#endif //SHELL_UTILS_H
