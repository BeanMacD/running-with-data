class DisneySpider(BaseSpider):
    name = "DisneySpider"
    allowedr_domains=["https://www.trackshackresults.com"]

    def start_requests(self):
        Alphabet =['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        Years = [13, 14, 15,16, 17]
        for year in Years:
            i=0
            while i<len(Alphabet):
                Letter = Alphabet[i]
                yield Request("https://www.trackshackresults.com/disneysports/results/wdw/wdw%d/mar_results.php?Link=43&Type=2&Div=%s&Ind=%d" %(year, Letter, i), callback=self.parse)
                i+=1
    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        rows = hxs.xpath('//table[@class="info_table"]//tr')
        for row in rows:
            item = DisneyItem()
            	item['ID'] = row.xpath('./td[1]/text()').extract()
    			item['name'] = row.xpath('./td[2]/text()').extract()
    			item['Bib'] = row.xpath('./td[3]/text()').extract()
    			item['Age'] = row.xpath('./td[4]/text()').extract()
    			item['Place'] = row.xpath('./td[5]/text()').extract()
    			item['GenderPlace'] = row.xpath('./td[6]/text()').extract()
    			item['Five_Mile_Split'] = row.xpath('./td[7]/text()').extract()
    			item['Ten_Mile_Split'] = row.xpath('./td[8]/text()').extract()
    			item['Half_Split'] = row.xpath('./td[9]/text()').extract()
    			item['Twenty_Mile_Split'] = row.xpath('./td[10]/text()').extract()
    			item['Clock_Time'] = row.xpath('./td[11]/text()').extract()
    			item['Net_Time'] = row.xpath('./td[12]/text()').extract()
    			item['Hometown'] = row.xpath('./td[13]/text()').extract()
    			yield item
