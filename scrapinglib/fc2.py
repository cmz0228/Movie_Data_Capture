# -*- coding: utf-8 -*-

import re
from lxml import etree
from urllib.parse import urljoin

from .parser import Parser


class Fc2(Parser):
    source = 'fc2'
    imagecut = 0

    expr_title = '/html/head/title/text()'
    expr_studio = '//*[@id="top"]/div[1]/section[1]/div/section/div[2]/ul/li[3]/a/text()'
    expr_release = '//*[@id="top"]/div[1]/section[1]/div/section/div[2]/div[2]/p/text()'
    expr_runtime = "//p[@class='items_article_info']/text()"
    expr_director = '//*[@id="top"]/div[1]/section[1]/div/section/div[2]/ul/li[3]/a/text()'
    expr_actor = '//*[@id="top"]/div[1]/section[1]/div/section/div[2]/ul/li[3]/a/text()'
    expr_cover = "//div[@class='items_article_MainitemThumb']/span/img/@src"
    expr_tags = "//a[@class='tag tagTag']/text()"

    def search(self, number):
        self.number = number.replace('FC2-', '').replace('fc2-', '')
        self.detailurl = 'https://adult.contents.fc2.com/article/' + self.number + '/'
        self.htmlcode = self.getHtml(self.detailurl)
        if self.htmlcode == 404:
            return 404
        htmltree = etree.HTML(self.htmlcode)
        result = self.dictformat(htmltree)
        return result

    def getNum(self, htmltree):
        return 'FC2-' + self.number

    def getRelease(self, htmltree):
        return super().getRelease(htmltree).strip(" ['販売日 : ']").replace('/','-')
    
    def getActors(self, htmltree):
        actors = super().getActors(htmltree)
        if not actors:
            actors = '素人'
        return actors

    def getCover(self, htmltree):
        return urljoin('https://adult.contents.fc2.com', super().getCover(htmltree)) 

    def getExtrafanart(self, htmltree):
        html_pather = re.compile(r'<ul class=\"items_article_SampleImagesArea\"[\s\S]*?</ul>')
        html = html_pather.search(self.htmlcode)
        if html:
            html = html.group()
            extrafanart_pather = re.compile(r'<a href=\"(.*?)\"')
            extrafanart_imgs = extrafanart_pather.findall(html)
            if extrafanart_imgs:
                return extrafanart_imgs
        return ''

    def getTrailer(self, htmltree):
        video_pather = re.compile(r'\'[a-zA-Z0-9]{32}\'')
        video = video_pather.findall(self.htmlcode)
        if video:
            try:
                video_url = video[0].replace('\'', '')
                video_url = 'https://adult.contents.fc2.com/api/v2/videos/' + self.number + '/sample?key=' + video_url
                url_json = eval(self.getHtml(video_url))['path'].replace('\\', '')
                return url_json
            except:
                return ''
        else:
            return ''