import requests

if __name__ == "__main__":
    import os, sys
    import django

    from django.conf import settings

    import pprint

    pp = pprint.PrettyPrinter(indent=4, depth=10, compact=True, width=120)

    from logger import logger

    logger.info("Loading django...")

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
    logger.debug(sys.path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ao_qrick.settings")
    os.chdir("../")
    django.setup()

    logger.info("Django was load.")

else:
    from libs.logger import logger

from killboard.models import Item, VictimLog, Item2Victim


class KillBoardParser:
    API_TEMPLATE = "https://gameinfo.albiononline.com/api/gameinfo/events?limit={}&offset={}"

    def __init__(self, limit=50, max_offset=50):
        self.limit = limit
        self.max_offset = max_offset

    def exec(self):
        logger.info('Start work.')
        for offset in range(0, self.max_offset, self.limit):
            data = self.get_data(offset)
            parsed_data = self.parse_data(data)
            self.save_data(parsed_data)

    def get_data(self, offset: int):
        uri = self.API_TEMPLATE.format(self.limit, offset)

        logger.info("Request data from %s" % uri)

        return requests.get(uri).json()

    def parse_data(self, data: list):
        logger.info("Start parsing data.")

        parsed_data = []

        for event in data:
            logger.info("Found <%s>" % event['EventId'])

            items = {
                item['Type']: item['Count']
                for slot, item in event["Victim"]["Equipment"].items()
                if item
            }

            parsed_data.append(
                (
                    event['EventId'], {
                        'timestamp': event['TimeStamp'],
                        'items': items
                    }
                )
            )

        logger.info("Parsing result: \n {}".format(pp.pformat(parsed_data)))

        return parsed_data

    def save_data(self, parsed_data: list):
        logger.info("Start saving data.")

        for event_id, data in parsed_data:
            logger.info(
                "Create victim_log_obj with (timestamp<{timestamp}>, event_id=<{event_id}>)"
                    .format(timestamp=data['timestamp'], event_id=event_id)
            )

            victim_log_obj = VictimLog.objects.create(timestamp=data['timestamp'], event_id=event_id)

            Item2Victim.objects.bulk_create(
                [
                    Item2Victim(
                        item=Item.objects.get_or_create(name=item_name)[0],
                        victim=victim_log_obj,
                        count=count
                    )
                    for item_name, count in data['items'].items()
                ]
            )


if __name__ == "__main__":
    parser = KillBoardParser()
    parser.exec()
