import subprocess
import time

# Set the duration of time to monitor GPU utilization (in seconds)
monitor_duration = 60

# Get the current time in milliseconds
start_time_ms = int(time.time() * 1000)

# Open the output file for writing
with open('gpu_utilization.txt', 'w') as f:

    # Continuously monitor GPU utilization until the time limit is reached
    while int(time.time() * 1000) < start_time_ms + (monitor_duration * 1000):
    
        # Run nvidia-smi and capture the output
        nvidia_smi_output = subprocess.check_output(['nvidia-smi'])

        # Decode the output to a string
        output_string = nvidia_smi_output.decode('utf-8')
        # Split the output into lines
        output_lines = output_string.split('\n')

        # Find the line that contains the GPU utilization data
        utilization_line = output_lines[9]

        # Extract the GPU utilization data from the line
        if utilization_line[61]==' ' :
            gpu_utilization = int(utilization_line[62])
        else:
            #print(int(utilization_line[62]))
            gpu_utilization =int(utilization_line[61])*10+int(utilization_line[62])

        # Write the GPU utilization data to the output file
        f.write(str(gpu_utilization) + '\n')

        # Wait for a short period of time before checking GPU utilization again
        time.sleep(1)
