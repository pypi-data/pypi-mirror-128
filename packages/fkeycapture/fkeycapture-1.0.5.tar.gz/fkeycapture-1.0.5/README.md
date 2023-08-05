# fkeycapture
This is a simple and easy to use package that allows you to capture individual keystrokes from the user.
#### Forms:
1. (Default) Recive key as a string
2. Recive key as bytes
#### How to Use:
1. from fkeycapture import get
2. Use it like this 
: get([number of keys to capture],[if you want bytes output, make this 'True'])
###### v.1.0.5:
Repaired an issue in 1.0.4 which caused the module to cause a recusion error.