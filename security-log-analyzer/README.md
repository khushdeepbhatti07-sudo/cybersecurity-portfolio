# C++ Security Log Analyzer

A defensive C++ command-line project that reads controlled authentication logs and flags repeated failed logins. It demonstrates file I/O, regular expressions, STL maps and vectors, sorting, and basic security monitoring.

## Features

- Parses login success and failure events
- Counts failed logins by IP address and user
- Alerts when an IP reaches three failed attempts
- Ignores malformed entries while reporting their count

## Safe use

Use only logs and systems that you own or are authorized to analyze. Sample data should use fictional names and documentation-only IP addresses.

## Build

```bash
g++ -std=c++17 -Wall -Wextra -o security_log_analyzer security_log_analyzer.cpp
./security_log_analyzer sample_auth.log
```

## Skills demonstrated

C++, file I/O, regular expressions, STL containers, sorting, defensive security monitoring, and command-line development.
