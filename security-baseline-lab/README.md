# Windows and Linux Security Baseline Lab

An authorized VirtualBox lab for practicing secure workstation setup on Windows 11 and Linux Mint. The project focuses on practical hardening, verification, and documentation.

## Lab environment

- VirtualBox
- Windows 11 evaluation VM
- Linux Mint VM
- One administrator account and one standard-user account on each VM

## Baseline checklist

### Windows 11

- Install updates and reboot
- Verify Microsoft Defender real-time protection
- Verify Windows Defender Firewall for active profiles
- Use a standard account for daily work
- Review Event Viewer Security and System logs

### Linux Mint

- Install updates with Update Manager or `sudo apt update && sudo apt upgrade`
- Check firewall status with `sudo ufw status verbose`
- Review administrator membership and file permissions with `ls -la`
- Review recent local-login activity with `last`

## Evidence to document

1. A simple two-VM network diagram.
2. Screenshots showing update, firewall, and account settings.
3. A short remediation summary describing each change, why it matters, and how it was verified.

## Lab boundaries

Only use systems you own or are explicitly authorized to administer. Do not scan, attack, or alter external systems.

## Resume-ready description

Built an authorized Windows 11 and Linux Mint VirtualBox lab; applied operating-system updates, account controls, firewall settings, and permission reviews, then documented verification evidence and remaining risks.
