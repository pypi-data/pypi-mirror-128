# e-Manifest

[![Downloads](https://pepy.tech/badge/emanifest)](https://pepy.tech/project/emanifest)
![PyPI](https://img.shields.io/pypi/v/emanifest)

**emanifest** is a Python utility wrapper for accessing the e-Manifest API of the US Environmental Protection Agency's RCRAInfo national electronic hazardous waste management system.

## Contents
- [Requirements](#requirements)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
  - [Getting Started](#getting-started)
  - [Functions](#functions)
  - [Help](#help)
- [Contact](#contact)
- [License](#license)

## Requirements

- Python 3.6

## Dependencies

- requests
- requests_toolbelt
- getpass
- pandas
- json
- zipfile
- io

## Installation

**emanifest** can be installed directly from the Python package directory using pip:

```bash
pip install emanifest
```

## Usage

### Getting Started

Before using the **emanifest** package, ensure you have a RCRAInfo user account and the necessary permissions to generate an API ID and key. Make note of your ID and key somewhere safe.

To add **emanifest** to your current Python environment and authenticate your account, peform the following commands:

```python
from emanifest import emanifest as em

em.eManAuth('YOUR_API_ID', 'YOUR_API_KEY', 'YOUR_ENVIRONMENT')
```

Your environment variable can be any of the following for which you have permission: "dev", "sandbox", "preprod", "prod"

Once you receive a "Authentication successful" message, you are ready to use the full functionality of the **emanifest** package. Functions designed for use by other groups, such as regulators or industry users, will return 'Access Denied' errors if you are not authorized to view this content in RCRAInfo.

### Functions

There are ten categories of functions in the **emanifest** package. For more information about these services, visit the Swagger page of your selected environment. ([DEV](https://rcrainfodev.com/rcrainfo/secured/swagger/), [SANDBOX](https://sandbox.rcrainfodev.net/rcrainfo/secured/swagger/), [PREPROD](https://rcrainfopreprod.epa.gov/rcrainfo/secured/swagger/), [PROD](https://rcrainfo.epa.gov/rcrainfoprod/secured/swagger/))

1. [All users] Authentication services
2. [All users] e-Manifest Lookup Services
3. [All users] Lookup Services
4. [All users] Site Services
5. [Industry users] e-Manifest Services
6. [Industry users] e-Manifest UI Link Services
7. [Regulator users] CM&E Evaluation Services
8. [Regulator users] e-Manifest Services
9. [Regulator users] Handler Services
10. [Regulator users] User Services

Most content will be returned as a [Pandas Dataframe item](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html). To output this data as a CSV or Excel file, you will need to ensure the Pandas library is active in your current Python environment, select a desired **emanifest** function (e.g. GetSiteDetails), and perform one of the following commands:

```python
import pandas as pd # Unnecessary if you have imported Pandas elsewhere

em.GetSiteDetails('VATESTSD123').to_csv('your_new_file_name.csv')

em.GetSiteDetails('VATESTSD123').to_excel('your_new_file_name.xlsx')

```

More complicated results will be returned as a JSON object.

Functions that download file attachments will store these in the same folder as your Python document. Functions that update, correct, or save manifests by uploading new .json and/or .zip files must receive the specific location of these files on your computer. By default, these functions will assume the files are located in the same folder as your Python document.

### Help

If you are uncertain how to use a function, run help(em.FunctionName) in your Python environment. This will return a description of the function, any required inputs, and the formats of those inputs. For a list of all the functions contained in **emanifest** and additional information about this package, run help(emanifest) in your Python environment.

## Contact

Please direct questions to the EPA e-Manifest team at [USEPA/e-manifest](https://github.com/USEPA/e-manifest)

## Disclaimer

The United States Environmental Protection Agency (EPA) GitHub project code is provided on an "as is" basis and the user assumes responsibility for its use. EPA has relinquished control of the information and no longer has responsibility to protect the integrity , confidentiality, or availability of the information. Any reference to specific commercial products, processes, or services by service mark, trademark, manufacturer, or otherwise, does not constitute or imply their endorsement, recommendation or favoring by EPA. The EPA seal and logo shall not be used in any manner to imply endorsement of any commercial product or activity by EPA or the United States Government.
