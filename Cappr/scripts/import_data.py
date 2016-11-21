import csv

from Cappr.models import Cap


def run():
    index = {}

    _type = 'snapback'
    _audience = 'mens'
    with open('Cappr/scripts/data/mens-snapback.csv', 'r') as cf:
        rows = csv.reader(cf)
        c = next(rows)

        # Storing indices as it differs for some files.
        for k in c:
            index[k] = c.index(k)

        for row in rows:

            cap = Cap.objects.filter(SKU=row[index['SKU']]).first()

            if cap is None:
                cap = Cap.objects.create(name=row[index['name']],
                                         SKU=row[index['SKU']],
                                         type=_type,
                                         audience=_audience,
                                         url=row[index['url']],
                                         price=row[index['price']],
                                         detail=row[index['detail']],
                                         team=row[index['team']])

            cap.save()
