 AWS Cost Monitor CLI

A simple Python tool I built to keep track of AWS spending and avoid surprise bills at the end of the month.

**What it does:**

This script connects to your AWS account, checks how much you've spent so far this month, and lets you know if you're on track or heading over budget. No more logging into the AWS Console just to check costs.

**Built with:** Python 3.8+, boto3 (AWS SDK), and PyYAML

**Before you start, you'll need:**

- Python 3.8 or higher installed on your machine
- An AWS account with Cost Explorer turned on
- An IAM user that has permission to read cost data (specifically the `ce:GetCostAndUsage` permission)

---

**Getting it running:**

First, grab the code and set up your environment:
```bash
git clone https://github.com/cojocloud/aws_cost_usage_report.git
cd aws-cost-monitor
```

Create a virtual environment so your dependencies stay isolated:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install what you need:
```bash
pip install -r requirements.txt
```

Configure your AWS credentials (if you haven't already):
```bash
aws configure
```

You'll be asked for your AWS Access Key ID, Secret Access Key, and preferred region.

Now create your config file:
```bash
cp config.yaml.example config.yaml
```

Open `config.yaml` and set your budget:
```yaml
budget_threshold: 100.00          # How much you want to spend per month
aws_region: ca-central-1          # Your AWS region
alert_threshold_percentage: 80    # When to start warning you (80% = $80 of $100)
```

---

**Running the tool:**

Make sure your virtual environment is active, then run:
```bash
source venv/bin/activate
python cost_monitor.py
```

You'll see something like this:
```
📊 AWS Cost Monitor

Fetching AWS costs...

Current Month Spending: $28.80
Budget: $100.00
Status: ✅ OK (28.8%)
```

The status changes based on your spending:
- ✅ OK - You're under your alert threshold
- ⚠️ WARNING - You've hit your alert threshold (default 80%)
- ❌ OVER BUDGET - You've exceeded your monthly budget

---

**Setting up AWS properly:**

**Enabling Cost Explorer:**

If you've never used Cost Explorer before, you'll need to turn it on:

1. Log into AWS Console and go to the Billing Dashboard
2. Find "Cost Explorer" in the sidebar
3. Click "Enable Cost Explorer"
4. Wait about 24 hours for AWS to start collecting data

**IAM Permissions:**

Your AWS user needs permission to read cost data. Attach a policy with this permission:
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": ["ce:GetCostAndUsage"],
    "Resource": "*"
  }]
}
```

---

**Common issues and fixes:**

**"No module named 'boto3'"**

Your virtual environment probably isn't activated. Run `source venv/bin/activate` and try again. If that doesn't work, reinstall dependencies with `pip install -r requirements.txt`.

**"The security token included in the request is invalid"**

Your AWS credentials aren't set up correctly. Run `aws configure` again and double-check your Access Key ID and Secret Access Key. You can verify they work by running `aws sts get-caller-identity`.

**"User not enabled for cost explorer access"**

You need to enable Cost Explorer in the AWS Console (see the AWS Setup section above). After enabling it, you'll need to wait about 24 hours before data shows up.

**"AccessDeniedException"**

Your IAM user doesn't have the right permissions. Add the `ce:GetCostAndUsage` permission to your user or role.

---

**Why I built this:**

I got tired of constantly logging into AWS just to check if I was staying on budget. This tool lets me run a quick check from my terminal and see immediately if my costs are tracking normally or if something's gone wrong.

For teams, this is useful because:
- You catch cost spikes early, before they become real problems
- No one needs AWS Console access just to check spending
- It's simple enough to run in CI/CD pipelines or cron jobs
- You can set team-specific budgets and alerts

---

**What's next:**

Some ideas I'm considering for future versions:
- Email or Slack notifications when you go over budget
- Support for multiple AWS accounts
- Show cost trends over time
- Break down costs by service to see what's expensive
- Deploy as an AWS Lambda function for automatic scheduled checks

---

**License:** MIT - use it however you want
