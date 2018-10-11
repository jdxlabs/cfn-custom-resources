# cfn-custom-resources

AWS CloudFormation : Usefull custom resources

## Instructions

You will create 2 custom resources for your CloudFormation templates : 
- A resource to retrieve credentials in Secrets Manager.
- A resource str-utils to make operations on strings, that's not natively included in CF for now.

### Create the secrets
```
aws secretsmanager create-secret --name "test/creds" --secret-string file://creds.json

# You can retrieve them in the cli like this : 
aws secretsmanager get-secret-value --secret-id "test/creds"
```

### Create your own S3 bucket, where you can store artifacts about CloudFormation and Lambda
```
cp cfn/params.json.dist cfn/params.json
# then edit cfn/params.json
# and set a unique name for your S3 bucket (the names are shared between AWS accounts)

aws cloudformation create-stack --stack-name cfn-exercise-s3 --template-body file://./cfn/create-s3.yml --parameters file://./cfn/params.json
```

### Deploy your lambda functions to S3
```
./deploy-lambda.sh <my-bucket>
```

### Create the lambda functions to be used by the custom resources
```
aws cloudformation create-stack --stack-name cfn-exercise-lambda-functions --template-body file://./cfn/create-lambda-functions.yml --parameters file://./cfn/params.json --capabilities CAPABILITY_NAMED_IAM
```

### Execute the custom resources directly from a new stack
```
aws cloudformation create-stack --stack-name cfn-exercise-custom-resources-usage --template-body file://./cfn/custom-resources-usage.yml --timeout-in-minutes 5
```
Now you should see your outputs processed by the custom ressources !


## Clean up

### Once it's done, you should delete your stacks
```
aws cloudformation delete-stack --stack-name cfn-exercise-custom-resources-usage
aws cloudformation delete-stack --stack-name cfn-exercise-lambda-functions
aws cloudformation delete-stack --stack-name cfn-exercise-s3
```
