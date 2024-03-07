import boto3
from datetime import datetime
import os

def stop_instances_with_shutdown_tag():
    # IAM access key and secret key
 
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

    region_name = 'ap-south-1'

    # Create an EC2 client
    ec2 = boto3.client('ec2', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    # Get current day of the week (0: Monday, 6: Sunday)
    current_day = datetime.now().weekday()

    # Check if it's a weekend (Saturday or Sunday)
    if current_day in [4]:  # 5: Saturday, 6: Sunday
        try:
            # Describe running instances
            response = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

            # Extract instance IDs with 'shutdown' tag
            instances_to_stop = []
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    for tag in instance.get('Tags', []):
                        if tag['Key'] == 'shutdown' and tag['Value'].lower() == 'true':
                            instances_to_stop.append(instance['InstanceId'])

            # Stop instances with 'shutdown' tag
            if instances_to_stop:
                ec2.stop_instances(InstanceIds=instances_to_stop)
                print("EC2 instances with tag 'shutdown' and in 'running' state have been stopped.")
            else:
                print("No EC2 instances with tag 'shutdown' found in 'running' state.")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("It's not a weekend. No action required.")

 

if __name__ == '__main__':
    # Call the function
    stop_instances_with_shutdown_tag()
