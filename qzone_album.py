# -*-coding:utf-8-*- 
######################################
########copyright tangloner###########
######################################

import urllib
import urllib2
import re
import time
import os
from HTMLParser import HTMLParser

def load_mainpage(page_url):
    cookieFile=urllib2.HTTPCookieProcessor()
    opener=urllib2.build_opener(cookieFile)
    mainpage_req=urllib2.Request(page_url)
    mainpage=opener.open(mainpage_req)
    page_text=mainpage.read()
    server_busy_pattern=re.compile(r'<li class="blank"><img alt="" src="http://edu.qzs.qq.com/qzonestyle/qzone_mobile_v1/img/blank.png">对不起,网络繁忙,请稍后再试</li>')
    server_busy=server_busy_pattern.search(page_text)
    if server_busy:
        return None
    else:
        return page_text
    
def extract_album_list(text):
    albumlist=[]
    #album_url_Pattern=re.compile(r'<a title="(\s*[\d*\.*]*[\x80-\xff]*.*[\d*\.*]*\s*)" href="(http://qz.qq.com/275636551/photolist\?aid=V14PxmvK1gKwpn)">')
    album_url_Pattern=re.compile(r'<a title="(\s*[\d*\.*]*[\x80-\xff]*.*[\d*\.*]*\s*)" href="(.*?)"><img')
    iterator=album_url_Pattern.finditer(text)
    for match in iterator:
        albumlist.append((match.group(1),match.group(2)))
    return albumlist

def extract_image_url(text):
    image_url=[]
    image_url_Pattern=re.compile(r'style="max-width:100px; max-height:100px;" src="(.*?)"')
    #image_url_Pattern=re.compile(r'<a title="\w*\s*" href="(.*?)">')
    image_url=image_url_Pattern.findall(text)
    return image_url

def extract_next_page_url(text):
    next_pageurl_Pattern=re.compile(r'<a href="(.*?)" title="下一页" class="bt_next"><span>下一页</span></a>')
    next_pageurl=next_pageurl_Pattern.search(text)
    if next_pageurl:
        next_pageurl=next_pageurl.group(1)
        print next_pageurl
        return next_pageurl
    else:
        print "this album going ending!"
        next_pageurl=None
        return next_pageurl

    
class QZONE:
    @staticmethod
    def DownloadAlbum(qq,DstDir):
        albumlist="http://qz.qq.com/%s/albumlist?page=0"%qq
        static_albumpage="%s.html"%qq
        DstDir=DstDir+str(qq)+'\\'
        os.mkdir(DstDir)
        print "start load album in %s QQ zone."%qq," and store on %s"%DstDir
        QZONE.__Download_album(qq,albumlist,static_albumpage,DstDir)
        print "Download Completed!"
    @staticmethod
    def __Download_album(qq,albumlist,static_albumpage,DstDir):
        auto_loadpage=load_mainpage(albumlist)
        if auto_loadpage:
            loadpage=auto_loadpage
        else:
            print "Please load", qq," by your hand and named %s.html"%qq
            f=open(static_albumpage)
            loadpage=f.read()
            #print loadpage
            f.close()
        albumlist=extract_album_list(loadpage)
        #print albumlist
        album_order=1
        for title,url in albumlist:
            starturl=url
            cnt=0
            print 'downloading ', title ,'start from ',starturl
            StoreDir=DstDir+str(title)+'\\'
            os.mkdir(StoreDir)
            print album_order
            while True:
                image_text=urllib2.urlopen(starturl).read()
                imagelist=extract_image_url(image_text)
                next_page_url=extract_next_page_url(image_text)
                count=1
                for image_url in imagelist:
                    print image_url
                    image_url=image_url.replace('http://a','http://b')
                    image_url=image_url.replace('/a/','/b/')
                    print image_url
                    path=StoreDir+str(cnt*12+count)+'.jpg'
                    print path
                    #time.sleep(10)
                    data=urllib.urlopen(image_url).read()
                    f=file(path,'wb')
                    f.write(data)
                    f.close()
                    count+=1
                if next_page_url:
                    starturl=next_page_url
                    cnt+=1
                else:
                    break
if __name__=='__main__':
    QZONE.DownloadAlbum('447948133','E:\\Code\\python_code\\qzone\\')







        
            
