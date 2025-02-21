from jinja2 import Template

ami_options = {
    "1": "ami-0dee1ac7107ae9f8c",
    "2": "ami-0f1a6835595fb9246"
}
instance_options = {
    "1": "t3.small",
    "2": "t3.medium"
}
#ami
print("Choose ami: [1] Ubuntu, [2] Amazon Linux ")
ami_choice = input("Enter your choice: ")
ami = ami_options.get(ami_choice, "ami-0dee1ac7107ae9f8c")
if ami_choice not in ami_options:
    print("Invalid choice for Ubuntu")

#instance type
print("Choose instance type: [1] t3.small, [2] t3.medium")
instance_choice = input("Enter your choice: ")
instance_type = instance_options.get(instance_choice, "t3.small")
if instance_choice not in instance_options:
    print("Invalid choice for t3.small.")

#region
region = input("Enter region but only us-east-1): ").strip()
if region != "us-east-1":
    print("Invalid region for us-east-1.")
    region = "us-east-1"

#alb
alb_name = input("Enter a name for ALB: ").strip()

# Template for your choices
template = Template("""
Summary:
--------
AMI: {{ ami }}
Instance Type: {{ instance_type }}
Region: {{ region }}
ALB Name: {{ alb_name }}
""")

# Print the summary
print(template.render(ami=ami, instance_type=instance_type, region=region, alb_name=alb_name))
