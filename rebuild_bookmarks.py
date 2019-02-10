import sqlite3
from datetime import datetime
from urlparse import urlparse

"""
Will skip URLs where the tld and the title are the same as a history item that has already come through. 
"""

print ('creating bookmarks...')

conn = sqlite3.connect("/Users/djk/Library/Safari/History.db")

file = open("bookmarks.html", "w")


file.write('<html><head><style>\r\n')

file.write('body { background-color: #2F4858; font-family: "Helvetica Neue";  }\r\n')
file.write('a { font-size:16px; text-decoration: none; }\r\n')
file.write('.sub_link { color: #333333; font-size:11px; }\r\n')
file.write('.link { color: #333333; }\r\n')
file.write('.link_wrapper { display:block; float:left; width:250px; height:50px; padding:8px; border:solid #000000 1px; overflow:hidden; margin:2px; background-color:#96d2f2;  box-shadow: 4px 4px 4px #000000; border-radius: 4px; }\r\n')
file.write('.tld.link { font-weight: bold; }\r\n')
file.write('.tld { background: #ffffff; }\r\n')
file.write('.tld.link_wrapper { background: #ffffff; }\r\n')
file.write('.frag { background: #6CA9D8; }\r\n')
file.write('.amazon.link_wrapper { background: #F6AE2D }\r\n')
file.write('.amazon.frag, .amazon.tld { background: #F6AE2D; }\r\n')
file.write('.amazon { color: black; }\r\n')
file.write('div.fav { float: left; margin:4px 8px 32px 0; }\r\n')
file.write('div.fav img { width:16px; height:16px; }\r\n')
file.write('h2 { color:white; font-family: "Helvetica Neue"; margin:12px 0 0 0; font-size:16px;}')
file.write('.note { color:white; font-size:10px; margin:2px 0px 4px 0px; }')
file.write('.section_header { color:white; font-size:8px; width=900px; padding:2dpx; display:block; clear:both; text-align:right; margin-right:32px;  }')
file.write('.column { width:560px; float:left; padding-bottom:12px;}')

file.write('</style></head><body>')
file.write('<div style="width:1120px; margin:0 auto;">')
file.write('<h2>darryl kanouse / djk / ' + str(datetime.now()) + '</h2>')
file.write('<div class="note">To rebuild bookmarks run: /Users/djk/repos/safari_history/rebuild_bookmarks.py</div>')

written = []

def write_bookmarks(file, cursor, written, limit, tldonly ):
    file.write('<div class="column">')

    i = 0
    for row in cursor:
        url = str(row[1])
        if url.startswith("file:///"): continue
        if url.startswith("about:"): continue
        parsed = urlparse(url)

        style_class = ''
        try:
            if not row[2]:
            	continue
                # style_class += 'notitle '   # NO TITLE! make is small
                # title = url
            else:
                title = row[2]
            long_title = str(parsed.netloc) + '|' + str(title)
        except:
        	# continue
            style_class += 'notitle '
            long_title = parsed.netloc

        # check if indistinguishable version came through already
        if long_title in written:
            print ('skipping: ' + long_title)
            continue

        # check if url came through already
        if url in written: continue

        if url.endswith(parsed.netloc + '/'):
            style_class += 'tld '           # make it bold! because this is a top level domain
        elif tldonly: continue

        if 'amazon' in str(parsed.netloc):
            style_class += 'amazon '        # AMAZON! make it colorful
        if parsed.fragment != '':
            style_class += 'frag '          # FRAGMENT- this has a # so make it small

        i += 1
        if i > limit: break

        file.write('<a href="' + url + '" class="' + style_class + 'link_wrapper">')
        file.write('<div class="fav"><img src="' + parsed.scheme + '://' + parsed.netloc + '/favicon.ico" ')
        file.write('onerror="this.onerror=null; this.src=\'https://www.google.com/s2/favicons?domain=' + parsed.netloc + '\'" /></div>')

        link = '<div class="' + style_class + 'link">' + str(parsed.netloc).replace("www.", "") + '</div>'
        sub_link = '<div class="' + style_class + 'sub_link">' + title + '</div>'

        file.write(link.encode('utf8') + "\r\n")
        file.write(sub_link.encode('utf8') + "\r\n")
        file.write('</a>')

        written.append(url) # write the url version
        written.append(long_title) # write the long string version

    file.write('</div>')


cursor = conn.execute("""
  select count(*) as count, h.url, v.title from history_visits v 
    inner join history_items h on h.id = v.history_item
  where datetime(v.visit_time + 978307200, 'unixepoch', 'localtime') > datetime('now', '-90 day')
    and h.url not like '%amazon.com%'
    and h.url not like '%docs.google.com%'
  group by h.url, v.title
  order by count desc
  limit 200
  """)

# file.write('<div class="section_header">- 45 days -</div>')
write_bookmarks(file, cursor, written, 48, False)


cursor = conn.execute("""
  select count(*) as count, h.url, v.title from history_visits v 
    inner join history_items h on h.id = v.history_item
  where datetime(v.visit_time + 978307200, 'unixepoch', 'localtime') > datetime('now', '-45 day')
    and h.url like '%docs.google.com%'
  group by h.url, v.title
  order by count desc
  limit 200
  """)

# file.write('<div class="section_header">- 45 days -</div>')
write_bookmarks(file, cursor, written, 10, False)


cursor = conn.execute("""
  select count(*) as count, h.url, v.title from history_visits v 
    inner join history_items h on h.id = v.history_item
  where datetime(v.visit_time + 978307200, 'unixepoch', 'localtime') > datetime('now', '-14 day')
    and h.url not like '%amazon.com%'
    and h.url not like '%docs.google.com%'
  group by h.url, v.title
  order by count desc
  limit 120
  """)

# file.write('<div class="section_header">- 14 days -</div>')
write_bookmarks(file, cursor, written, 10, False)


cursor = conn.execute("""
  select count(*) as count, h.url, v.title from history_visits v 
    inner join history_items h on h.id = v.history_item
  where datetime(v.visit_time + 978307200, 'unixepoch', 'localtime') > datetime('now', '-45 day')
    and h.url like '%amazon.com%'
  group by h.url, v.title
  order by count desc
  limit 200
  """)

# file.write('<div class="section_header">- 45 days -</div>')
write_bookmarks(file, cursor, written, 40, False)



file.write('</div></body></html>')

print ('done')