# SQL Injection Labs
My lab notes and learning progress for the Web Security Academy's SQL Injection chapter.

Follows PortSwigger's Web Security Academy training path. This repository is a record of my labs for Chapter 1: SQL injection. The course can be found here: https://portswigger.net/web-security/learning-path

The labs are done on Kali Linux VM on VirtualBox, where I also utilize Burp Suite Community Edition 2023.7.2.

### General Notes
Prior to doing these labs, I learned the basic theory of:
- What is an SQL injection?
  - Types of SQL injections
- How do I find it?
  - Methodologies for Black / Grey / White Box Testing
  - Leverage automation to find vulnerabilities
- How do I exploit it?
  - Explore these in the labs
- How do I prevent it?
  - Prepared Statements, Stored Procedures, Whitelist Input Validation, Escaping All User Supplied Input, Enforce Least Privilege

![image](https://github.com/kienmarkdo/SQL-Injection-Labs/assets/67518620/33cbdd8a-4a44-4ecd-b429-1683fe381b7e)


### Automation
Manual SQL injections (or manual pen testing in general) via random payloads is time-consuming; moreover, bots can already do this and it will only catch the low hanging fruits. As such, I will not only try to solve these labs manually, but also I will attempt to write Python scripts that perform the SQL injections.

When I do come across a vulnerability that requires scripting/automation in the future, such as a blind SQL injection vulnerability, I will have been more familiar with it.

<!-- Source: https://github.com/kienmarkdo/SQL-Injection-Labs -->
