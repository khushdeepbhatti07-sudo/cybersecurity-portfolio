#include <algorithm>
#include <fstream>
#include <iostream>
#include <map>
#include <regex>
#include <string>
#include <vector>

struct Event {
    std::string timestamp;
    std::string user;
    std::string ip;
    bool failed;
};

bool parseEvent(const std::string& line, Event& event) {
    static const std::regex pattern(
        R"(^(.{19})\s+EVENT=(LOGIN_FAILED|LOGIN_SUCCESS)\s+user=([^\s]+)\s+ip=([^\s]+)$)");
    std::smatch match;
    if (!std::regex_match(line, match, pattern)) return false;
    event.timestamp = match[1];
    event.failed = match[2] == "LOGIN_FAILED";
    event.user = match[3];
    event.ip = match[4];
    return true;
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <log-file>\n";
        return 1;
    }

    std::ifstream input(argv[1]);
    if (!input) {
        std::cerr << "Could not open log file.\n";
        return 1;
    }

    std::map<std::string, int> failedByIp;
    std::map<std::string, int> failedByUser;
    std::string line;
    int malformed = 0;

    while (std::getline(input, line)) {
        Event event;
        if (!parseEvent(line, event)) {
            ++malformed;
            continue;
        }
        if (event.failed) {
            ++failedByIp[event.ip];
            ++failedByUser[event.user];
        }
    }

    std::vector<std::pair<std::string, int>> ranked(failedByIp.begin(), failedByIp.end());
    std::sort(ranked.begin(), ranked.end(), [](const auto& a, const auto& b) {
        return a.second > b.second;
    });

    std::cout << "Failed-login alerts (threshold: 3)\n";
    for (const auto& [ip, count] : ranked) {
        if (count >= 3) std::cout << "[ALERT] " << ip << ": " << count << " failures\n";
    }
    std::cout << "Malformed lines ignored: " << malformed << "\n";
    return 0;
}
