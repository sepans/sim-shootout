
import os
import sys
import gensim
import sqlite3

if __name__ == '__main__':
	basedir = sys.argv[1]
	print("basedir %s" % basedir)

	createTable = 0
	insertTable = 0


	conn = sqlite3.connect('annoy.db')
	c = conn.cursor()
	
	if createTable:
		c.execute("DROP TABLE annoy_map")
		c.execute('''CREATE TABLE annoy_map
	              (annoy_id integer, title text, wiki_id integer)''')

	
	if insertTable:
		id2title = gensim.utils.unpickle(os.path.join(basedir, 'id2title'))
		print('number of articles in index %s' %len(id2title))
		print("loading wikiids")
		wikiidlist = gensim.utils.unpickle(os.path.join(basedir, 'wikiidlist'))
		#wikiIdToIndexId = collections.OrderedDict((int(wikiid), pos) for pos, wikiid in enumerate(wikiidlist))
		#title2id = dict((gensim.utils.to_unicode(title).lower(), pos) for pos, title in enumerate(id2title))
		print('number of articles in wikiidlist %s' %len(wikiidlist))

		id2titleAndWiki = zip(id2title, wikiidlist)
		for i, (title, wikiid) in enumerate(id2titleAndWiki):
			values = (i, gensim.utils.to_unicode(title).lower(), wikiid)
			c.execute("INSERT INTO annoy_map VALUES (?, ?, ?)", values)
		print('creating indices')
		c.execute("CREATE UNIQUE INDEX annoy_index on annoy_map (annoy_id)")
		c.execute("CREATE INDEX title_index on annoy_map (title)")
		c.execute("CREATE UNIQUE INDEX wiki_index on annoy_map (wiki_id)")

	conn.commit()

	title = ('anarchism', )
	c.execute('SELECT * FROM annoy_map WHERE title = ?', title)
	print(c.fetchall())

	ids = [1,2,10, 15, 1000]
	c.execute('SELECT title FROM annoy_map WHERE annoy_id in (%s)' % ','.join('?'*len(ids)), ids)
	print(c.fetchall())

	conn.close()

