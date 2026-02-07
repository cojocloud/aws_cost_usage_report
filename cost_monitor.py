import boto3
import yaml
import sys
from datetime import datetime

def load_config():
    """Load configuration from config.yaml"""
    try:
        with open('config.yaml', 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print("Error: config.yaml not found")
        sys.exit(1)

def get_monthly_cost():
    """Fetch current month AWS costs using boto3"""
    try:
        client = boto3.client('ce', region_name='ca-central-1')
        
        # Get first day of current month and today
        today = datetime.now()
        start = today.replace(day=1).strftime('%Y-%m-%d')
        end = today.strftime('%Y-%m-%d')
        
        response = client.get_cost_and_usage(
            TimePeriod={'Start': start, 'End': end},
            Granularity='MONTHLY',
            Metrics=['UnblendedCost']
        )
        
        cost = float(response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount'])
        return round(cost, 2)
    except Exception as e:
        raise Exception(f"Failed to fetch AWS costs: {str(e)}")

def check_budget(current_cost, budget, threshold_pct):
    """Compare current cost against budget and return status"""
    percentage = (current_cost / budget) * 100
    
    if percentage >= 100:
        status = "❌ OVER BUDGET"
    elif percentage >= threshold_pct:
        status = "⚠️  WARNING"
    else:
        status = "✅ OK"
    
    return status, percentage

def main():
    print("\n📊 AWS Cost Monitor\n")
    
    try:
        # Load configuration
        config = load_config()
        
        # Get current AWS costs
        print("Fetching AWS costs...")
        current_cost = get_monthly_cost()
        
        # Check against budget
        status, percentage = check_budget(
            current_cost,
            config['budget_threshold'],
            config['alert_threshold_percentage']
        )
        
        # Display results
        print(f"\nCurrent Month Spending: ${current_cost:.2f}")
        print(f"Budget: ${config['budget_threshold']:.2f}")
        print(f"Status: {status} ({percentage:.1f}%)\n")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure:")
        print("1. AWS credentials are configured (run: aws configure)")
        print("2. Your IAM user has ce:GetCostAndUsage permission")
        sys.exit(1)

if __name__ == "__main__":
    main()