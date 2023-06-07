import os

folder_path = "/home/rtcl/workspace/yolov5/runs/detect/exp1/labels/"
total_lines = 0

with open("obj_num.txt","w") as f:
    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        # Check if the file is a text file (you can modify this condition for your specific use case)
        if filename.endswith(".txt"):
            # Open the file and count the number of lines
            with open(os.path.join(folder_path, filename), "r") as file:
                num_lines = sum(1 for line in file)
                print(f"{filename} has {num_lines} lines")
                total_lines += num_lines
        f.write(str(num_lines))
        f.write("\n")
print(f"Total number of lines: {total_lines}")
