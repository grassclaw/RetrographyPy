# Mex+Sync Covert Channel Setup Guide

This README provides instructions for setting up the environment, installing necessary packages, and running the Trojan and Spy scripts to implement the Mex+Sync covert channel.

## Next Steps
Enhance Covert Channel:
- Improve timing! :/ :
    - It's currently very very very very VERY slow!
    - Ideas:
        1. Variable-Length Encoding (Run-Length Encoding) 50ms -> 3 consectuvie 1's, etc.
        2. Matrix Based Encoding for N-Dimensional matrix
        3. Compression! Compress (e.g., ZIP, GZIP)
- Improve Adaptive communication:
    - Ideas:
        1. Hierarchical Encoding with Control Signals
- Error Checking
    - Ideas:
        1. Checksum exchange
        2. Parity Check
- Add randomized timing or switch to other synchronization primitives (e.g., semaphores, events).

- Experiment with Cross-VM Communication:

    -  Test the channel across different VMs using shared mutexes in the Global\\ namespace.

## 1. Prerequisites

Ensure you have the following installed on your Windows VM:

- **Python 3.8+**: Download and install Python from the [official website](https://www.python.org/downloads/).
- **pip**: Python's package manager is included with Python 3. Ensure it's up to date:
  
  ```bash
  python -m pip install --upgrade pip

## 2. Python Virtual Environment (Recommended)

To isolate the required packages and avoid conflicts with other Python projects, create a virtual environment.

### Steps to Create a Virtual Environment:

1. Open Command Prompt and navigate to the folder where you’ll store the project:

   ```bash
   cd path\to\project\folder\Development\MexSync

2. Create a virtual environment:

   ```bash
    python -m venv mexsync-env

3. Activate the virtual environment:
    ```bash
    mexsync-env\Scripts\activate
4. After activation, install the necessary Python packages as listed below (proceed to step 3).

## 3. Required Python Packages

Install the following Python package in your environment:

### Required Libraries:

- **pywin32**: Provides access to the Win32 API for mutex and event handling.

   ```bash
   pip install pywin32

## 4. Folder Structure
Organize your project files as follows:

MexSync/

├── mexsync-env/          # Virtual environment (automatically created)

├── trojan.py             # Trojan script (sender)

├── spy.py                # Spy script (receiver)

└── README.md             # This file
## 5. Running the Scripts

Follow these steps to test the covert channel:

### Start the Trojan (Sender):
1. Open Command Prompt.
2. Activate the virtual environment:

   ```bash
    mexsync-env\Scripts\activate

2. Run the Trojan script:
   ```bash
    python trojan.py

### Start the Spy (Receiver):
1. Open a separate Command Prompt window and activate the same virtual environment:

   ```bash
    mexsync-env\Scripts\activate

2. Run the Spy script:
    ```bash
    python spy.py

    Expected Output:
    The Spy will receive and decode the bits sent by the Trojan, based on the timing intervals.

## 6. Troubleshooting
#### Environment Issues: 
- Ensure the virtual environment is activated before running the scripts.
- If pywin32 installation fails, ensure you're using the correct Python version (3.8+).
#### Communication Issues:
- Verify the MUTEX_NAME constant matches in both trojan.py and spy.py.
- Adjust the THRESHOLD value in spy.py if the bits are misinterpreted.


## Additional Notes
This project uses Win32 API through pywin32, which provides direct access to Windows-native synchronization primitives.
For educational purposes only: Be mindful of the ethical implications and legal considerations of experimenting with covert channels.