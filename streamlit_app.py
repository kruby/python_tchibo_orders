import streamlit as st

st.title("Tchibo Orders")


import os
import xml.etree.ElementTree as ET
import pandas as pd

# Mapping
type_map = {'A': 'SSTA', 'B': 'SSTB', 'C': 'SSTC', 'E': 'SSTE'}

# Paths
base_input_folder = '/Users/thomas/FTP/TCHIBO/SSTA KOMPLET'
base_processed_folder = '/Users/thomas/Nordisk Company A S/Nordisk Company A S Team Site - BC/Tchibo/Processed SSTA'
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
