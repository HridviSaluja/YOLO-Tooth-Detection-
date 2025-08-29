import os
import random
import shutil
import yaml

# --------- CONFIG ---------
images_dir = r"C:\Users\HP\Downloads\ToothNumber_TaskDataset\images"   # folder containing all images
labels_dir = r"C:\Users\HP\Downloads\ToothNumber_TaskDataset\labels"   # folder containing YOLO txt labels
output_dir = r"C:\Users\HP\Downloads\ToothNumber_TaskDataset\split_dataset" # output folder where train/val/test will be created
yaml_path = os.path.join(output_dir, "data.yaml")  # yaml file path

# Classes (FDI system, 32 classes)
class_names = [
    "Canine (13)", "Canine (23)", "Canine (33)", "Canine (43)",
    "Central Incisor (21)", "Central Incisor (41)", "Central Incisor (31)", "Central Incisor (11)",
    "First Molar (16)", "First Molar (26)", "First Molar (36)", "First Molar (46)",
    "First Premolar (14)", "First Premolar (34)", "First Premolar (44)", "First Premolar (24)",
    "Lateral Incisor (22)", "Lateral Incisor (32)", "Lateral Incisor (42)", "Lateral Incisor (12)",
    "Second Molar (17)", "Second Molar (27)", "Second Molar (37)", "Second Molar (47)",
    "Second Premolar (15)", "Second Premolar (25)", "Second Premolar (35)", "Second Premolar (45)",
    "Third Molar (18)", "Third Molar (28)", "Third Molar (38)", "Third Molar (48)"
]

# --------- CREATE FOLDERS ---------
for split in ["train", "val", "test"]:
    os.makedirs(os.path.join(output_dir, split, "images"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, split, "labels"), exist_ok=True)

# --------- SPLIT DATA ---------
# Collect all images
images = [f for f in os.listdir(images_dir) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
random.shuffle(images)

# Ratios
train_split = int(0.8 * len(images))
val_split = int(0.9 * len(images))

train_files = images[:train_split]
val_files = images[train_split:val_split]
test_files = images[val_split:]

def copy_files(files, split):
    for f in files:
        # Copy image
        shutil.copy(os.path.join(images_dir, f), os.path.join(output_dir, split, "images", f))
        
        # Copy matching label
        label_file = os.path.splitext(f)[0] + ".txt"
        if os.path.exists(os.path.join(labels_dir, label_file)):
            shutil.copy(os.path.join(labels_dir, label_file), os.path.join(output_dir, split, "labels", label_file))
        else:
            print(f"⚠️ Warning: Label file missing for {f}")

copy_files(train_files, "train")
copy_files(val_files, "val")
copy_files(test_files, "test")

print("✅ Dataset split completed!")

# --------- CREATE data.yaml ---------
data_yaml = {
    "train": os.path.join(output_dir, "train", "images"),
    "val": os.path.join(output_dir, "val", "images"),
    "test": os.path.join(output_dir, "test", "images"),
    "nc": len(class_names),
    "names": {i: name for i, name in enumerate(class_names)}
}

with open(yaml_path, "w") as f:
    yaml.dump(data_yaml, f, sort_keys=False)

print(f"✅ data.yaml created at {yaml_path}")

