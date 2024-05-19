import json


def handler(event, context):

    print("Hello world")
    print(event)
    print(context)

    return {
        "statusCode": 200,
        "headers": {},
        "body": json.dumps({"msg": "Hellow world"}),
    }
