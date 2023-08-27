Manage your Ansible Tower jobs with ease using this Python tool!

## Table of Contents

- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Options Explained](#options-explained)
- [Examples](#examples)

## Prerequisites

1. **Python3**: Ensure you have Python 3 installed.
2. **Requests Library**: Install it using pip:

    ```shell
    pip install requests
    ```

## Usage

1. Run the script in your terminal:

   ```shell
    python towerJobs.py
   ```
    
2. You will be prompted to input the Ansible Tower's host address, your username, and your password.
    
3. A menu with various options will appear. Choose the desired operation.
    

## Options Explained

- **Enable jobs**: Enables jobs based on IDs provided in files named with the prefix `enabled_jobs.json`.
- **Disable jobs**: Disables currently enabled jobs and saves their IDs to `enabled_jobs.json`.
- **List all jobs**: Outputs a list of all jobs, regardless of their status.
- **List only enabled jobs**: Outputs a list of jobs that are currently enabled.
- **List only disabled jobs**: Outputs a list of jobs that are currently disabled.
- **Exit**: Terminate the script (Accepts inputs: `6`, `X`, `x`).

For the options that list jobs (3, 4, 5), you'll get a choice on how to view the output: on the screen, saved to a file, or both.

## Examples

**Enable Jobs**:

- Run the script.
- Opt for `1. Enable jobs`.
- If there are `enabled_jobs.json` prefixed files available, decide if you want to apply changes from one specific file or all of them.

**Disable Jobs**:

- Run the script.
- Opt for `2. Disable jobs`. All the enabled jobs will be disabled, and their IDs will be recorded in `enabled_jobs.json`.

**List All Jobs**:

- Run the script.
- Opt for `3. List all jobs`.
- Decide how you want to view the output.

**Exiting the Script**:

- Run the script.
- Simply choose the option `6. Exit (X or x)`.
