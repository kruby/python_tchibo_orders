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
