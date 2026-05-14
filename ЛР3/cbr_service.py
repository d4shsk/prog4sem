import httpx
import xml.etree.ElementTree as ET
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Currency

CBR_URL = "https://www.cbr.ru/scripts/XML_daily.asp"

async def fetch_and_update_currencies(session: AsyncSession):
    async with httpx.AsyncClient() as client:
        response = await client.get(CBR_URL)
        response.raise_for_status()

        root = ET.fromstring(response.content)

        for valute in root.findall('Valute'):
            code = valute.find('CharCode').text
            name = valute.find('Name').text

            vunit_rate_node = valute.find('VunitRate')
            if vunit_rate_node is not None:
                rate_str = vunit_rate_node.text.replace(',', '.')
                rate = float(rate_str)
            else:
                value_str = valute.find('Value').text.replace(',', '.')
                nominal_str = valute.find('Nominal').text
                rate = float(value_str) / float(nominal_str)

            stmt = select(Currency).where(Currency.code == code)
            result = await session.execute(stmt)
            currency = result.scalar_one_or_none()

            if currency:
                currency.name = name
                currency.rate = rate
            else:
                currency = Currency(code=code, name=name, rate=rate)
                session.add(currency)

        await session.commit()
