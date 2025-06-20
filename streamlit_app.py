
import os
import xml.etree.ElementTree as ET
import pandas as pd
import streamlit as st

# Mapping
type_map = {'A': 'SSTA', 'B': 'SSTB', 'C': 'SSTC', 'E': 'SSTE'}

# Paths
base_input_folder = '/Users/thomas/FTP/TCHIBO/SSTA KOMPLET'
base_processed_folder = '/Users/thomas/Nordisk Company A S/Nordisk Company A S Team Site - BC/Tchibo/Processed'
xml_tag = 'VBELN'

# Functions
def get_recent_tag_values(folder_path, tag, limit):
    file_infos = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.xml'):
            file_path = os.path.join(folder_path, filename)
            try:
                mtime = os.path.getmtime(file_path)
                file_infos.append((mtime, file_path))
            except:
                continue
    file_infos.sort(key=lambda x: x[0], reverse=True)
    values = []
    for _, file_path in file_infos[:limit]:
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            elem = root.find(f'.//{tag}')
            if elem is not None and elem.text:
                values.append(elem.text.strip())
        except:
            continue
    return values

def get_all_tag_values(folder_path, tag):
    values = set()
    for filename in os.listdir(folder_path):
        if filename.endswith('.xml'):
            file_path = os.path.join(folder_path, filename)
            try:
                tree = ET.parse(file_path)
                root = tree.getroot()
                elem = root.find(f'.//{tag}')
                if elem is not None and elem.text:
                    values.add(elem.text.strip())
            except:
                continue
    return values

# Streamlit UI
st.title("Tchibo File Processing Check")

n_records = st.number_input("How many recent files to check?", min_value=100, max_value=100000, value=10000, step=500)

recentA = get_recent_tag_values(base_input_folder, xml_tag, n_records)

for key, code in type_map.items():
    st.subheader(f"Check for {code}")
    folderB = f"{base_processed_folder}/{code}_Processed"
    allB = get_all_tag_values(folderB, xml_tag)

    if code == "SSTE":
        found = [v for v in recentA if v in allB]
        df = pd.DataFrame(found, columns=["VBELN found NORDISK"])
    else:
        missing = [v for v in recentA if v not in allB]
        df = pd.DataFrame(missing, columns=["VBELN not in NORDISK folders"])

    if df.empty:
        st.success(f"✅ All {len(recentA)} records found in {code}_Processed.")
    else:
        st.warning(f"⚠️ {len(df)} records missing in {code}_Processed.")
        st.dataframe(df)
        st.download_button(f"Download missing list for {code}", df.to_csv(index=False), file_name=f"{code}_check.csv")


ChatGPT sagde:
Thanks for sharing the full code. Here's how you can update it so your app doesn't crash on Streamlit Cloud when it can't find the local directories.

❗ Problem
You're using absolute paths:

python
Kopiér
Rediger
base_input_folder = '/Users/thomas/FTP/TCHIBO/SSTA KOMPLET'
base_processed_folder = '/Users/thomas/Nordisk Company A S/Nordisk Company A S Team Site - BC/Tchibo/Processed'
These won’t exist on Streamlit Cloud, leading to errors like:

python
Kopiér
Rediger
FileNotFoundError: [Errno 2] No such file or directory: ...
✅ Fix
Add existence checks inside get_recent_tag_values() and get_all_tag_values().

Provide clear error messages using Streamlit's st.error() instead of crashing.

💡 Updated Functions With Checks
Here's your updated code with safe checks:

python
Kopiér
Rediger
def get_recent_tag_values(folder_path, tag, limit):
    if not os.path.exists(folder_path):
        st.error(f"🚫 Input folder not found: `{folder_path}`")
        return []

    file_infos = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.xml'):
            file_path = os.path.join(folder_path, filename)
            try:
                mtime = os.path.getmtime(file_path)
                file_infos.append((mtime, file_path))
            except:
                continue
    file_infos.sort(key=lambda x: x[0], reverse=True)
    values = []
    for _, file_path in file_infos[:limit]:
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            elem = root.find(f'.//{tag}')
            if elem is not None and elem.text:
                values.append(elem.text.strip())
        except:
            continue
    return values

def get_all_tag_values(folder_path, tag):
    if not os.path.exists(folder_path):
        st.error(f"🚫 Processed folder not found: `{folder_path}`")
        return set()

    values = set()
    for filename in os.listdir(folder_path):
        if filename.endswith('.xml'):
            file_path = os.path.join(folder_path, filename)
            try:
                tree = ET.parse(file_path)
                root = tree.getroot()
                elem = root.find(f'.//{tag}')
                if elem is not None and elem.text:
                    values.add(elem.text.strip())
            except:
                continue
    return values
🧪 Optional: Add Environment Detection
You can optionally detect if you’re running on Streamlit Cloud (which uses a Linux-based environment) and use dummy or test folders:

python
Kopiér
Rediger
is_cloud = not os.path.exists('/Users')  # crude but effective

if is_cloud:
    base_input_folder = './data/input'
    base_processed_folder = './data/processed'
else:
    base_input_folder = '/Users/thomas/FTP/TCHIBO/SSTA KOMPLET'
    base_processed_folder = '/Users/thomas/Nordisk Company A S/Nordisk Company A S Team Site - BC/Tchibo/Processed'
Let me know if you’d like help turning this into a file upload version that works on Streamlit Cloud!








Kan du lide denne personlighed?







Værktøjer



ChatGPT kan tage fejl. Vi anbefaler at dobbelttjekke vigtig information.
