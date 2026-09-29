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
./security_log_analyzer samples/auth.log
```

## Skills demonstrated

C++, file I/O, regular expressions, STL containers, sorting, defensive security monitoring, and command-line development.

## Included demo

Run the build commands from this directory. The synthetic sample produces:

```text
Failed-login alerts (threshold: 3)
[ALERT] 192.0.2.10: 3 failures
Malformed lines ignored: 1
```

The sample contains documentation-only IP addresses. Counts cover the entire file, not a sliding time window. An alert is a signal to investigate, not proof of an attack. The parser accepts the custom format shown in the sample; timestamps and IP addresses are not semantically validated. Per-user counts are collected internally but are not printed.
