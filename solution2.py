import boto3
from datetime import datetime, timedelta
import dateutil.parser
ec2resource = boto3.resource('ec2')
ec2client = boto3.client('ec2')
class aws:
    
    def ec2instance(self):
        response = ec2client.describe_instances()
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                if(len(instance["NetworkInterfaces"])):
                    ti=instance["NetworkInterfaces"][0]['Attachment']['AttachTime']
                    tn=datetime.now()
                    tn = tn - timedelta(hours=168)
                    ti=str(ti)
                    tn=str(tn)
                    ti=dateutil.parser.parse(ti[0:19])
                    tn=dateutil.parser.parse(tn[0:19])
                    if(tn>ti):
                        print("............................")
                        print("Instance Name -->", instance['Tags'][0]['Value'])
                        print("Instance Id -->",instance["InstanceId"])
                        print("Instance Type -->",instance["InstanceType"])
                        print("Instance State-->",instance['State']['Name'])
                        instances = ec2resource.Instance(instance["InstanceId"])
                        volumes = instances.volumes.all()
                        l=[]
                        for v in volumes:
                            l.append(v.id)
                        print("No Of Volumes-->",len(l))
                        print("............................")
                    
    def elasticip(self):
        addresses_dict = ec2client.describe_addresses()
        if(len(addresses_dict['Addresses']) == 0):
            print("No Elastic Ip's associated")
        else:
            for eip_dict in addresses_dict['Addresses']:
                print(eip_dict['PublicIp'])
    def securitygrp(self):
        vpc_id = 'vpc-b95ffed2'
        response = ec2client.create_security_group(GroupName='SECURITY_GROUP_NAME',
                                         Description='DESCRIPTION',
                                         VpcId=vpc_id)
        security_group_id = response['GroupId']
        print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))
        data = ec2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {'IpProtocol': 'tcp',
             'FromPort': 22,
             'ToPort': 22,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp',
             'FromPort': 22,
             'ToPort': 22,
             'IpRanges': [{'CidrIp': '172.0.0.0/24'}]}
        ])
        print('Ingress Successfully Set...!')
        return security_group_id
    def instance(self,grpid):
        instances = ec2resource.create_instances(
            ImageId='ami-04fcd96153cb57194', 
            MinCount=1, 
            MaxCount=1,
            KeyName="sample",
            InstanceType="t2.micro",
            SecurityGroupIds=[grpid]
            )
        print("Instance Created Sucessfully....!")
        time.sleep(45)
        response = ec2client.describe_instances()
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                if(instance["InstanceId"]==instances[0].id):
                    zone=instance["Placement"]["AvailabilityZone"]
        l=['/dev/sdm','/dev/sdf']
        for i in range(2):
            ebs_vol = ec2client.create_volume(
                Size=2,
                AvailabilityZone=zone
                )
            volumeId=ebs_vol['VolumeId']
            time.sleep(30)
            attach_resp = ec2client.attach_volume(
                VolumeId=volumeId,
                InstanceId=instances[0].id,
                Device=l[i]
                )
        print("EBS volume Created and Attached Sucessfully....! ")
a=aws()
a.ec2instance()
a.elasticip()
grpid=a.securitygrp()
a.instance(grpid)

