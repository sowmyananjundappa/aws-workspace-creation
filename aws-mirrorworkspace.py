import boto3
import json
import os
import sys
import types
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
dict_username=sys.argv[2]
dict[1]=dict_username.split(',')
dict[2]=sys.argv[3]
dict[3]=sys.argv[4]
dict[4]=sys.argv[5]
dict[5]=sys.argv[6]
dict[6]=sys.argv[7]
dict[7]=sys.argv[8]
dict[8]=sys.argv[9]
dict[9]=sys.argv[10]
dict_name=sys.argv[11]
dict[10]=dict_name.split(',')
dict[11]=sys.argv[12]
dict[12]=sys.argv[13]
print(dict)


def mail(text):
    sender = 'mail id'
    receivers = ['mail id reciver']
    now = time.strftime("%c")
    msg = MIMEMultipart()
    msg['Subject'] = 'AWS NewsUK Workspace creation in account ' + dict[4] + ' %s' %now
    msg['From'] = sender
    msg['To'] = ', '.join(receivers)
    msg.attach(MIMEText(text))
    try:
        smtpObj = smtplib.SMTP('mail.relay.server', port)
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
#for i in range(len(dict[1])):
  # print ("{}" .format (dict[0][i]))
 #       dict[1] = ("{}" .format (dict[1][i]))
#print (dict[1])



def workspace_creation():
    print 'inside workspace_creation'

    with open('/path for aws/role.json') as ec2_file:
        ec2_data = json.load(ec2_file)

     #   print (dict[1])
        for index in range(len(ec2_data['Items'])):
            Account_Name = ec2_data['Items'][index]['Acc_Name']
            if Account_Name == dict[5]:
                Account_Number = ec2_data['Items'][index]['Aws_Account_Number']
                ARN = ec2_data['Items'][index]['ARN']
                b = get_assume_arn_to_keys(Account_Number,Account_Name,ARN)
                client = boto3.client('workspaces',aws_access_key_id=b[1],aws_secret_access_key=b[2],region_name='eu-west-1',aws_session_token=b[3])
                n=0
                for i in range (len(dict[1])):
                    Name= [dict[10][n]]
                    print ("{}".format(dict[10][n]))
               # for i in range(len(dict[1])):
                    print ("{}" .format (dict[1][i]))
                  #for j in range (len(dict[10])):
                    #print ("{}".format (dict[10][j]))
                 #dict[1] = ("{}" .format (dict[1]))
                # print (dict[1])
                    response = client.create_workspaces(
                    Workspaces=[
                    {
                  'DirectoryId': dict[0],
                  'UserName': dict[1][i],
                  'BundleId': dict[2],
                  'WorkspaceProperties': {
                  'RunningMode': dict[3],
                  'RunningModeAutoStopTimeoutInMinutes': 60
                   },
                  'Tags': [
                     {
                     'Key': 'BUNDLE',
                     'Value': dict[4].upper()

                     },
                     {
                     'Key': 'ACCOUNT',
                     'Value': dict[5].upper()

                     },
                     {
                     'Key': 'STATUS',
                     'Value': dict[6].upper()

                     },
                     {
                     'Key': 'BU',
                     'Value': dict[7].upper()

                     },
                     {
                     'Key': 'BILLING',
                     'Value': dict[8].upper()

                     },
                     {
                     'Key': 'ENVIRONENT',
                     'Value': dict[9].upper()

                     },
                     {
                     'Key': 'FULL NAME',
                     'Value': dict[10][n].upper()

                     },

                     ]
                     },
                     ]
                     )
                    #n +=1
                   # res = client.describe_workspace_directories(DirectoryIds= [dict[0]],)
                            #print(res)
                            #print(response)
                   # a = res['Directories'][0]['RegistrationCode']
                            #b = json.loads(a)
                   # print(a)
                   # uname = dict[1][i]
                   # for uname in range(len(dict[1])):
                    res = client.describe_workspace_directories(DirectoryIds= [dict[0]],)
                    a = res['Directories'][0]['RegistrationCode']
                    print(a)
                    # print ("{}" .format (dict[1][uname]))
                    line = " in account " + dict[5]
                    msg =  "--------- Workspace is created "  + line + "---------" "\n" + " UserName: "+dict[1][i].upper()+ "\n"  +" Bundle-ID: "+dict[2] + "\n" " Directory-ID: " +dict[0]  + "\n" " Registration Code: " +a + "\n" +"Tags:" + "\n"+ "Account: " +dict[5] +"\n" + "BUNDLE: " +dict[4].upper() +"\n" + "STATUS: " +dict[6].upper() +"\n"+ "BU: " +dict[7].upper()+ "\n"+ "ENVIRONMENT: " +dict[9].upper()  +"\n" + "BILLING: " +dict[8].upper() +"\n" + "FULL NAME:" +dict[10][n].upper()
                    mail(msg)
                    n +=1
            #except ClientError as e:
              #     print(e)

                #print(response)
def workspace_describe():
  with open('/var/lib/jenkins/jobs/wokspace_creation/updated_tags.json') as ec2_file:
      ec2_data = json.load(ec2_file)
      for index in range(len(ec2_data['Items'])):
          Account_Number = ec2_data['Items'][index]['Aws_Account_Number']
          Account_Name = ec2_data['Items'][index]['Acc_Name']
          ARN = ec2_data['Items'][index]['ARN']
          b = get_assume_arn_to_keys(Account_Number,Account_Name,ARN)
          client = boto3.client('workspaces',aws_access_key_id=b[1],aws_secret_access_key=b[2],region_name='eu-west-1',aws_session_token=b[3])
          paginator = client.get_paginator('describe_workspaces')
          page_iterator = paginator.paginate()
          for page in page_iterator:
               for workspace_stat_index in range(len(page['Workspaces'])):
                   usid = page['Workspaces'][workspace_stat_index]['UserName']
                   if (dict[11].lower() == usid.lower()):
                       #dict[1] = usid
                       dict[2] = page['Workspaces'][workspace_stat_index]['BundleId']
                       dict[0] = page['Workspaces'][workspace_stat_index]['DirectoryId']
                      # Res_id = page['Workspaces'][workspace_stat_index]['WorkspaceId']
                       response = client.describe_tags(ResourceId= page['Workspaces'][workspace_stat_index]['WorkspaceId'])
                       dict[4]= response['TagList'][0]['Value']
                       dict[6]= response['TagList'][2]['Value']
                       dict[7]= response['TagList'][3]['Value']
                       dict[8]= response['TagList'][4]['Value']
                      # dict[9]= response['TagList'][5]['Value']
                      # dict[10]= response['TagList'][6]['Value']
                       print(response)

if (dict[12]=='True'):
    #print "dict8 value is true"
    workspace_describe()
else:
    #print "dict8 value is false"
    workspace_creation()
