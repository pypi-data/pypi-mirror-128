import requests
import lxml.html as lh
import json

def getHtmlResponse(tingkatan,tahun_ajaran,id_tabel='1'):
	content = requests.get('http://statistik.data.kemdikbud.go.id/index.php/statistik/tableLoad/'+tingkatan+'/'+tahun_ajaran+'/000000/0/'+id_tabel)
	doc = lh.fromstring(content.text.replace('\r\n\t\t\t','').replace('\r\n\t\t',''))
	return doc
