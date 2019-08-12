from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from Marathons.items import DublinItem
from scrapy.http import Request


id = 1
class DublinSpider(BaseSpider):
    name = "DublinSpider"
    allowed_domains = ["http://results.dublinmarathon.ie"]

    def start_requests(self):
        racesid = [82, 78, 66, 54, 48, 41, 31, 26, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        MaxPages = [1589, 1677, 1294, 1230, 1236, 1169, 1078, 1048, 938, 846, 819, 795, 852, 627, 650, 616, 717]
        for index, race in enumerate(racesid):
            temp = MaxPages[index]
            MaxPage = (temp-1)*10
            i=0
            while(i<MaxPage):
                yield Request("http://results.dublinmarathon.ie/results.php?search&race=%d&sort=placeall&from=%d" %(race, i), callback = self.parse)
                i+=10

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        temp = hxs.xpath('//*[@id="content"]/p').extract_first()
        temp = temp[3:]
        Year = temp[:4]
        rows = hxs.xpath('//table[@class="results_table"]//tr')
        global id
        for row in rows:
            item = DublinItem()
            Name = row.xpath('./td[2]/text()[1]').extract_first()
            Name = str(Name)
            if "None" not in Name:
                Name = Name.replace('|', '')
                item['Age'] = 'n/a'
                item['OverallPlace'] = row.xpath('./td[1]/text()').extract_first()
                item['Hometown'] = row.xpath('./td[3]/text()').extract_first()
                item['Category'] = row.xpath('./td[4]/text()').extract_first()
                item['CategoryPlace'] = row.xpath('./td[5]/text()').extract_first()
                item['Ten_Kilometer_Split'] = row.xpath('./td[6]/text()').extract_first()
                item['Half_Split'] = row.xpath('./td[7]/text()').extract_first()
                item['Thirty_Kilometer_Split'] = row.xpath('./td[8]/text()').extract_first()
                item['Clock_Time'] = row.xpath('./td[9]/text()').extract_first()
                item['Net_Time'] = row.xpath('./td[10]/text()').extract_first()
                Gender = row.xpath('./td[4]/text()').extract_first()
                Gender = str(Gender)
                item['AgeCategory'] = Gender[1:]
                item['Gender'] = Gender[:1]
                item['GenderPlace'] = 'n/a'
                item['Name'] = Name.split()
                item['RunnerID'] = id
                id+=1
                item['RaceID'] = 'Dublin'+Year
                yield item
