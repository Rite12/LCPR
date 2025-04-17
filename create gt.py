import os

#folder .tif
ground_truth_dir = "F:/Codes/LCPR/ground-truth"

plate_numbers = []
for filename in os.listdir(ground_truth_dir):
    if filename.endswith(".tif"):
        base_name = os.path.splitext(filename)[0]  
        parts = base_name.split("-")
        if len(parts) >= 3:
            plate = parts[2]
            plate_numbers.append(plate)
            
            gt_filename = base_name + ".gt.txt"
            gt_path = os.path.join(ground_truth_dir, gt_filename)
            with open(gt_path, "w") as gt_file:
                gt_file.write(plate)


print(f"✅ {len(plate_numbers)} file .gt berhasil dibuat.")
