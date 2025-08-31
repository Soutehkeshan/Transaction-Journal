import os
import gdown

# === Google Drive shared link ===
url = "https://drive.google.com/file/d/1An3PyEQ0odVhG91RVr_FneP1oIiTtTs1/view?usp=sharing"

# Extract file ID from the link
file_id = url.split("/d/")[1].split("/")[0]
download_url = f"https://drive.google.com/uc?id={file_id}"

# Ensure database folder exists
os.makedirs("database", exist_ok=True)

# Path to save database
output_path = os.path.join("database", "transactions.db")

# Download the file
gdown.download(download_url, output_path, quiet=False)

print(f"Database downloaded to {output_path}")
