#!/usr/bin/python3

#
#     Listing of your AWS EC2 instances, RDS, Elasticache
# App require boto3 AWS-API module, make sure it is installed by running 'sudo pip3 install boto3'
# If no args specified app lists your EC2 instances using .aws/credentials "Default" profile and region. Use ./ec2top.py --help for possible options
#

import boto3, argparse
from operator import itemgetter

parser = argparse.ArgumentParser(description='AWS EC2 instances listing.')
parser.add_argument('-p', '--profile', action="store", dest="aws_profile", help='.aws/credentials profile name. Using "default" if not set')
parser.add_argument('-r', '--region', action="store", dest="aws_region", help='EC2 region name. Using "default" for your profile if not set')
parser.add_argument('-s', '--sort', action="store", dest="sort_key", help='Sort your output by column name. Default sorting is "Name". Other options are Status|Type|VPC|pubIP|privIP|Time. Works with --ec2 only. ')
group = parser.add_mutually_exclusive_group()
group.add_argument('--rds', action="store_true", default=False, help='RDS data')
group.add_argument('--ech', action="store_true", default=False, help='Elastic cache data')
group.add_argument('--elb', action="store_true", default=False, help='ELB data')
group.add_argument('--ec2', action="store_true", default=True, help='EC2 data (Default).')
args = parser.parse_args()

if args.ech or args.rds or args.elb:
    args.ec2 = False
#print(args)


if args.aws_profile:
    session = boto3.Session(profile_name=args.aws_profile)
else:
    session = boto3.Session()

#list of Tags dictionaries as input
def instance_name(tags):
    for i in tags:
        if i['Key'] == 'Name':
            return i['Value'].replace(' ', '_')

#VPC ID string as input
vpcnames = {}
def vpc_name(id):
    if id not in vpcnames.keys():
        if args.aws_profile:
            session = boto3.Session(profile_name=args.aws_profile)
        else:
            session = boto3.Session()
        if args.aws_region:
            ec2 = session.client('ec2', region_name=args.aws_region)
        else:
            ec2 = session.client('ec2')
        vpcdata = ec2.describe_vpcs()
        for vpci in vpcdata['Vpcs']:
            if vpci['VpcId'] == id:
                if 'Tags' not in vpci.keys():
                    vpci['Tags'] = [{'Value': 'NoNameAssigned', 'Key': 'Name'}]
                vpcname = instance_name(vpci['Tags'])
                if vpcname:
                    vpcname = vpcname.replace(' ', '_')
                else:
                    vpcname = 'NoVPCNameTag'
        vpcnames[id] = vpcname
        return vpcname
    else:
        return vpcnames[id]


if args.ec2:
    if args.aws_region:
        ec2 = session.client('ec2', region_name=args.aws_region)
    else:
        ec2 = session.client('ec2')
    response = ec2.describe_instances()

    fmt = '%Y-%m-%d %H:%M'
    top_list = []

    for i in range(len(response['Reservations'])):
        for r in range(len(response['Reservations'][i]['Instances'])):
            instance = response['Reservations'][i]['Instances'][r]
            top_instance = {}

            top_instance.setdefault('Status', instance['State']['Name'])
            top_instance.setdefault('Type', instance['InstanceType'])
            top_instance.setdefault('Id', instance['InstanceId'])
            top_instance.setdefault('Time', instance['LaunchTime'].strftime(fmt))
            if 'Tags' in instance.keys():
                top_instance.setdefault('Name', instance_name(instance['Tags']))
            else:
                top_instance.setdefault('Name', 'None')
                
            if 'PrivateIpAddress' in instance.keys():
                top_instance.setdefault('privIP', instance['PrivateIpAddress'])
            else:
                top_instance.setdefault('privIP', 'None')
            
            if 'PublicIpAddress' in instance.keys():
                top_instance.setdefault('pubIP', instance['PublicIpAddress'])
            else:
                top_instance.setdefault('pubIP', 'None')
            
            if 'VpcId' in instance.keys():
                top_instance.setdefault('VPC', instance['VpcId'])
                vpcname = vpc_name(instance['VpcId'])
                top_instance.setdefault('VPCname', vpcname)
            else:
                top_instance.setdefault('VPC', 'None')
                top_instance.setdefault('VPCname', 'None')
            
            if top_instance['Name'] is None:
                top_instance['Name'] = 'None'
            top_list.append(top_instance)

    sorted_list = sorted(top_list, key=itemgetter('Name'))

    if args.sort_key:
        sorted_list = sorted(sorted_list, key=itemgetter(args.sort_key))

    for i in range(len(sorted_list)):
        print(sorted_list[i]['Id'].ljust(20) + sorted_list[i]['Status'].ljust(11) + sorted_list[i]['Type'].ljust(12)\
        + sorted_list[i]['pubIP'].ljust(16) + sorted_list[i]['privIP'].ljust(16) + sorted_list[i]['VPC'].ljust(13) + sorted_list[i]['VPCname'][:16].ljust(17) + sorted_list[i]['Time'].ljust(17) + sorted_list[i]['Name'] )


if args.rds:
    if args.aws_region:
        rds = session.client('rds', region_name=args.aws_region)
    else:
        rds = session.client('rds')
    response = rds.describe_db_instances()

    top_list = []

    for i in response['DBInstances']:
        top_instance = {}
        top_instance.setdefault('DBInstanceIdentifier', i['DBInstanceIdentifier'])
        top_instance.setdefault('DBInstanceClass', i['DBInstanceClass'])
        top_instance.setdefault('DBInstanceStatus', i['DBInstanceStatus'])
        top_instance.setdefault('DBName', i['DBName'])
        top_instance.setdefault('AvailabilityZone', i['AvailabilityZone'])
        top_instance.setdefault('Engine', i['Engine'])
        top_instance.setdefault('EngineVersion', i['EngineVersion'])
        top_instance.setdefault('VpcId', i['DBSubnetGroup']['VpcId'])
        vpcname = vpc_name(i['DBSubnetGroup']['VpcId'])
        top_instance.setdefault('VPCname', vpcname)
        top_instance.setdefault('Endpoint', i['Endpoint']['Address'] + ':' + str(i['Endpoint']['Port']))

        top_list.append(top_instance)

    sorted_list = sorted(top_list, key=itemgetter('DBInstanceIdentifier'))

    for i in sorted_list:
        print(i['DBInstanceIdentifier'][:18].ljust(19) + i['DBName'][:12].ljust(13) + i['DBInstanceClass'].ljust(14) \
        + i['DBInstanceStatus'].ljust(11) + i['Engine'].ljust(12) + i['EngineVersion'].ljust(14) \
        + i['AvailabilityZone'].ljust(12) + i['VpcId'].ljust(13) + i['VPCname'][:15].ljust(16) + i['Endpoint'])


if args.ech:
    if args.aws_region:
        ech = session.client('elasticache', region_name=args.aws_region)
    else:
        ech = session.client('elasticache')
    response = ech.describe_cache_clusters()

    top_list = []

    for i in response['CacheClusters']:
        top_instance = {}
        top_instance.setdefault('CacheClusterId', i['CacheClusterId'])
        top_instance.setdefault('CacheNodeType', i['CacheNodeType'])
        top_instance.setdefault('CacheClusterStatus', i['CacheClusterStatus'])
        top_instance.setdefault('Engine', i['Engine'])
        top_instance.setdefault('EngineVersion', i['EngineVersion'])
        top_instance.setdefault('NumCacheNodes', i['NumCacheNodes'])
        top_instance.setdefault('PreferredAvailabilityZone', i['PreferredAvailabilityZone'])

        top_list.append(top_instance)
    
    sorted_list = sorted(top_list, key=itemgetter('CacheClusterId'))

    for i in sorted_list:
        print(i['CacheClusterId'].ljust(32) + i['CacheNodeType'].ljust(20) + i['CacheClusterStatus'].ljust(12) \
        + i['Engine'].ljust(12) + i['EngineVersion'].ljust(12) + str(i['NumCacheNodes']).ljust(5) + i['PreferredAvailabilityZone'].ljust(16))


if args.elb:
    if args.aws_region:
        elb = session.client('elb', region_name=args.aws_region)
    else:
        elb = session.client('elb')
    response = elb.describe_load_balancers()

    top_list = []
    for i in response['LoadBalancerDescriptions']:
        top_instance = {}
        top_instance.setdefault('DNSName', i['DNSName'])
        top_instance.setdefault('VPCId', i['VPCId'])
        vpcname = vpc_name(i['VPCId'])
        top_instance.setdefault('VPCname', vpcname)
        top_instance.setdefault('Scheme', i['Scheme'])
        
        listener = []
        for f in i['ListenerDescriptions']:
            listener.append('%s%d>%s%d' % (f['Listener']['Protocol'], f['Listener']['LoadBalancerPort'], f['Listener']['InstanceProtocol'], f['Listener']['InstancePort']) )
        top_instance.setdefault('Listener', ','.join(listener) + ' ' )
        
        fmt = '%Y-%m-%d_%H:%M'
        top_instance.setdefault('Created', i['CreatedTime'].strftime(fmt))
        
        top_list.append(top_instance)
    sorted_list = sorted(top_list, key=itemgetter('DNSName'))

    for i in sorted_list:
        print(i['DNSName'][:50].ljust(51) + i['Scheme'].ljust(16) + i['Listener'].ljust(30) + i['VPCId'].ljust(13) + i['VPCname'][:15].ljust(16) + i['Created'].ljust(20))

