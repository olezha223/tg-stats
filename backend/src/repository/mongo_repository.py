from .interface import RepositoryInterface
from ..database import AsyncMongoDB
from ..models.request_models import WhoTextedMore, WhoIgnoredMore, MeanIntervals
import datetime
from collections import defaultdict

def prepare_dict(dct: dict) -> dict:
    result = dict()
    for key, value in dct.items():
        result[key.strftime("%Y-%m-%d")] = value
    return result


class MongoRepository(RepositoryInterface):
    """Работа с MongoDB"""

    async def add_chat(self, session: AsyncMongoDB, data: dict, user: str, name: str):
        return (await session.users[user][name].insert_one(data)).inserted_id

    async def delete_chat(self, session: AsyncMongoDB, user: str, name: str):
        await session.users[user][name].drop()

    async def update_chat(self, session: AsyncMongoDB, new_data: dict, user: str, name: str):
        await self.delete_chat(session, user, name)
        await self.add_chat(session, new_data, user, name)

    async def get_who_texted_more(self, session: AsyncMongoDB, dto: WhoTextedMore) -> tuple[dict, dict]:
        data = (await session.users[dto.user][dto.name].find().to_list())[0]
        messages = data['messages']
        first_day = datetime.datetime.strptime(messages[0]['date'], "%Y-%m-%dT%H:%M:%S")
        first_day = first_day.replace(hour=2, minute=0, second=0, microsecond=0)
        period_counts_1 = defaultdict(int)
        period_counts_2 = defaultdict(int)
        for msg in messages:
            last_day = first_day + datetime.timedelta(dto.interval.value)
            date = datetime.datetime.strptime(msg["date"], "%Y-%m-%dT%H:%M:%S")
            if period_counts_1[first_day] == 0:
                period_counts_1[first_day] = 0
            if period_counts_2[first_day] == 0:
                period_counts_2[first_day] = 0
            if first_day <= date <= last_day:
                if msg.get('from') != dto.name:
                    period_counts_1[first_day] += 1
                else:
                    period_counts_2[first_day] += 1
            else:
                first_day = last_day

        return prepare_dict(period_counts_1), prepare_dict(period_counts_2)

    async def get_who_ignored_more(self, session: AsyncMongoDB, dto: WhoIgnoredMore) -> tuple[dict, dict]:
        data = (await session.users[dto.user][dto.name].find().to_list())[0]
        messages = data['messages']
        period_counts_1 = defaultdict(int)
        period_counts_2 = defaultdict(int)
        first_day = datetime.datetime.strptime(messages[0]['date'], "%Y-%m-%dT%H:%M:%S")
        first_day = first_day.replace(hour=2, minute=0, second=0, microsecond=0)
        for i in range(1, len(data['messages'])):
            msg = data['messages'][i]
            last_day = first_day + datetime.timedelta(dto.interval.value)
            date = datetime.datetime.strptime(msg["date"], "%Y-%m-%dT%H:%M:%S")
            if period_counts_1[first_day] == 0:
                period_counts_1[first_day] = 0
            if period_counts_2[first_day] == 0:
                period_counts_2[first_day] = 0
            if first_day <= date <= last_day:
                if data['messages'][i - 1]['from'] != data['messages'][i]['from']:
                    date_prev = datetime.datetime.strptime(data['messages'][i - 1]['date'], "%Y-%m-%dT%H:%M:%S")
                    if (date - date_prev).total_seconds() / 60 >= dto.min_ignore_minutes:
                        if data['messages'][i]['from'] == dto.name:
                            period_counts_2[first_day] += 1
                        else:
                            period_counts_1[first_day] += 1
            else:
                first_day = last_day
        return prepare_dict(period_counts_1), prepare_dict(period_counts_2)

    async def get_intervals(self, session: AsyncMongoDB, dto: MeanIntervals) -> tuple[dict, dict]:
        data = (await session.users[dto.user][dto.name].find().to_list())[0]
        messages = data['messages']
        first_day = datetime.datetime.strptime(messages[0]['date'], "%Y-%m-%dT%H:%M:%S")
        first_day = first_day.replace(hour=2, minute=0, second=0, microsecond=0)
        period_counts_1 = defaultdict(list)
        period_counts_2 = defaultdict(list)
        last_msg_date_1 = first_day
        last_msg_date_2 = first_day
        for msg in messages:
            last_day = first_day + datetime.timedelta(dto.interval.value)
            date = datetime.datetime.strptime(msg["date"], "%Y-%m-%dT%H:%M:%S")
            if first_day <= date <= last_day:
                if msg.get('from') != dto.name and not period_counts_1[first_day]:
                    period_counts_1[first_day] = [0, 0]
                elif msg.get('from') == dto.name and not period_counts_2[first_day]:
                    period_counts_2[first_day] = [0, 0]
                if msg.get('from') != dto.name:
                    delta = (date - last_msg_date_1).total_seconds() // 3600
                    period_counts_1[first_day] = [
                        period_counts_1[first_day][0] + delta,
                        period_counts_1[first_day][1] + 1
                    ]
                    last_msg_date_1 = date
                else:
                    delta = (date - last_msg_date_2).total_seconds() // 3600
                    period_counts_2[first_day] = [
                        period_counts_2[first_day][0] + delta,
                        period_counts_2[first_day][1] + 1
                    ]
                    last_msg_date_2 = date
            else:
                first_day = last_day
        means_1 = dict()
        means_2 = dict()
        for key, value in period_counts_1.items():
            if value[1] != 0:
                means_1[key.strftime("%Y-%m-%d")] = round(value[0] / value[1])
            else:
                means_1[key.strftime("%Y-%m-%d")] = 0
        for key, value in period_counts_2.items():
            if value[1] != 0:
                means_2[key.strftime("%Y-%m-%d")] = round(value[0] / value[1])
            else:
                means_2[key.strftime("%Y-%m-%d")] = 0

        return means_1, means_2
