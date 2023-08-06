# Snitch AI Python Client Library

This library is used to perform Snitch AI analyses in a programmatic manner. This allows for easier upload
to the Snitch AI platform without having to use the UI. Additionally, this library can facilitate integration
with existing MLOps pipelines and external reporting tools.

## Usage:

### Generate a quality report

```
import snitch_ai

# you can specify the access_token in code or set the SNITCH_ACCESS_TOKEN environment variable 
snitch_ai.access_token = "VGhpcyBpcyBub3QgYW4gYWN0dWFsIGFjY2VzcyB0b2tlbi4gVG8gZ2V0I..."

project = snitch_ai.select_project("My First Project")

quality = project.run_quality_analysis(model, train_x, train_y, test_x, test_y)

json = quality.get_json()
quality.save_pdf("My Quality Report.pdf")
```

### Generate a drift report

```
import snitch_ai

# you can specify the access_token in code or set the SNITCH_ACCESS_TOKEN environment variable
snitch_ai.access_token = "VGhpcyBpcyBub3QgYW4gYWN0dWFsIGFjY2VzcyB0b2tlbi4gVG8gZ2V0I..."

project = snitch_ai.select_project("My First Project")

drift = project.run_drift_analysis(train_x, updated_x)

json = drift.get_json()
drift.save_pdf("My Drift Report.pdf")
```

### Usage within a hybrid environment

Snitch AI can also be used in a hybrid environment. This gives you the full power of Snitch AI's analysis
engine without needing to upload your models or datasets to the cloud. If your internal security policy
forbids uploading your data to a public cloud, this will likely be your preferred method of using Snitch AI.

You can learn more about Snitch AI Hybrid here: https://www.snit.ch/hybrid/
```
import snitch_ai

# replace this address with the address of your on-premises Snitch AI environment
# you can also set this in the SNITCH_ENDPOINT_ADDRESS environment variable
snitch_ai.endpoint_address = "https://localhost:5443/"

# you can specify the access_token in code or set the SNITCH_ACCESS_TOKEN environment variable
snitch_ai.access_token = "VGhpcyBpcyBub3QgYW4gYWN0dWFsIGFjY2VzcyB0b2tlbi4gVG8gZ2V0I..."

# perform quality or drift analysis per usual

```

Full product documentation can be found at https://help.snit.ch/