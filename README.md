# AWS Route 53 DDNS Records Updater
Update AWS Route 53 DDNS records with your public IP address.
Run as a cron job (for example every minute) and when an IP address change is detected the rules specified in `rules.yml` will be updated with your new IP.

## Requirements
* Python 3 (not tested on Python 2)
* Python modules in `requirements.txt`

## Usage
Clone the repository:
```
git clone https://github.com/shugyosha89/route53-ddns-updater.git
```

Copy `.env.example` to `.env` and optionally update the log file location and TTL value (seconds).

Make sure you've configured the AWS CLI on your machine (`aws configure`).
Note the user must have `route53:ChangeResourceRecordSets` permission on the hosted zones you wish to update.

Copy `rules.yml.example` to `rules.yml` and fill it with a list of zones (headings) and DNS records (list items) you want to update.

Install the requirements using e.g. `pip install -r requirements.txt`.

Set up a cron job to run `update.py` at regular intervals.
Example: Add the below to `crontab -e` to run every minute:
```
* * * * * python3 /path/to/route53-ddns-updater/update.py
```

## Example hosted zone policy
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "route53:ChangeResourceRecordSets",
            "Resource": "arn:aws:route53:::hostedzone/*"
        }
    ]
}
```

## Troubleshooting
To force an IP update, change the contents of `ip.txt`.
