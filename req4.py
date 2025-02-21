import boto3
import json
#mock for create "aws_validation.json"
from unittest.mock import MagicMock

def get_instance_details(instance_id):
    ec2_client = boto3.client('ec2')
    try:
        response = ec2_client.describe_instances(InstanceIds=[instance_id])
    except Exception as e:
        raise Exception(f"Error retrieving EC2 instance data: {str(e)}")

    reservations = response.get('Reservations', [])
    if not reservations:
        raise Exception(f"No reservation found for the provided instance ID: {instance_id}")

    instances = reservations[0].get('Instances', [])
    if not instances:
        raise Exception(f"No instance data found for instance ID: {instance_id}")

    instance = instances[0]
    instance_state = instance['State']['Name']
    public_ip = instance.get('PublicIpAddress', 'Not Available')

    if instance_state != 'running':
        raise Exception(f"Instance {instance_id} is not running. Current state: {instance_state}")

    return {
        'instance_id': instance_id,
        'state': instance_state,
        'public_ip': public_ip}

def get_load_balancer_details(load_balancer_name):
    """Fetch details of a Load Balancer."""
    elbv2_client = boto3.client('elbv2')
    try:
        response = elbv2_client.describe_load_balancers(Names=[load_balancer_name])
    except Exception as e:
        raise Exception(f"Error retrieving ALB data: {str(e)}")

    load_balancers = response.get('LoadBalancers', [])
    if not load_balancers:
        raise Exception(f"No Load Balancer found with the name: {load_balancer_name}")

    load_balancer = load_balancers[0]
    return {
        'alb_name': load_balancer_name,
        'dns_name': load_balancer['DNSName']}
    
def main():
    mock_ec2_client = MagicMock()     # Mock EC2 client behavior
    mock_ec2_client.describe_instances.return_value = {
        'Reservations': [{
            'Instances': [{
                'State': {'Name': 'running'},
                'PublicIpAddress': '123.45.67.89',}]}]}

    mock_elbv2_client = MagicMock()     # Mock ALB client behavior
    mock_elbv2_client.describe_load_balancers.return_value = {
        'LoadBalancers': [{
            'DNSName': 'mock-alb-123.elb.amazonaws.com'}]}

    boto3.client = MagicMock(side_effect=lambda service_name: mock_ec2_client if service_name == 'ec2' else mock_elbv2_client)     # Replace to mock clients

    ec2_instance_id = 'mock-instance-id'
    load_balancer_name = 'mock-alb-name'

    print("Fetching EC2 instance details")
    ec2_data = get_instance_details(ec2_instance_id)
    print(f"EC2 Instance details fetched successfully:
          \nInstance ID: {ec2_data['instance_id']}, State: {ec2_data['state']}, Public IP: {ec2_data['public_ip']}")

    print("\nFetching Load Balancer details")
    alb_data = get_load_balancer_details(load_balancer_name)
    print(f"Load Balancer details fetched successfully:
          \nALB Name: {alb_data['alb_name']}, DNS Name: {alb_data['dns_name']}")

    # Save the collected validation data to aws_validation.json
    validation_data = {
        'ec2': ec2_data,
        'alb': alb_data
    }

    print("\nSaving validation data to 'aws_validation.json':")
    with open('aws_validation.json', 'w') as json_file:
        json.dump(validation_data, json_file, indent=2)
    print("Validation data is saved")

if __name__ == "__main__":
    main()
