import oci
import csv

# Define the necessary compartments (set your compartment OCID here)
COMPARTMENT_OCID = ""

# Initialize the OCI config
config = oci.config.from_file()  # Default location is ~/.oci/config

# Initialize Compute Client
compute_client = oci.core.ComputeClient(config)

# List all instances in the compartment
def list_instances(compartment_id):
    instances = []
    try:
        # Fetch the list of instances
        response = compute_client.list_instances(compartment_id)
        instances = response.data
    except oci.exceptions.ServiceError as e:
        print(f"Error fetching instances: {e}")
    
    return instances

# Get instance tags and other required details
def get_instance_details(instance):
    return {
        'Instance Name': instance.display_name,
        'Instance OCID': instance.id,
        'Lifecycle State': instance.lifecycle_state,
        'Availability Domain': instance.availability_domain,
        'Tags': instance.defined_tags,  # Custom tags
        'Freeform Tags': instance.freeform_tags  # Freeform tags
    }

# Export to CSV
def export_to_csv(instances_data, filename='running_instances_with_tags.csv'):
    # Define the CSV column headers
    fieldnames = ['Instance Name', 'Instance OCID', 'Lifecycle State', 'Availability Domain', 'Tags', 'Freeform Tags']

    # Write the data to the CSV file
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Write the instance data rows
        for instance_data in instances_data:
            writer.writerow(instance_data)

    print(f"Data successfully exported to {filename}")

# Main function
def main():
    # List all instances in the specified compartment
    instances = list_instances(COMPARTMENT_OCID)
    
    # Filter out only running instances
    running_instances = [instance for instance in instances if instance.lifecycle_state == 'RUNNING']

    # Get the details of each running instance
    instances_data = [get_instance_details(instance) for instance in running_instances]

    # Export to CSV
    export_to_csv(instances_data)

if __name__ == '__main__':
    main()