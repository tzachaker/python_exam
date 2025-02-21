from python_terraform import Terraform
import json
import sys

def run_terraform():
    try:
        tf = Terraform()
        print("\nRunning Terraform init")
        return_code, stdout, stderr = tf.init()
        if return_code != 0:
            raise Exception(f"Terraform init failed:\n{stderr}")
        print(stdout)

        print("\nRunning Terraform plan")
        return_code, stdout, stderr = tf.plan()
        if return_code != 0:
            raise Exception(f"Terraform plan failed:\n{stderr}")
        print(stdout)

        print("\nRunning Terraform apply")
        return_code, stdout, stderr = tf.apply(skip_plan=True, auto_approve=True)
        if return_code != 0:
            raise Exception(f"Terraform apply failed:\n{stderr}")
        print(stdout)

        print("\nTerraform outputs:")
        return_code, stdout, stderr = tf.output(json=True)
        if return_code != 0:
            raise Exception(f"Terraform outputs failed:\n{stderr}")

        outputs = json.loads(stdout)
        print("\nTerraform outputs after success:")
        print(f"Instance ID: {outputs.get('instance_id', {}).get('value', 'N/A')}")
        print(f"Load Balancer DNS: {outputs.get('lb_dns_name', {}).get('value', 'N/A')}")

    except Exception as e:
        print(f"\nTerraform failed:\n{e}")
        sys.exit(1)

def main():
    run_terraform()
    print("\nTerraform runs successfully! ")

if __name__ == "__main__":
    main()
