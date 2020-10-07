# anonAddy2Sieve
Simple scripts that help creating Sieve emial filters from AnonAddy's fantastic API

## Introduction
**AnonAddy** [[LINK](https://anonaddy.com)] is a web service that allows you to create custom alias emails. This is useful if you want to keep your personal email private, if you want to easylu compaartimentalize your emails, or if you want to disable internet giants from prifoling you through your email address. AnonAddy and other services like it are great and offer many advantages. However, they also bring an obvious disatvantage, now you have a great number of email addresses instead of just the one.
AnonAddy in particular offers an ample API that allows management of your account using JSON. Using this tool it is possible to create, list or manage your aliases at your will from scripts and external apps.

**ProtonMail** [[LINK](https://protonmail.com)] is a privacy focused email service based in Szwitzerland. They might not offer as many features and it is not as customizable as other services, however it is powerfully private and it is constantly being improved. At this time it even offers the possibility to program email filters using Sieve language, a greate feature that we will use in this script

## What does AnonAddy2Sieve do
This script was made to do one simple task. It creates a Sieve code that labels all incoming email from an AnnonAddy's account aliases with their respective descriptions.  
AnonAddy2Sieve will request AnonAddy to share a list of all the not-deleated aliases. For each alias, AnonAddy will send a JSON snippet such as this one:
```json
    {
      "id": "50c9e585-e7f5-41c4-9016-9014c15454bc",
      "user_id": "ca0a4e09-c266-4f6f-845c-958db5090f09",
      "aliasable_id": null,
      "aliasable_type": null,
      "local_part": "first",
      "extension": null,
      "domain": "johndoe.anonaddy.com",
      "email": "everybody-should-quit-facebook@johndoe.anonaddy.com",
      "active": true,
      "description": "facebook",
      "emails_forwarded": 5,
      "emails_blocked": 0,
      "emails_replied": 0,
      "recipients": [],
      "created_at": "2019-10-01 09:00:00",
       "updated_at": "2019-10-01 09:00:00"
    }
```
AnonAddy2Sieve will then take the 'email' field and the 'description' field in order to create a code such as this:

```Sieve
if allof (address :all :comparator "i;unicode-casemap" :is "From" "everybody-should-quit-facebook@johndoe.anonaddy.com") {
	fileinto "facebook";

}
```


## How to use AnonAddy2Sieve
### Requirments
- Python3 installed. You can test if you have python and what version is installed by open a terminal and typing python, the first line will tell you the version number. To exit type exit() and click Enter.
- A personal access token from AnonAddy. You can get one by going into AnonAddy's settings and scrolling down to API. There you can create a new token, then put it into a new text document on the same folder where you have downloaded anonAddy2Sieve.py

### How-To GUI
Open the file with python. You can do this either opening the file using python as prefered app on the context menu. Or typing python anonAddy2Sieve.py on a terminal, where anonAddy2Sieve.py is the full path to the file.

### How-To CLI
You can use the CLI version to output the generated directly into terminal. More options available on the CLI usage information below.
- Open a terminal. 
- Browse to the folder where you have downloaded AnonAddy2Sieve.py
- execute by typing 'python anonAddy2Sieve.py -c -t tokenfile' where tokenfile is the text file with the token given by anonAddy.

## CLI Usage information
```
usage: ./anonAddy2Sieve.py [option]
Options and arguments (and corresponding environment variables):
-c       : disables the GUI and outputs either to terminal or to a file if -o option specified. (also --useCLI)
-h       : print this help message and exit. (also --help)
-j file  : uses json text from a given file instead of contacting anonaddy. 
           this option will overide -t. (also --json=<file>)
-o file  : specifies the file where the Sieve code will be writen.
           If empty, the code will print on the default channel (e.g. terminal) (also --output=<file>)
-t file  : specifies the file containing anonaddy's API token. (also --token=<file>)

EXAMPLE:
./anonAddy2Sieve.py -c -t token.txt -o protonMailFilter.sieve
```
