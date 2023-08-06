# S3 Bucket Notifications Destinations

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

This module includes integration classes for using Topics, Queues or Lambdas
as S3 Notification Destinations.

## Examples

The following example shows how to send a notification to an SNS
topic when an object is created in an S3 bucket:

```python
# Example automatically generated from non-compiling source. May contain errors.
import aws_cdk.aws_s3_notifications as s3n

bucket = s3.Bucket(stack, "Bucket")
topic = sns.Topic(stack, "Topic")

bucket.add_event_notification(s3.EventType.OBJECT_CREATED_PUT, s3n.SnsDestination(topic))
```

The following example shows how to send a notification to a Lambda function when an object is created in an S3 bucket:

```python
# Example automatically generated from non-compiling source. May contain errors.
import aws_cdk.aws_s3_notifications as s3n

bucket = s3.Bucket(stack, "Bucket")
fn = Function(self, "MyFunction", {
    "runtime": Runtime.NODEJS_12_X,
    "handler": "index.handler",
    "code": Code.from_asset(path.join(__dirname, "lambda-handler"))
})

bucket.add_event_notification(s3.EventType.OBJECT_CREATED, s3n.LambdaDestination(fn))
```
