# Alira Platform

## Table of Contents

-   [Roadmap](#roadmap)
-   [Solution architecture](#solution-architecture)
-   [Running a pipeline](#running-a-pipeline)
-   [Instances](#instances)
-   [Modules](#modules)
    -   [Map module](#map-module)
    -   [Selection module](#selection-module)
    -   [Flagging module](#flagging-module)
    -   [Dashboard module](#dashboard-module)
    -   [Email Notification module](#email-notification-module)
    -   [SMS Notification module](#sms-notification-module)
    -   [S3 module](#s3-module)
    -   [SocketIO module](#socketio-module)
-   [Implementing custom code](#implementing-custom-code)
-   [Running the test suite](#running-the-test-suite)

## Roadmap

Here is the overall roadmap for the project:

-   Season 0 - On-prem-enabled architecture
    -   On-prem exclusive deployments
    -   Ability to support offline processing of data
    -   Asynchronous module processing
    -   Integration with Boston Dynamics Spot
-   **Season 1 - Cloud-enabled architecture**
    -   Introduction of a data-collection endpoint (currently merged with hardware-specific functionality)
    -   Ability to deploy the solution in a cloud environment
    -   Support batch processing of data
    -   Integration with Skydio
-   Season 2 - Context-aware architecture
    -   Ability to maintain context around individual instances
    -   Implementation of context-dependent models

We are currently working on **Season 1** functionality. The rest of the documentation here represents the current version of project (Season 0). [Here you can find more information about Season 1](docs/season1.md).

## Solution architecture

The following diagram shows the architecture of the solution when deployed in Boston Dynamic's Spot robot:

![Solution architecture](docs/diagram.png)

### Components

-   `Spot Mission Controller`: A container responsible to serve as a bridge between Spot and the rest of the system.
-   `Model 1`, `Model 2`, ...: Containers representing every available model.
-   `Vinsa SDK`: The gateway to process every instance returned by the available models. Instances will run through the pipeline defined for each individual model. (The Vinsa SDK is precisely "Alira".)
-   `Store`: The database responsible from storing the data processed by the pipeline.
-   `Redis`: A Redis server in charge of processing any asynchronous operations.
-   `Dashboard`: A web application displaying real-time results as they are processed by the system.

## Running a pipeline

To run a pipeline, you can use the `alira.Pipeline` class. Here is an example of how to initialize it and run it:

```python
from alira import Pipeline

pipeline = Pipeline(
    configuration_directory="/path/to/model/folder",
    redis_server="redis://redis:6379/"
)
pipeline.run({
    "prediction": 1,
    "confidence": 0.85,
    "image": "image1.jpg",
    "metadata": {
        "sample": 123
    }
})
```

The `Pipeline` constructor receives the following arguments:

-   `configuration_directory`: The directory containing the pipeline configuration file. If `pipeline_configuration` is not specified, the `Pipeline` class will try to load the configuration from a file named `pipeline.yaml` in this directory.
-   `pipeline_configuration`: The path to the pipeline configuration file or a stream containing the configuration. This attribute is optional and mostly used for testing purposes. It's also useful in case you want to use a different configuration file than the one inside `configuration_directory`.
-   `redis_server`: The URL of the Redis server.

The `pipeline.run()` function returns the instance object created by the pipeline. Keep in mind that pipeline modules run asynchronously, so the returned instance will not contain any modifications made by the pipeline modules.

## Instances

An instance is an individual request sent through a pipeline. Instances are automatically created from the JSON object used when running the pipeline.

An instance is an object of the class `alira.instance.Instance` and has the following attributes:

-   `id`: A unique identifier associated to the instance.
-   `prediction`: `1` if the prediction is positive, `0` if negative.
-   `confidence`: A float between 0 and 1 indicating the confidence on the prediction.
-   `image`: The file associated with this instance.
-   `metadata`: A dictionary of metadata attributes associated with this instance. This property is initialized using all of the attributes in the JSON object used when running the pipeline.
-   `properties`: A dictionary of properties contributed by each module of the pipeline.

To get a specific attribute of an instance, use the `get_attribute()` method with the path to access the attribute. For example, to get the value of an attribute named `sample` that's part of the metadata of an instance, use `instance.get_attribute("metadata.sample")`. This method will raise an exception if the attribute does not exist. If you want to use a default value in case the attribute doesn't exist, use `instance.get_attribute("metadata.sample", default=0)`.

Internally, `get_attribute()` uses JMESPath to access attributes in the instance. For more information, check [JMESPath's specification](https://jmespath.org/specification.html).

You can create an instance directly from a JSON object using the `Instance.create()` static method. This method looks for top-level attributes that match the instance's properties. Everthing else that don't match will be automatically added as part of the `metadata` attribute. For example:

```python
instance = Instance.create({
    "prediction": 1,
    "confidence": 0.85,
    "image": "image1.jpg",
    "sample": 123,
    "hello": {
        "company": "levatas"
    },
    "metadata": {
        "value2": 234
    }
})
```

The above instance will end-up with the following attributes:

-   `instance.prediction` = 1
-   `instance.confidence` = 0.85
-   `instance.image` = `image1.jpg`
-   `instance.metadata` = `{ "sample": 123, "hello": { "company": "levatas" }, "value2": 234 }`

## Modules

### Map module

You can use the Map module to apply a given function to every instance processed by the pipeline.

A simple way to implement and reference a function is by using a pipeline.py file in the same directory as the configuration file. You can find more information about this under [Implementing custom code](#implementing-custom-code).

Here is an example:

```yaml
name: thermal

pipeline:
    - module: alira.modules.Map
      function: thermal.pipeline.map
```

The `Map` module defined above expects a function with the following signature:

```python
def map(instance) -> dict:
    return {
        "hello": "world"
    }
```

The properties returned by the function will be automatically added to the instance as part of its `properties` dictionary under a key derived from the name of the function. For example, the above setup will add a `thermal_pipeline_map` key to the instance's `properties` dictionary containing the result of the function.

If you specify the `module_id` attribute, the result of the module will be added to the instance's `properties` dictionary under that identifier. For example:

```yaml
name: thermal

pipeline:
    - module: alira.modules.Map
      module_id: sample
      function: thermal.pipeline.map
```

The result of the `map()` function will be added under `instance.properties["sample"]`.

### Selection module

You can use the Selection module to select a percentage of instances as they go through the pipeline and flag them for human review. Having a group of instances reviewed by humans gives the model a baseline understanding of its performance, and allows it to compute metrics that can later be extrapolated to all processed instances.

```yaml
name: thermal

pipeline:
    - module: alira.modules.Selection
      percentage: 0.2
```

The above example will extend `instance.properties` with a new `selected` attribute under the `selection` key. The value of this attribute will be `1` if the instance has been selected for review, and `0` otherwise.

### Flagging module

You can use the Flagging module to optimize the decision of routing instances for human review.

There are two implementations of the Flagging module:

-   `alira.modules.Flagging`
-   `alira.modules.CostSensitiveFlagging`

#### `alira.modules.Flagging`

This implementation optimizes the decision of routing instances to a human using a threshold. Any instance with a confidence below the threshold will be sent for human review.

```yaml
name: thermal

pipeline:
    - module: alira.modules.Flagging
      threshold: 0.7
```

This module will extend `instance.properties` with a new `flagging` key containing the attribute `flagged`. This attribute indicates whether the instance has been flagged for human review. This attribute is `1` if the instance has been flagged for review, and `0` otherwise.

#### `alira.modules.CostSensitiveFlagging`

This implementation uses cost sensitivity criteria to reduce the cost of mistakes.

```yaml
name: thermal

pipeline:
    - module: alira.modules.CostSensitiveFlagging
      fp_cost: 100
      fn_cost: 1000
      human_review_cost: 10
```

When configuring the module, you can specify the following attributes:

-   `fp_cost` (`float`): The cost of a false positive prediction. This attribute is optional and when not specified the module will assume the cost is `0`.
-   `fn_cost` (`float`): The cost of a false negative prediction. This attribute is optional and when not specified the module will assume the cost is `0`.
-   `human_review_cost` (`float`): The cost sending this instance for human review. This attribute is optional and when not specified the module will assume the cost is `0`.

This module will extend `instance.properties` with a new `flagging` key containing the following attributes:

-   `flagged`: Whether the instance has been flagged for human review. This attribute is `1` if the instance has been flagged for review, and `0` otherwise.
-   `cost_prediction_positive`: The cost associated with a positive prediction.
-   `cost_prediction_negative`: The cost associated with a negative prediction.

### Dashboard module

You can use the Dashboard module to extend an instance with properties required to render the dashboard. These are mostly user-friendly derivations of an instance's original properties This module also supports specifying any additional properties that you may want to display.

By default, the Dashboard module extends an instance with a dictionary under `instance.properties["dashboard"]` containing the following properties:

-   `prediction`: Either "Positive" if the prediction is `1`, or "Negative" if the prediction is `0`.
-   `confidence`: The confifence on the prediction rounded two `2` decimal places and the percentage sign. For example, `0.59245443` will be displayed as `59.24%`.
-   `selected`: Either "Yes" if the instance has been selected or flagged for review, or "No" otherwise.
-   `flagged`: Either "Yes" if the instance has been flagged for review, or "No" otherwise.

Here is an example configuration for the Dashboard module:

```yaml
name: thermal

pipeline:
    - module: alira.modules.Dashboard
      image: metadata.new_image
      attributes:
          confidence: This is the confidence
          metadata.temperature: Max Temperature
```

The Dashboard module supports the following attributes:

-   `image`: By default, the dashboard renders the image specified under the `instance.image` property. If you want to override this, you can use the `image` attribute to specify the instance's property from where the image should be taken. In the example above, the image will be taken from the `instance.metadata["new_image"]` property.

-   `attributes`: To extend the attributes that the dashboard displays for each instance, you can use `attributes`. This property can be a dictionary of attributes or a reference to an attribute of the instance that contains such dictionary. All of the attributes specified here will be displayed on the dashboard in addition to the default list. In this dictionary, the key represents the attribute and the value represents the label that will be used when displaying it. For example, the configuration before specifies two custom attributes:

    -   `confidence`: The dashboard will display the value of the `instance.confidence` property with a label "_This is the confidence_".
    -   `metadata.temperature`: The dashboard will display the value of the `instance.metadata["temperature"]` property with a label "_Max Temperature_."

    Another way to use the `attributes` property is by referencing an attribute of the instance. For example:

    ```yaml
    name: thermal

    pipeline:
        - module: alira.modules.Dashboard
          image: metadata.new_image
          attributes: metadata.attributes
    ```

    In this particular case, the custom attributes will be copied from `instance.metadata["attributes"]`. This should be a dictionary with the same structure specified above.

If the Dashboard module is not included as part of a pipeline, the pipeline will not be available in the dashboard.

### Email Notification module

You can use the Email Notification module to send email notifications to a list of email addresses. By default, this module uses AWS' Simple Email Service (SES) to send the notifications.

```yaml
name: thermal

pipeline:
    - module: alira.modules.notification.EmailNotification
      filtering: alira.instance.onlyPositiveInstances
      sender: thermal@levatas.com
      recipients:
          - user1@levatas.com
          - user2@levatas.com
      subject: Random subject
      template_html_filename: template.html
      template_text_filename: template.txt
      aws_access_key: [YOUR AWS ACCESS KEY]
      aws_secret_key: [YOUR AWS SECRET KEY]
      aws_region_name: [YOUR AWS REGION NAME]
```

Here is an example `template.html` file:

```html
<!DOCTYPE html>
<html>
    <body>
        <span>prediction:</span>
        <span>[[prediction]]</span>
        <span>confidence:</span>
        <span>[[confidence]]</span>
        <img src="[[properties.s3.public_url]]" />
    </body>
</html>
```

And here is an example `template.txt` file:

```txt
prediction: [[prediction]]
confidence: [[confidence]]
metadata_attribute: [[metadata.attr1]]
image: [[properties.s3.public_url]]
```

When configuring the module, you can specify the following attributes:

-   `filtering`: An optional function that will be used to filter the instance and decide whether the module should process it. If this function is not specified, the instance will be processed. For convenience purposes, there are two predefined functions that you can use:
    -   `alira.instance.onlyPositiveInstances`: Only positive instances will be considered.
    -   `alira.instance.onlyNegativeInstances`: Only negative instances will be considered.
-   `sender`: The email address where the notification will come from.
-   `recipients`: The list of email addresses that will receive the notification.
-   `subject`: The subject of the email notification.
-   `template_html_filename`: The name of the HTML template file that will be used to construct the email notification. This file should be located in the same directory as the pipeline configuration file.
-   `template_text_filename`: The name of the text template file that will be used to construct the email notification. This file should be located in the same directory as the pipeline configuration file.
-   `aws_access_key`: The access key to access AWS services. This attribute is optional and when not specified the module will attempt to use the environment variable `ALIRA_AWS_ACCESS_KEY_ID`.
-   `aws_secret_key`: The secret key to access AWS services. This attribute is optional and when not specified the module will attempt to use the environment variable `ALIRA_AWS_SECRET_ACCESS_KEY`.
-   `aws_region_name`: The name of the region hosting the AWS services. This attribute is optional and when not specified the module will attempt to use the environment variable `ALIRA_AWS_REGION_NAME`.

This module extends the instance with a dictionary under `properties.alira.modules.notifications.email` containing the following attributes:

-   `status`: The status of the operation. It's either `SUCCESS`, `FAILURE`, or `SKIPPED`. The latter happens whenever the instance has been filtered out by the function specified as the `filtering` attribute.
-   `message`: An optional message with more information about the status of the module execution.

### SMS Notification module

You can use the SMS Notification module to send text message notifications to a list of phone numbers. By default, this module uses [Twilio](https://twilio.com) to send the notifications.

```yaml
name: thermal

pipeline:
    - module: alira.modules.notification.SmsNotification
      filtering: alira.instance.onlyPositiveInstances
      image: properties.image_url
      sender: +11234567890
      recipients:
          - +11234567890
          - +11234567891
      template_text_filename: template.txt
      account_sid: [YOUR TWILIO ACCOUNT SID]
      auth_token: [YOUR TWILIO AUTH TOKEN]
```

Here is an example `template.txt` file:

```txt
prediction: [[prediction]]
confidence: [[confidence]]
metadata_attribute: [[metadata.attr1]]
```

When configuring the module, you can specify the following attributes:

-   `filtering`: An optional function that will be used to filter the instance and decide whether the module should process it. If this function is not specified, the instance will be processed. For convenience purposes, there are two predefined functions that you can use:
    -   `alira.instance.onlyPositiveInstances`: Only positive instances will be considered.
    -   `alira.instance.onlyNegativeInstances`: Only negative instances will be considered.
-   `image`: The property referencing an image URL that will be included in the notification. If this attribute is not specified, the message will not include an image. The value of this attribute should point to a publicly accessible URL.
-   `sender`: The phone number where the notifications will come from.
-   `recipients`: The list of phone numbers that will receive the notification.
-   `template_text_filename`: The name of the text template file that will be used to construct the notification. This file should be located in the same directory as the pipeline configuration file.
-   `account_sid`: Twilio's account sid. This attribute is optional and when not specified the module will attempt to use the environment variable `ALIRA_TWILIO_ACCOUNT_SI`.
-   `auth_token`: Twilio's authentication token. This attribute is optional and when not specified the module will attempt to use the environment variable `ALIRA_TWILIO_AUTH_TOKEN`.

This module extends the instance with a dictionary under `properties.alira.modules.notifications.sms` containing the following attributes:

-   `status`: The status of the operation. It's either `SUCCESS`, `FAILURE`, or `SKIPPED`. The latter happens whenever the instance has been filtered out by the function specified as the `filtering` attribute.
-   `message`: An optional message with more information about the status of the module execution.

### S3 module

You can use the S3 module to upload a file associated with an instance to an S3 location.

```yaml
name: thermal

pipeline:
    - module: alira.modules.S3
      filtering: alira.instance.onlyPositiveInstances
      file: image
      autogenerate_name: true
      aws_s3_bucket: sample-bucket
      aws_s3_key_prefix: images
      aws_s3_public: true
      aws_access_key: [YOUR AWS ACCESS KEY]
      aws_secret_key: [YOUR AWS SECRET KEY]
      aws_region_name: [YOUR AWS REGION NAME]
```

When configuring the module, you can specify the following attributes:

-   `module_id`: An optional identifier for this module. This identifier is used to construct the dictionary key that will be added to `instance.properties`. If `module_id` is not specified, the dictionary key will be `alira.modules.s3`.
-   `filtering`: An optional function that will be used to filter the instance and decide whether the module should process it. If this function is not specified, the instance will be processed. For convenience purposes, there are two predefined functions that you can use:
    -   `alira.instance.onlyPositiveInstances`: Only positive instances will be considered.
    -   `alira.instance.onlyNegativeInstances`: Only negative instances will be considered.
-   `file`: The property referencing the file that will be uploaded. If this attribute is not specified, the S3 module will upload the file referenced by the `instance.image` property. Files will be loaded relatively to the `/images` folder within the pipeline configuration directory.
-   `autogenerate_name`: If this attribute is `true`, the module will generate a unique name for the file. If this attribute is `false`, the module will use the original file's name. By default, this attribute is `false`.
-   `aws_s3_bucket`: The S3 bucket where the image will be stored.
-   `aws_s3_key_prefix`: The key prefix that will be used when storing this image in the S3 bucket.
-   `aws_s3_public`: Whther the image should be publicly accessible.
-   `aws_access_key`: The access key to access AWS services. This attribute is optional and when not specified the module will attempt to use the environment variable `ALIRA_AWS_ACCESS_KEY_ID`.
-   `aws_secret_key`: The secret key to access AWS services. This attribute is optional and when not specified the module will attempt to use the environment variable `ALIRA_AWS_SECRET_ACCESS_KEY`.
-   `aws_region_name`: The name of the region hosting the AWS services. This attribute is optional and when not specified the module will attempt to use the environment variable `ALIRA_AWS_REGION_NAME`.

This module extends the instance with a dictionary under `properties.alira.modules.s3` containing the following attributes (if the attribute `module_id` is specified, the dictionary key will have that name):

-   `status`: The status of the operation. It's either `SUCCESS`, `FAILURE`, or `SKIPPED`. The latter happens whenever the instance has been filtered out by the function specified as the `filtering` attribute.
-   `message`: An optional message with more information about the status of the module execution.
-   `file_url`: The URL of the file that was uploaded to S3.
-   `public_url`: The public URL of the file that was uploaded to S3. This property is only present if the `aws_s3_public` attribute was set to `true`.

### SocketIO module

You can use the SocketIO module to send notifications to a socketio endpoint. This module is useful to combine with the Dashboard module so users can receive real time notifications every time an instance is processed.

```yaml
name: thermal

pipeline:
    - module: alira.modules.notification.SocketIO
      endpoint: http://alira-dashboard:5003
```

When configuring the module, you can specify the following attributes:

-   `endpoint`: The URL of the socketio endpoint that will receive the notification. When running inside a swarm of containers, you can use the name of the dashboard container `alira-dashboard` to refer to the endpoint. The socket io port is `5003`.

This module should always be specified after the `Dashboard` module in a pipeline. It uses the attributes generated by the Dashboard module to construct the notification.

## Implementing custom code

Several modules require a function to do some sort of processing. For example, the [Map module](#map-module) requires a function that will be called to extend the supplied instance.

You can implement your own custom function by including a `pipeline.py` file in the same directory where the `pipeline.yml` file is located. The pipeline will automatically load this file and make every function in it available under the following namespace: `{pipeline name}.pipeline.{function name}`.

For example, look at the following `pipeline.py` file:

```python
def sample_function(instance: Instance) -> dict:
    return {
        "hello": "world"
    }
```

You can reference `sample_function()` from your `pipeline.yml` as follows:

```yaml
name: thermal

pipeline:
    - module: alira.modules.Map
      function: thermal.pipeline.sample_function
```

This is the breakdown of the `function` attribute:

-   `thermal`: The name of the pipeline.
-   `pipeline`: This is an arbitrary section indicating that this code is part of the `pipeline.py` file.
-   `sample_function`: The name of the function that will be called (this function should exist in the `pipeline.py` file.)

## Running the test suite

To run the test suite, you can follow the instructions below:

1. Create a `.env` file in the root of the project. (See below for the contents of the file.)
2. Create and activate a virtual environment
3. Install the requirements from the `requirements.txt` file
4. Run the unit tests using the `pytest` command.

```shell
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ pytest -s
```

Here is an example of the `.env` file:

```
ALIRA_AWS_ACCESS_KEY_ID=[your access key]
ALIRA_AWS_SECRET_ACCESS_KEY=[your secret key]
ALIRA_AWS_REGION_NAME=[your region name]

ALIRA_TWILIO_ACCOUNT_SID=[your Twilio account sid]
ALIRA_TWILIO_AUTH_TOKEN=[your Twilio auth token]

TEST_EMAIL_MODULE_SENDER=[your email address]
TEST_EMAIL_MODULE_RECIPIENT=[your email address]
TEST_SMS_MODULE_SENDER=[your phone number]
TEST_SMS_MODULE_RECIPIENT=[your phone number]
```

### Redis tests

Some of the tests require a Redis server to be running. To run these tests, you can follow the instructions below.

First, run a Redis server by downloading and starting a Redis container:

```shell
$ docker pull redis:6.2.5
$ docker container run -it --name redis -p 6379:6379 --rm redis:6.2.5
```

The test suite uses a queue named `tests`, so we need to run a Redis worker listening on this queue:

```shell
$ rq worker --with-scheduler --logging_level=INFO tests
```

With Redis and the worker running, you can run the tests:

```shell
$ pytest -s -m redis
```

### Integration tests

To run the integration tests, you can use the following command:

```shell
$ pytest -s -m integration
```
