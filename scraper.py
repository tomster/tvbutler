mapper = {
    'show title' : 'title',
    'show name' : 'name',
    'season' : 'season',
    'episode' : 'episode',
    'filename' : 'filename',
}

def extract_metadata(description):
    data = dict()
    for item in description.split(';'):
        try:
            key, value = item.split(':')
        except ValueError:
            continue
        data[mapper[key.strip().lower()]] = value.strip()

    if '720p' in data['title'] + data['filename']:
        data['quality'] = u'720p'
    else:
        data['quality'] = u'sd'
    return data
