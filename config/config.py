configuration= {
    "trigger_out_types": {
        'lambda': r'^arn:aws:lambda:.*',
        'sns': r'^arn:aws:sns:.*',
        'sqs': r'^arn:aws:sqs:.*',
        'eventbridge': r'^arn:aws:events:.*'
    }
}