from asset import Asset
link = 'https://next.backpack.tf/stats?item=Mann%20Co.%20Supply%20Crate%20Key&quality=Unique'
a = Asset(link)
a.update()
a.opportunity()