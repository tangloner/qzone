# -*-coding:utf-8-*- 
######################################
########copyright tangloner###########
######################################
import urllib
import urllib2
import re
from HTMLParser import HTMLParser

def analysis_blogList(text):
    blogList=[]
    iterator=[]
    blogListPattern=re.compile(r'href="(http://qz.qq.com/447948133/blog\?uin=447948133&vin=0&blogid=\d+)">\s+([\w*\s*]*[\x80-\xff]*)')
    iterator=blogListPattern.finditer(text)
    for match in iterator:
        blogList.append((match.group(1),match.group(2)))
    return blogList
def analysis_qzsection(text):
    sectionList=[]
    sectionListPattern=re.compile(r'http://qz.qq.com/447948133/[a-z]*list/')
    sectionList=sectionListPattern.findall(text)
    return sectionList
def extract_next_url(text):
    next_url=''
    next_page_pattern=re.compile(r'href="(.*?)" title="下一页"')
    next_page=next_page_pattern.search(text)
    if next_page:
        next_url=next_page.group(1)
    else:
        print "this is the end page! no next"
        next_url=None
    return next_url
class QZONE:
    @staticmethod
    def DownloadBlog(qq,filename=None):
        blogurl='http://qz.qq.com/%s/bloglist?page=0'%qq
        print 'start at url:',blogurl,'0'
        QZONE.__Download(blogurl,filename)
        print 'Download completed!'
    @staticmethod
    def __Download(starturl,filename):
        blog_url=[]
  section_list=[]
	next_pageurl=''
	url=starturl
	count=0
        cookieFile=urllib2.HTTPCookieProcessor()
        opener=urllib2.build_opener(cookieFile)
        if not filename:
            filename='blog.txt'
        file=open(filename,'w+')
        while True:
            req=urllib2.Request(url)
            result=opener.open(req)
            text=result.read()
            blog_url=analysis_blogList(text)
            #print blog_url
            section_list=analysis_qzsection(text)
            nextpageurl=extract_next_url(text)
            next_pageurl=nextpageurl
            blogContentPattern=re.compile(r'<div class="entry_content">(.*?)</div>', re.S)   
            for url,title in blog_url:
                print 'Downloading',url
                req=urllib2.Request(url)
                result=opener.open(req)
                file.write('\n'+title+'\n')
                ret=blogContentPattern.search(result.read())
                if ret:
                    file.write(ret.group(1).replace('<p>','\n'))
            if next_pageurl:
                url=next_pageurl
                count+=1
                print 'start at url:',url,count
            else:
                break
        file.close()
if __name__=='__main__':
    QZONE.DownloadBlog('447948133','447948133.txt')
