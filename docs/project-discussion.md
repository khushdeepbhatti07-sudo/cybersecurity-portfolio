# Project discussion notes

Use these questions to understand and demonstrate the code. They are prompts, not claims of independently completed work.

## C++ analyzer

**Problem:** Repeated failed authentication may deserve investigation.

**Walkthrough:** Read lines → parse into an `Event` → aggregate failures by IP and user → sort IP counts → print IPs with at least three failures.

**Be ready to explain:** Why use `std::map`? What happens to malformed lines? Why might three failures be benign? What would a sliding time window change?

**Limits:** The count spans the whole input, not a time window. Shared IPs and simple typos can trigger alerts. Successful logins do not reset a count. The parser expects a custom format and does not validate real calendar dates or IP addresses. User totals are collected internally but are not currently displayed.

**Next improvement:** Add configurable thresholds and timestamp validation before describing the tool as time-based detection.

## File integrity monitor

**Problem:** A trusted file can change without an obvious visible sign.

**Walkthrough:** Hash files → save a baseline → rescan → compare path sets and digests → append observations to SQLite → emit JSON.

**Be ready to explain:** Why hash instead of store contents? Why is the database outside the monitored folder? Why is a checksum not proof that a file is safe? What happens if the baseline is compromised?

**Demo:** Initialize a test folder, edit one file, add another, delete a third, and explain each emitted event. Repeat the check to show that the original baseline remains unchanged.

**Trade-off:** An on-demand scan is easy to inspect and uses no external dependencies, but misses changes that happen and are reverted between scans.

## Baseline lab

Complete the [verification record](../security-baseline-lab/verification-record.md) with your own observations before presenting the lab as finished. Explain one setting, why it matters, and how you verified it. Redact personal information from screenshots.
