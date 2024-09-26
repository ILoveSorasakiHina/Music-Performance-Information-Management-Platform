import json
import ssl
import urllib.request
from datetime import datetime
from django.core.management.base import BaseCommand
from pymongo import MongoClient
from DataGovCRUD.models import Event, ShowInfo, Location, Organizer

MONGO_URI = 'mongodb://localhost:27017/'
DB_NAME = 'crawl_logs'


class Command(BaseCommand):
    help = 'Update data from external JSON source'

    def handle(self, *args, **kwargs):
        url = 'https://cloud.culture.tw/frontsite/trans/SearchShowAction.do?method=doFindTypeJ&category=1'
        context = ssl._create_unverified_context()

        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        log_collection = db['crawl_logs']

        try:
            client = MongoClient(MONGO_URI)
            db = client[DB_NAME]
            print("Connected to MongoDB")
        except Exception as e:
            print("Failed to connect to MongoDB:", e)

        start_time = datetime.now()
        try:
            with urllib.request.urlopen(url, context=context) as jsondata:
                data = json.loads(jsondata.read().decode('utf-8-sig'))

            def parse_date(date_str):
                for fmt in ('%Y/%m/%d %H:%M:%S', '%Y/%m/%d', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d'):
                    try:
                        return datetime.strptime(date_str, fmt)
                    except ValueError:
                        pass
                raise ValueError(f"日期格式不匹配: {date_str}")

            def parse_datetime(datetime_str):
                if not datetime_str:
                    return None
                for fmt in ('%Y/%m/%d %H:%M:%S', '%Y-%m-%d %H:%M:%S'):
                    try:
                        return datetime.strptime(datetime_str, fmt)
                    except ValueError:
                        pass
                raise ValueError(f"日期時間格式不匹配: {datetime_str}")

            for event_data in data:
                start_date = parse_date(event_data['startDate']).date()
                end_date = parse_date(event_data['endDate']).date()
                edit_modify_date = parse_datetime(event_data.get('editModifyDate'))

                event, created = Event.objects.update_or_create(
                    uid=event_data['UID'],
                    defaults={
                        'version': event_data['version'],
                        'title': event_data['title'],
                        'category': event_data['category'],
                        'description_filter_html': event_data['descriptionFilterHtml'],
                        'image_url': event_data['imageUrl'],
                        'web_sale': event_data['webSales'],
                        'source_web_promote': event_data['sourceWebPromote'],
                        'comment': event_data['comment'],
                        'edit_modify_date': edit_modify_date,
                        'source_web_name': event_data['sourceWebName'],
                        'start_date': start_date,
                        'end_date': end_date,
                        'hit_rate': event_data['hitRate'],
                        'discount_info': event_data['discountInfo']
                    }
                )

                for organizer_name in event_data['masterUnit']:
                    organizer, created = Organizer.objects.update_or_create(name=organizer_name)
                    event.master_unit.add(organizer)

                for organizer_name in event_data['subUnit']:
                    organizer, created = Organizer.objects.update_or_create(name=organizer_name)
                    event.sub_unit.add(organizer)

                for organizer_name in event_data['supportUnit']:
                    organizer, created = Organizer.objects.update_or_create(name=organizer_name)
                    event.support_unit.add(organizer)

                for organizer_name in event_data['otherUnit']:
                    organizer, created = Organizer.objects.update_or_create(name=organizer_name)
                    event.other_unit.add(organizer)

                for show_info in event_data['showInfo']:
                    location, created = Location.objects.update_or_create(
                        name=show_info['locationName'],
                        address=show_info['location'],
                        defaults={
                            'latitude': show_info['latitude'],
                            'longitude': show_info['longitude']
                        }
                    )
                    time = parse_date(show_info['time']).date()
                    end_time = parse_datetime(show_info.get('endTime'))
                    ShowInfo.objects.update_or_create(
                        event=event,
                        time=time,
                        end_time=end_time,
                        defaults={
                            'on_sale': show_info['onSales'] == 'Y',
                            'price': show_info['price'],
                            'location': location
                        }
                    )
            log_collection.insert_one({
                'timestamp': start_time,
                'status': 'success',
                'message': 'Data updated successfully.'
            })

        except Exception as e:
            log_collection.insert_one({
                'timestamp': start_time,
                'status': 'failure',
                'message': str(e)
            })
            raise
