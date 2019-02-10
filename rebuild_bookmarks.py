import sqlite3
from datetime import datetime
from urllib.parse import urlparse

print ('creating bookmarks...')

# History is stored as a sqllite database.
# Fun fact, a linked iOS device will update this history as well.
HISTORY_LOCATION = "/Users/djk/Library/Safari/History.db"

# Open a connection to the safari history database
conn = sqlite3.connect(HISTORY_LOCATION)

# Get the HTML template for our home page.
with open("template.html", "r") as file:
  template_html = file.read()

# The document title
body = """
  <div style="width:1120px; margin:0 auto;">
  <h2>darryl kanouse / djk / {0} </h2>
  <div class="note">To rebuild bookmarks run: <code>rebuild_bookmarks.py</code></div>
""".format(str(datetime.now()))

# Will skip URLs where the tld and the title are the same as a history item that has already come through. 
written = []

def write_bookmarks(body, cursor, written, limit, tldonly ):
    """This is the main function that writes the bookmark HTML
    """
    body += '<div class="column">'

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

        body += '<a href="' + url + '" class="' + style_class + 'link_wrapper">'
        body += '<div class="fav"><img src="' + parsed.scheme + '://' + parsed.netloc + '/favicon.ico" '
        body += 'onerror="this.onerror=null; this.src=\'https://www.google.com/s2/favicons?domain=' + parsed.netloc + '\'" /></div>'


        link = '<div class="' + style_class + 'link">' + str(parsed.netloc).replace("www.", "") + '</div>'
        sub_link = '<div class="' + style_class + 'sub_link">' + title + '</div>'

        # body += str(link.encode('utf8')) + "\r\n"
        # body += str(sub_link.encode('utf8')) + "\r\n"
        body += link + "\r\n"
        body += sub_link + "\r\n"
        body += '</a>'

        written.append(url) # write the url version
        written.append(long_title) # write the long string version

    body += '</div>'
    return body

# Get the main links that are not amazon and not google.
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
body = write_bookmarks(body, cursor, written, 48, False)

cursor = conn.execute("""
  select count(*) as count, h.url, v.title from history_visits v 
    inner join history_items h on h.id = v.history_item
  where datetime(v.visit_time + 978307200, 'unixepoch', 'localtime') > datetime('now', '-14 day')
    and ((h.url not like '%amazon.com%') or (h.url like '%www.amazon.com%'))
    and h.url not like '%docs.google.com%'
  group by h.url, v.title
  order by count desc
  limit 120
  """)
body += "<h2 class='section-header'>latest (past 14 days)</h2>"
body = write_bookmarks(body, cursor, written, 10, False)

cursor = conn.execute("""
  select count(*) as count, h.url, v.title from history_visits v 
    inner join history_items h on h.id = v.history_item
  where datetime(v.visit_time + 978307200, 'unixepoch', 'localtime') > datetime('now', '-45 day')
    and h.url like '%docs.google.com%'
  group by h.url, v.title
  order by count desc
  limit 200
  """)
body += "<h2 class='section-header'>google.com (past 45 days)</h2>"
body = write_bookmarks(body, cursor, written, 10, False)

cursor = conn.execute("""
  select count(*) as count, h.url, v.title from history_visits v 
    inner join history_items h on h.id = v.history_item
  where datetime(v.visit_time + 978307200, 'unixepoch', 'localtime') > datetime('now', '-45 day')
    and h.url like '%amazon.com%'
    and h.url not like '%www.amazon.com%'
  group by h.url, v.title
  order by count desc
  limit 200
  """)
body += "<h2 class='section-header'>amazon.com (past 45 days)</h2>"
body = write_bookmarks(body, cursor, written, 24, False)

file = open('homepage.html', 'w')
file.write(template_html.replace('{% body %}', body))

print ('done')