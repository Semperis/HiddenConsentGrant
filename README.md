# HiddenConsentGrant

This code exploits the hidden consent grant attack which leverages the Directory.ReadWrite.all application permission.

## Pre-requirements
1. Create certificate and private key (or use the given pair of certificate and key from the repository).
2. Update client secret and user id in the code.
   
## Usage

1. Run the tool
```
  python server.py
```

2. Launch the "non-malicious" page.
3. get the access tokens
4. have fun!

## Link to blog
https://www.semperis.com/blog/app-consent-attack-hidden-consent-grant/
