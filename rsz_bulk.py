import subprocess
import time
import os
import argparse

# Function to parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description='Process Bitcoin addresses to find private keys.')
    parser.add_argument('--source', help='Path to the text file containing Bitcoin addresses', required=True)
    return parser.parse_args()

# Function to create output directory
def create_output_directory():
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

# Function to process each address
def process_addresses(addresses, output_dir):
    for address in addresses:
        # Command to run the rsz_rdiff_scan.py script
        command = ['python', 'rsz_rdiff_scan.py', '-a', address]

        # Notify which address is currently being processed
        print(f'Processing address: {address}')
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Collect the output and error messages
        stdout, stderr = process.communicate()

        # Check for private key found in the output
        private_key_found = False  # Flag to track if a private key is found
        for line in stdout.splitlines():
            if 'Privatekey FOUND:' in line:
                # Extract the private key and address from the line
                private_key = line.split(' ')[2]  # Extracting hex(d)
                found_address = line.split(' ')[-1]  # Extracting address
                print(f'Privatekey FOUND: {private_key} for Address: {found_address}')

                # Save the private key to a file named after the address
                address_file_path = os.path.join(output_dir, f"{found_address}.txt")
                with open(address_file_path, 'w') as key_file:
                    key_file.write(private_key)
                    print(f'Saved private key to {address_file_path}')
                    private_key_found = True

        if not private_key_found:
            print(f'No private key found for address: {address}')

        # Add a delay of 5 seconds before the next address
        time.sleep(5)

if __name__ == '__main__':
    # Parse command-line arguments
    args = parse_arguments()

    # Create output directory
    output_dir = create_output_directory()

    # Read addresses from the specified source file
    with open(args.source, 'r') as file:
        addresses = file.read().splitlines()

    # Process the addresses
    process_addresses(addresses, output_dir)

    print('Processing finished for all addresses.')
