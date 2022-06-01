from asset import Asset
key = 'https://next.backpack.tf/stats?item=Mann%20Co.%20Supply%20Crate%20Key&quality=Unique'
tod = 'https://next.backpack.tf/stats?item=Tour%20of%20Duty%20Ticket&quality=Unique'
a = Asset(key)
a.update()
a.opportunity()