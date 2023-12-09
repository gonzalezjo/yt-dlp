from .common import InfoExtractor
import json
import re
from datetime import datetime
from ..utils import clean_html, traverse_obj, unified_timestamp, variadic


class CNBCIE(InfoExtractor):
    _VALID_URL = r"https?://video\.cnbc\.com/gallery/\?video=(?P<id>[0-9]+)"
    _TEST = {
        "url": "http://video.cnbc.com/gallery/?video=3000503714",
        "info_dict": {
            "id": "3000503714",
            "ext": "mp4",
            "title": "Fighting zombies is big business",
            "description": "md5:0c100d8e1a7947bd2feec9a5550e519e",
            "timestamp": 1459332000,
            "upload_date": "20160330",
            "uploader": "NBCU-CNBC",
        },
        "params": {
            # m3u8 download
            "skip_download": True,
        },
        "skip": "Dead link",
    }

    def _real_extract(self, url):
        video_id = self._match_id(url)
        return {
            "_type": "url_transparent",
            "ie_key": "ThePlatform",
            "url": smuggle_url(
                "http://link.theplatform.com/s/gZWlPC/media/guid/2408950221/%s?mbr=true&manifest=m3u"
                % video_id,
                {"force_smil_url": True},
            ),
            "id": video_id,
        }


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
        duration = metadata['page']['page']['layout'][1]['columns'][1]['modules'][0]['data']['duration']

        return {
            "id": str(video_id),
            "url": metadata["page"]["page"]["layout"][1]["columns"][0]["modules"][0][
                "data"
            ]["encodings"][0]["url"],
            "formats": self._extract_akamai_formats(url, str(video_id)),
            "channel": self._html_search_regex(r'<div class="ClipPlayer-clipPlayerIntroSection"><[^>]*>([^<]+)<', webpage, 'channel name'),
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

        return info
