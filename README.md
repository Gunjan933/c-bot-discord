# c-bot-discord
Discord bot for server moderation, and other custom usages including auto project allotment and etc.

### How to make bot run as systemd service

We can use `nohup` for this purpose too.
```bash
nohup python bot.py &
```

Also you can create a service for it if you are running Ubuntu 15.04 or newer you can create a simple systemd service file to run it as follows

```
[Unit]
Description=A test unit

[Service]
ExecStart=<full_path_to_script>
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=bot

[Install]
WantedBy=multi-user.target
```
Put these lines in a file called `bot.service` in `/etc/systemd/system`.

Make sure your script file is executable by running `sudo chmod +x <full_path_to_script>`

Reload systemd by running
```bash
sudo systemctl daemon-reload
```
Start the service `
```bash
sudo systemctl start bot
```

Now you can check if the service is running or not:
```bash
sudo systemctl status bot
```
Stop the service using:
```bash
sudo systemctl stop bot
```
Restart is using
```bash
sudo systemctl restart bot
```

Finally, use the enable command to ensure that the service starts whenever the system boots
```
sudo systemctl enable bot
```
