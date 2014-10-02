#!/usr/bin/env python
from confu import atlas
from troposphere import (
    Template, FindInMap, GetAtt, Ref, Parameter, Join, Base64, Select, Output,
    ec2 as ec2
)


template = Template()

template.add_description('kafka')

atlas.infra_params(template)  # ssh_key, Env, Silo

atlas.conf_params(template)   # Conf Name, Conf Version, Conf tarball bucket

atlas.instance_params(
    template,
    roles_default=['kafka', ],
    iam_default='kafka',
)

atlas.scaling_params(template)

atlas.mappings(
    template,
    accounts=[atlas.poundpay],
)

kafka_secgrp = atlas.instance_secgrp(
    template,
    name="Kafka",
    SecurityGroupIngress=[
        ec2.SecurityGroupRule(
            'Consumers',
            IpProtocol='tcp',
            FromPort='6667',
            ToPort='6667',
            CidrIp=atlas.vpc_cidr,  #TODO: open 6667 for consumers only.
        ),
    ]
)

i_meta_data = {}
atlas.cfn_auth_metadata(i_meta_data)
atlas.cfn_init_metadata(i_meta_data)

i_launchconf = atlas.instance_launchconf(
    template,
    "KAFKA",
    Metadata=i_meta_data,
    SecurityGroups=[Ref(kafka_secgrp)],
)

scaling_group = atlas.instance_scalegrp(
    template,
    'Kafka',
    LaunchConfigurationName=Ref(i_launchconf),
    MinSize=Ref('MinSize'),
    MaxSize=Ref('MaxSize'),
    DesiredCapacity=Ref('DesiredCapacity'),
)

if __name__ == '__main__':
    print template.to_json(indent=4, sort_keys=True)
