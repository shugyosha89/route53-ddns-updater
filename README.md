# AWS Route 53 DDNS Records Updater
Update AWS Route 53 A records with your public IP address.
Run as a cron job (for example every minute) and when an IP address change is detected the rules specified in `rules.yml` will be updated with your new IP.

## Requirements
* Python 3 (not tested on Python 2)
* Python modules in `requirements.txt`

## Usage
1. Clone the repository:
```
git clone https://github.com/shugyosha89/route53-ddns-updater.git
```

2. Copy `.env.example` to `.env` and optionally update the log file location and TTL value (seconds).

3. Make sure you've configured the AWS CLI on your machine (`aws configure`).
    Note the user must have the following permissions:
    * `route53:ChangeResourceRecordSets` (for the hosted zones you wish to update)
    * `route53:ListHostedZonesByName`

4. Copy `rules.yml.example` to `rules.yml` and fill it with a list of zones (headings) and DNS records (list items) you want to update.

5. Install the requirements using e.g. `pip install -r requirements.txt`.

6. Set up a cron job to run `update.py` at regular intervals.
Example: Add the below to `crontab -e` to run every minute:
```
* * * * * python3 /path/to/route53-ddns-updater/update.py
```

## Example hosted zone policy
The following policy allows listing and updating the records of all hosted zones.
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "route53:ChangeResourceRecordSets",
            "Resource": "arn:aws:route53:::hostedzone/*"
        },
        {
            "Effect": "Allow",
            "Action": "route53:ListHostedZonesByName",
            "Resource": "*"
        }
    ]
}
```

## Troubleshooting
To force an IP update, change the contents of `ip.txt`.
