# AWS S3
Easy Storage system with account and password control.

## How to use?
Note: Remember to change S3 bucket name.

### Create User
```
python3 CreateUser.py <UserName> <Pawssord> <yourEmail@gmail.com>
```

### Upload File
```
python3 UploadFile.py <userName> <password> <fileKey> <filePath>
```

### Get File
```
python3 GetFile.py <userName> <password> <file-key> <path-to-save-file-to>
```

### List all Files
```
python3 ListFiles.py <userName> <password>
```
