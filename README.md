# aws-tools

Shell utilities for AWS operations written on Python.


----------


ec2top.py - listing of your EC2 machines

    newuser@vbox:~$ ec2top --sort Type
    i-9262c07c          stopped    c3.large  54.84.57.91     10.155.4.105    vpc-8e9861e2   db2012-compute-01
    i-0f4e12fe047c8968b running    c3.large  54.165.160.131  10.155.4.98     vpc-8e9861e2   dev-auto-s3-compute101
    i-0b545c4b945aa6183 running    c3.large  54.236.202.212  10.155.2.199    vpc-8e9861e2   dev-compute-01
    i-0ce03d96ac577bba0 running    c3.large  34.192.41.156   10.155.2.241    vpc-8e9861e2   dev-compute-01-phx
    i-0401332de32993d1e running    c3.large  54.172.49.236   10.155.4.238    vpc-8e9861e2   dev-compute-02
    i-c8d6b639          stopped    c3.large  54.88.208.204   10.155.4.4      vpc-8e9861e2   dev-compute-03


----------


ec2runner.py - starting/stopping instances.

Example:

    newuser@vbox:~$ ec2runner --profile default --region us-east-1 stop i-007f29708864cc40b
    Response code: 200
    Instance:i-007f29708864cc40b running => stopping


----------

scrcleaner.py - explore and clean your EC2 Container Registry (ECR)

Example:

    root@vbox:/opt/mygithub# ./ecrcleaner.py -l esl-back
    66**********.dkr.ecr.us-east-1.amazonaws.com/esl-back

    43 / 1000 images
    
    Last pushed images:
    2018-11-21 14:56:33 ['19.1-d434']
    2018-11-21 13:10:30 ['19.1-d433']
    2018-11-21 05:40:42 notags
    2018-11-21 00:29:58 ['19.1-d432']
    2018-11-20 21:13:40 ['19.1-d431']
    2018-11-20 04:12:14 ['19.1-d430']
    2018-11-19 23:01:28 ['19.1-d429']
    2018-11-19 19:21:17 ['19.1-d428']
    2018-11-19 13:12:29 ['19.1-d427']
    root@vbox:/opt/mygithub# ./ecrcleaner.py -d 3 esl-back
    34 images will be deleted.
    [Yes/No] ?
    no
    root@vbox:/opt/mygithub#

    

----------


amilist.py - AMI listing

Example:

    newuser@vbox:~$ amilist.py|head -10|sort -k2
    ami-00e60416: Centos-6 2017-01-13 12-10-07
    ami-040ddc7e: devops-infra-amazonlinux-1.22.0-SNAPSHOT-hvm-20171017094118032
    ami-02af3c78: devops-infra-amazonlinux-1.22.0-SNAPSHOT-hvm-20171127115712474
    ami-0192c27b: devops-infra-amazonlinux-1.22.0-SNAPSHOT-hvm-20180105113209206
    ami-0403107f: devops-infra-centos-1.0.0-SNAPSHOT-hvm-20170906110115204
    ami-0216bb78: devops-infra-cis-centos-1.0.0-SNAPSHOT-hvm-20171030085909632
    ami-034c7e14: devops-infra-sles-11.4.9-hvm
    ami-08ae9460: emr 3.7.0-ami-roller-20 paravirtual is


----------


sgparser.py - Parsing of Security Groups to CSV-compatible format for each rule. Can be handy for importing output to rdatabases.

Example:

    newuser@vbox:~$ ./sgparser.py --profile default --region us-east-1
    sg-d2161bba, default, default group, 0.0.0.0/0, tcp, 22, 22
    sg-930d07fb, dev-ds-custom-01, dev-ds-custom-01, 0.0.0.0/0, tcp, 22, 22
    sg-2e16b645, AWS-OpsWorks-Rails-App-Server, AWS OpsWorks Rails-App server - do not change or delete, 0.0.0.0/0, tcp, 22, 22
    sg-2e16b645, AWS-OpsWorks-Rails-App-Server, AWS OpsWorks Rails-App server - do not change or delete, 0.0.0.0/0, tcp, 80, 80
    sg-2e16b645, AWS-OpsWorks-Rails-App-Server, AWS OpsWorks Rails-App server - do not change or delete, 0.0.0.0/0, tcp, 443, 443
    sg-2c16b647, AWS-OpsWorks-PHP-App-Server, AWS OpsWorks PHP-App server - do not change or delete, 0.0.0.0/0, tcp, 22, 22
    sg-2c16b647, AWS-OpsWorks-PHP-App-Server, AWS OpsWorks PHP-App server - do not change or delete, 0.0.0.0/0, tcp, 80, 80
    sg-2c16b647, AWS-OpsWorks-PHP-App-Server, AWS OpsWorks PHP-App server - do not change or delete, 0.0.0.0/0, tcp, 443, 443

