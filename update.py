#!/usr/bin/env python3
"""
Script to update AWS Route 53 DDNS records with the machine's current public IP address.
"""

__author__ = "Matthew Bowen"
__version__ = "0.1.0"
__license__ = "MIT"

from dotenv import load_dotenv
import logging
import logzero
import requests
from logzero import logger
import os
import pathlib
import yaml
import boto3

SCRIPT_DIR = pathlib.Path(__file__).parent.absolute()

client = boto3.client('route53')

def configure_logging():
    if log_file := os.environ.get('LOG_FILE'):
        logzero.logfile(log_file)
    if log_level := os.environ.get('LOG_LEVEL'):
        logzero.loglevel(logging.getLevelName(log_level.upper()))

def get_zone_id(zone_name):
    response = client.list_hosted_zones_by_name(DNSName=zone_name, MaxItems="1")
    if not 'HostedZones' in response or not response['HostedZones']:
        raise Exception(f'Zone {zone_name} not found')
    return response['HostedZones'][0]['Id'].split('/')[-1]  # Extract the zone ID from the full ARN

def update_record(zone_id, record, ip):
    client.change_resource_record_sets(
        HostedZoneId=zone_id,
        ChangeBatch={
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': record,
                        'Type': 'A',
                        'TTL': os.environ.get('TTL', 600),
                        'ResourceRecords': [{'Value': ip}]
                    }
                }
            ]
        }
    )

def update(ip):
    with open(f'{SCRIPT_DIR}/rules.yml', 'r') as file:
        rules = yaml.safe_load(file)
    for zone, names in rules.items():
        logger.debug(f"Updating zone {zone}")
        try:
            zone_id = get_zone_id(zone)
            for name in names:
                logger.debug(f"Updating record {name}")
                try:
                    update_record(zone_id, name, ip)
                except Exception as e:
                    logger.error(f'Failed to update record {name}: {e}')
        except Exception as e:
            logger.error(f'Failed to update zone {zone}: {e}')

def main():
    ip = requests.get(os.environ.get('IP_SERVER')).text.strip()
    with open(f'{SCRIPT_DIR}/ip.txt', 'r') as f:
        old_ip = f.read().strip()

    if ip == old_ip:
        logger.info('No change')
        exit(0)

    logger.info(f'IP changed from {old_ip} to {ip}')
    with open(f'{SCRIPT_DIR}/ip.txt', 'w') as f:
        f.write(ip)

    update(ip)
    logger.info('Done')

if __name__ == "__main__":
    load_dotenv()
    configure_logging()
    main()
