import aiohttp


async def get_characteristics(characteristics):
    result = {}
    for char in characteristics:
        result[char['name']] = char['value']

    return result


async def parse_wb(sku: str) -> dict | None:
    part = sku[:-3]
    vol = part[:-2]
    async with aiohttp.ClientSession() as session:
        for basket in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16',
                       '17', '18', '19', '20']:
            url = f'https://basket-{basket}.wb.ru/vol{vol}/part{part}/{sku}/info/ru/card.json'
            response = await session.get(url=url)
            if response.ok:
                data = await response.json()
                title = data.get('imt_name')
                description = data.get('description')
                characteristics = await get_characteristics(data.get('options'))

                return {
                    'title': title,
                    'description': description,
                    'characteristics': characteristics
                }
        return
