import boto3
import json
import os
import sys
import smtplib
import smtplib
import time
from smtplib import SMTPException
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email import encoders
from email.utils import COMMASPACE, formatdate
from botocore.exceptions import ClientError

dict={}
dict[0]=sys.argv[1]
dict[1]=sys.argv[2]
dict[2]=sys.argv[3]
dict[3]=sys.argv[4]
dict[4]=sys.argv[5]
dict[5]=sys.argv[6]
dict[6]=sys.argv[7]
dict[7]=sys.argv[8]
dict[8]=sys.argv[9]
dict[9]=sys.argv[10]
print(dict)

def mail(text):
    sender = 'mail id'
    receivers = ['mailid']
    now = time.strftime("%c")
    msg = MIMEMultipart()
    msg['Subject'] = 'AWS Workspace creation ' + dict[4] + ' %s' %now
    msg['From'] = sender
    msg['To'] = ', '.join(receivers)
    msg.attach(MIMEText(text))
    try:
        smtpObj = smtplib.SMTP('mail.relayserver.name', port)
        smtpObj.sendmail(sender, receivers, msg.as_string())
        print "Successfully sent email"
    except SMTPException:
        print "Error: unable to send email"

def get_assume_arn_to_keys(Account_Number,Account_Name,ARN):
    print "inside assume_role"
    sts_client = boto3.client('sts')
    response = sts_client.assume_role(
        DurationSeconds=3600,ExternalId=Account_Name,
        Policy='{"Version":"2012-10-17","Statement":[{"Sid":"Stmt1","Effect":"Allow","Action":"workspaces:*","Resource":"*"}]}',
        RoleArn=ARN,RoleSessionName=Account_Name)
    aws_account_number = Account_Number
    aws_access_key = response['Credentials']['AccessKeyId']
    aws_secret_key = response['Credentials']['SecretAccessKey']
    aws_session_token = response['Credentials']['SessionToken']
    return (aws_account_number,aws_access_key,aws_secret_key,aws_session_token)
def workspace_creation():
    print 'inside workspace_creation'
    with open('/var/lib/jenkins/jobs/wokspace_creation/workspace_creation.json') as ec2_file:
        ec2_data = json.load(ec2_file)
        print (dict[1])
        for index in range(len(ec2_data['Items'])):
            Account_Name = ec2_data['Items'][index]['Acc_Name']
            if Account_Name == dict[4]:
                try:
                    Account_Number = ec2_data['Items'][index]['Aws_Account_Number']
                    ARN = ec2_data['Items'][index]['ARN']
                    b = get_assume_arn_to_keys(Account_Number,Account_Name,ARN)
                    client = boto3.client('workspaces',aws_access_key_id=b[1],aws_secret_access_key=b[2],region_name='region',aws_session_token=b[3])
                    response = client.create_workspaces(
                    Workspaces=[
                    {
                    'DirectoryId': dict[0],
                    'UserName': dict[1],
                    'BundleId': dict[2],
                    'WorkspaceProperties': {
                    'RunningMode': dict[3],
                    'RunningModeAutoStopTimeoutInMinutes': 60
                    },
                    'Tags': [
                    {
                    'Key': 'Account',
                    'Value': dict[4]

                    },
                    {
                    'Key': 'BU',
                    'Value': dict[5]

                    },
                    {
                    'Key': 'Billing',
                    'Value': dict[6]

                    },
                    {
                    'Key': 'NAME',
                    'Value': dict[7]

                    },

                    ]
                    },
                    ]
                    )
                    res = client.describe_workspace_directories(DirectoryIds= [dict[0]],)
                    #print(res)
                    #print(response)
                    a = res['Directories'][0]['RegistrationCode']
                    #b = json.loads(a)
                    print(a)
                    line = " in account " + dict[4]
                    msg =  "--------- Workspace is created "  + line + "---------" "\n" + " UserName: " +dict[1] + "\n"  +" Bundle-ID: "+dict[2] + "\n" " Directory-ID: " +dict[0]  + "\n" " Registration Code: " +a
                    mail(msg)
                except ClientError as e:
                   print(e)
def workspace_describe():
  with open('/var/lib/jenkins/jobs/wokspace_creation/workspace_creation.json') as ec2_file:
      ec2_data = json.load(ec2_file)
      for index in range(len(ec2_data['Items'])):
          Account_Number = ec2_data['Items'][index]['Aws_Account_Number']
          Account_Name = ec2_data['Items'][index]['Acc_Name']
          ARN = ec2_data['Items'][index]['ARN']
          b = get_assume_arn_to_keys(Account_Number,Account_Name,ARN)
          client = boto3.client('workspaces',aws_access_key_id=b[1],aws_secret_access_key=b[2],region_name='region',aws_session_token=b[3])
          paginator = client.get_paginator('describe_workspaces')
          page_iterator = paginator.paginate()
          for page in page_iterator:
               for workspace_stat_index in range(len(page['Workspaces'])):
                   usid = page['Workspaces'][workspace_stat_index]['UserName']
                   if (dict[8] == usid):
                       #dict[1] = usid
                       dict[2] = page['Workspaces'][workspace_stat_index]['BundleId']
                       dict[0] = page['Workspaces'][workspace_stat_index]['DirectoryId']
 # print ( dict)
  #print "done with workspace describe and now going to workspace creation"

  workspace_creation()


if (dict[9]=='True'):
    #print "dict8 value is true"
    workspace_describe()
else:
    #print "dict8 value is false"
    workspace_creation()
