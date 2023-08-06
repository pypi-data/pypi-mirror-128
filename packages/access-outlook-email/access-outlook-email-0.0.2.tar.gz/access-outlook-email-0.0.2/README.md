# Access Outlook Email
This project contains the basic files to send an email through the module ```exchangelib```.

## Installation
Note that the module requires ```Python 3.6``` or higher.

To install the module, run a pip command like the following:


```
pip3 install outlook-email
```

## Usage
Simply import the modules via the following import statements:
```
from config import create_account
from send import send_email
```

The ```create_account``` function requires your Outlook-Exchange email-address and your password.

To send an email, the following code provides the core functionality:
```
account = create_account('user@provider.com', '***')

send_email(account, 'TestSubject', 'TestBody', ['recepient@provider.com'])
```

## License
This project is licensed by a MIT License.

## Project status
The current released version is 0.0.1.
