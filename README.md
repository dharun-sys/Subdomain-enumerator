# Subdomain Enumerator

## Description
Subdomain Enumerator is a tool designed to automate the process of discovering subdomains for a given domain. This tool is particularly useful for security researchers, penetration testers, and bug bounty hunters looking to identify potential attack surfaces during reconnaissance.

## Features
- Enumerates subdomains using a variety of techniques.
- Supports DNS resolution to verify active subdomains.
- Includes a built-in wordlist for brute-forcing subdomains.
- Provides output in a user-friendly format for easy analysis.

## Development Status
This project is currently under development. Features, functionality, and documentation are being actively worked on. Feedback and contributions are welcome!

## Usage
```bash
# Clone the repository
$ git clone https://github.com/dharun-sys/subdomain-enumerator.git

# Navigate to the project directory
$ cd subdomain-enumerator

# Run the script
$ python subdomain_enum.py example.com wordlist.txt --output results.txt --threads 20
```

## Prerequisites
- Python 3.7+
- Required Python libraries (install via `requirements.txt`):
  ```bash
  $ pip install -r requirements.txt
  ```

## Future Plans
- Integrate support for additional enumeration techniques such as DNS Zone Transfer and APIs.
- Add an option to export results in JSON, CSV, and HTML formats.
- Optimize performance for handling large datasets.
- Implement multi-threading for faster enumeration.

## Contributing
Contributions are welcome! If you have ideas, suggestions, or want to report bugs, please open an issue or submit a pull request.

## License
This project is licensed under the [MIT License](LICENSE).


**Note:** Since this project is still in development, some features may not work as expected. Thank you for your patience and support!
