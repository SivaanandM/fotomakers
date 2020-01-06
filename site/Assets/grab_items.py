from lxml import html, etree
import requests
import urllib.request
import re
import sys
import csv

dir = sys.argv[1] #"/Users/sivaamur/fotomakers.co.in/Assets/CCTV_Camera/HIKVISION/" 
headurl = sys.argv[2] #'http://www.cctvcameradealerschennai.com/product/CCTV-CAMERA/HIKVISION/HIKVISION-dealers-in-chennai.php' 
page = requests.get(headurl)
tree = html.fromstring(page.content)

product_branchs = tree.xpath("//div[@class='row']//div[contains(@class,'col-sm-4')]")
heading= ['ITEM_NO', 'HREF', 'TITLE', 'IMG_SRC', 'IMG_ALT', 'MODEL', 'PRODUCT_DESCRIPTION']
with open(dir+"/"+'product.csv', 'a') as csvfile:
    filewriter = csv.writer(csvfile)
    # filewriter = csv.writer(csvfile, delimiter=',',
    #                         quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(heading)
    for i, branch in enumerate(product_branchs):
        try:
            if i < len(product_branchs) - 3:
                print("Item No : ", i)
                # print(etree.tostring(branch, pretty_print=True))
                print("HREF -", branch.getchildren()[0].attrib['href'])
                print("TITLE - ", branch.getchildren()[0].attrib['title'])
                print("IMG SRC - ",branch.getchildren()[0][0].attrib['src'])
                
                urllib.request.urlretrieve(branch.getchildren()[0][0].attrib['src'])
                print("IMG ALT - ",branch.getchildren()[0][0].attrib['alt'])
                print("MODEL - ",branch.getchildren()[1][0].text)
                urllib.request.urlretrieve(branch.getchildren()[0][0].attrib['src'],dir+"/"+branch.getchildren()[0][0].attrib['src'].split('/')[-1])
                p_des=""
                description_page = requests.get(branch.getchildren()[0].attrib['href'])
                description_tree = html.fromstring(description_page.content)
                descriptions = description_tree.xpath("//div[@class='col-sm-4 '][3]//*")
                for it, des in enumerate(descriptions):
                    try:
                        if des.tag == "h2":
                            s = str(etree.tostring(des, pretty_print=True))
                            h2 = re.search('<h2>(.*)</h2>',s)
                            p_des = p_des +"@"+ h2.group(1)
                            point = re.search('#8226;(.*)',s)
                            p_des = p_des +"@"+ point.group(1)
                        if des.tag == "br":
                            s = str(etree.tostring(des, pretty_print=True))
                            if "#8226;" in s:
                                p_des = p_des +"@"+ s
                    except Exception as e:
                        print(str(e))
                print("PRODUCT DESCRIPTION - ",p_des)
                print("-----#######----------#######----------#######----------#######----------#######-----")
                filewriter.writerow([str(i), branch.getchildren()[0].attrib['href'], branch.getchildren()[0].attrib['title'],
                                    branch.getchildren()[0][0].attrib['src'], branch.getchildren()[0][0].attrib['alt'],branch.getchildren()[1][0].text
                                    ,p_des.replace(",", "~") ])
        except:
            print("issue in item no:",i)
csvfile.close()

    