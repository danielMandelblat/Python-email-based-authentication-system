
# Email Authentication Docker-Based System

This system helps to validate the user's email account.
Once the SMTP server settings are applied, you can send users an email with a verification code and then authenticate if the code is valid.
In this way, you can confirm your user's identity.

## How does it's works?
1.  The user sends a POST request with the email.
2. The system generates a code for this specific email that is valid for 30 (can be edited in the settings object) minutes.
3. The user sends a POST request with the email and the received code and gets authentication status in JSON format.
4. All the requests are saved in log objects with the user  IP and the process status.


## Installation

Navigate into the application folder

```bash
cd email-authentication
```

Build the Docker image
```bash
docker built -t authentication-system:latest .
```

Run new container
```bash
docker run -d --name authentication-system -p <host-port>:80 authentication-system:latest .
```

Login to the system
```
Username: admin
Password: admin123
```

Create a new SiteSettings object and enter your SMTP settings


## Authors
- [@danielMandelblat](https://github.com/danielMandelblat)



    