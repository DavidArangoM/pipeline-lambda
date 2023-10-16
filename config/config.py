#Description: Accepted configuration with accepted values
configuration= {
    "trigger_out_types": {
        'lambda': r'^arn:aws:lambda:.*',
        'sns': r'^arn:aws:sns:.*',
        'sqs': r'^arn:aws:sqs:.*',
        'eventbridge': r'^arn:aws:events:.*'
    },
    "trigger_in_types": {
        's3': r'^arn:aws:s3:.*'
    }
}

#Description: Assume role policy to call lambdas services
lambda_assume_role_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"  # Example service, adjust as needed
            },
            "Action": "sts:AssumeRole"
        }
    ]
}

#Description: Custom policies to call another services or execute actions
lambda_role_custom_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            
            "Sid": "cloudwatchLogs",
            "Action": [
                "logs:*"
            ],
            "Effect": "Allow",
            "Resource": "*"
            
        },
        {
            
            "Sid": "lambdaCreateNetworkInterfaceToAttachVpcPolicy",
            "Effect": "Allow",
            "Action": "ec2:CreateNetworkInterface",
            "Resource": [
                "arn:aws:ec2:*:980952865757:network-interface/*",
                "arn:aws:ec2:*:980952865757:security-group/*",
                "arn:aws:ec2:*:980952865757:subnet/*"
            ]
        },                
        {
            "Sid": "lambdaDeleteNetworkInterfaceToAttachVpcPolicy",
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeNetworkInterfaces",
                "ec2:DeleteNetworkInterface"
            ],
            "Resource": "*"
        }, 
        {
           
            "Sid": "triggerOutPolicy",
            "Effect": "Allow",
            "Action": [
                "events:PutEvents",
                "sns:Publish",
                "lambda:InvokeFunction",
                "sqs:SendMessage"
            ],
            "Resource": "*"
           
        }
    ]
}


