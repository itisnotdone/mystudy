urls = 'to_record.urls'
with open(urls) as f:
    content = f.readlines()
content = [x.strip() for x in content]

print content
