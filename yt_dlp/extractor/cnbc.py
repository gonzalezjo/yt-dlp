import json
from .common import InfoExtractor
from ..utils import traverse_obj, unified_strdate


class CNBCVideoIE(InfoExtractor):
    _VALID_URL = r"https?://(?:www\.)?cnbc\.com(?P<path>/video/(?:[^/]+/)+(?P<id>[^./?#&]+)\.html)"

    _TESTS = [
        {
            "url": "https://www.cnbc.com/video/2023/12/07/mcdonalds-just-unveiled-cosmcsits-new-spinoff-brand.html",
            "info_dict": {
                "title": "Here's a first look at McDonald's new spinoff brand, CosMc's",
                "description": "McDonald's unveiled its new spinoff brand known as CosMc's this week, announcing that the new brand's first location will open in Bolingbrook, Illinois. CosMc's drive-thru focused menu features brand new lemonades and teas, blended beverages, and cold coffee, as well as a small lineup of food. The burger chain first revealed it was creating CosMc's as a spinoff during its second-quarter earnings call in July.",
                "thumbnails": [
                    {
                        "url": "https://image.cnbcfm.com/api/v1/image/107344192-1701894812493-CosMcsskyHero_2336x1040_hero-desktop.jpg?v=1701894855"
                    }
                ],
                "duration": 65.0,
                "timestamp": 1701977810,
                "ext": "mp4",
                "id": "7000325168",
                "channel" : "News Videos",
                "upload_date" : "20231207",
                "thumbnail": 'https://image.cnbcfm.com/api/v1/image/107344192-1701894812493-CosMcsskyHero_2336x1040_hero-desktop.jpg?v=1701894855'
            },
            "expected_warnings": ["Unable to download f4m manifest"],
        }
    ]

    def _real_extract(self, url):
        path, display_id = self._match_valid_url(url).groups()
        video_id = self._download_json(
            "https://webql-redesign.cnbcfm.com/graphql",
            display_id,
            query={
                "query": """{ page(path: "%s") { vcpsId } }""" % path,
            },
        )["data"]["page"]["vcpsId"]
        webpage = self._download_webpage(url, video_id)
        metadata = json.loads(
            self._html_search_regex(
                r"window\.__s_data=(\{.*?\});", webpage, "video JSON data."
            )
        )
        url = metadata["page"]["page"]["layout"][1]["columns"][0]["modules"][0]["data"]["encodings"][0]["url"]

        # import pdb
        # pdb.set_trace()

        return {
            "id": str(video_id),
            "url": metadata["page"]["page"]["layout"][1]["columns"][0]["modules"][0][
                "data"
            ]["encodings"][0]["url"],
            "formats": self._extract_akamai_formats(url, str(video_id)),
            "channel": self._html_search_regex(r'<div class="ClipPlayer-clipPlayerIntroSection"><[^>]*>([^<]+)<', webpage, 'channel name'),
            "upload_date": unified_strdate(metadata['page']['page']['layout'][1]['columns'][0]['modules'][0]['data']['uploadDate']),
            **traverse_obj(
                self._search_json_ld(webpage, str(video_id), default={}),
                {
                    "title": "title",
                    "description": "description",
                    "duration": "duration",
                    "timestamp": "timestamp",
                    "thumbnails": "thumbnails",
                },
            ),
        }
