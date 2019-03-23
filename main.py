import requests, bs4, re

url = "http://www.issatso.rnu.tn/fo/emplois/emploi_groupe.php"
cookieName = 'PHPSESSID'
reg = re.compile("<center>(.*\S.*)</center>")
def getRequest(link):
	print('[i] Getting request link:')
	print (link)
	res = requests.get(link)
	try:
		res.raise_for_status()
	except:
		print('[-] Request failed')
		sys.exit(0)
	print('[+] Request succeeded')
	return res

def parseHtml(req):
    parsedHtml = bs4.BeautifulSoup(req.text,"html.parser")
    print('[+] Html parsing succeeded')
    return parsedHtml

def getOptions(parsedHtml):
    selectItem = parsedHtml.select('select')
    vals = [(op.text,op.get('value')) for op in selectItem[0].children if not isinstance(op,bs4.NavigableString)]
    #for val,name in vals:
    #    print(name + " " + val)
    return vals

def postRequest(ide,token,cookie):
    d={}
    d["jeton"] = token
    d["id"] = ide
    headers = {'Cookie': cookieName+"="+cookie}

    r = requests.post(url,headers=headers,data=d)
    return r

def getToken(parsedHtml):
    inputs = parsedHtml.select('input')
    token = [inp for inp in inputs if inp.get('name')=='jeton']
    return token[0].get('value')

def dumpRequestToFile(r,fileName):
    dumpToFile(r.content,fileName)

def dumpToFile(d,fileName):
    with open(fileName, mode='wb') as localfile:
        localfile.write(d)

def main():
	req = getRequest(url)

	print(req)
	print('[i] Type: '+str(type(req)))
	print('[i] File size: '+str(len(req.text)))
	parsedHtml = parseHtml(req)
	vals = getOptions(parsedHtml)
	cookie , token = req.cookies[cookieName] ,getToken(parsedHtml)
	print(cookie + ' ' + token)
	res = postRequest(vals[0],token,cookie)
	parsedRes= parseHtml(res)
	tableDiv = next(div.select('table') for div in parsedRes.select('div') \
                        if div.get('id')=='dvContainer')[0]
						#print(tableDiv.encode("utf-8"))
	table = tableDiv.select('tbody')[0]

if __name__=="__main__":
    main()
