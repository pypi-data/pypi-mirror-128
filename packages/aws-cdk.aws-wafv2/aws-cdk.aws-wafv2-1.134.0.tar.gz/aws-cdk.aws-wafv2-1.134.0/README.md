# AWS::WAFv2 Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_wafv2 as wafv2
```

## Examples

Create a simple WebACL resource.

```csharp
var WebACL = new CfnWebACL(this, "WebACL", new CfnWebACLProps{
   Name = "MyWebACL",
   Scope = "REGIONAL",
   DefaultAction =  new CfnWebACL.DefaultActionProperty {
       Allow = new CfnWebACL.AllowActionProperty{}
   },
   VisibilityConfig = new CfnWebACL.VisibilityConfigProperty {
       SampledRequestsEnabled = true,
       CloudWatchMetricsEnabled = true,
       MetricName = "WebACL",
   },
   Rules = new CfnWebACL.RuleProperty[] {}
  });
```
