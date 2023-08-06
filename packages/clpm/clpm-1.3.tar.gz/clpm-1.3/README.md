# CLPM: A command-line password manager. 
### About 
My goal for this project is to create an easy-to-use out-of-the-box password manager accessible through the command-line. The passwords are encrypted using 256 bit AES and the master password is hashed using 256 bit SHA-3. The master password is used to generate a key for encryption and for accessing the accounts using the UI. 

## Installation
Just install through pip. 
```
pip install clpm
```
Then run `clpm init` to initialize the database.
A prompt & confirmation will appear to input a master password.

### TODO
* Encrypt all account information rather than just passwords.
* Add usage to the README.
* Revamp menu.
* Fix double init/reset error






