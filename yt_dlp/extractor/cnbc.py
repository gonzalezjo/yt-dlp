from .common import InfoExtractor
from ..utils import smuggle_url, clean_html
import json
import re
from datetime import datetime
from ..utils import unified_timestamp, variadic


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
        'url': "https://www.cnbc.com/video/2023/12/07/mcdonalds-just-unveiled-cosmcsits-new-spinoff-brand.html",
        "info_dict":{
            "url" : "https://pdl-iphone-cnbc-com.akamaized.net/VCPS/Y2023/M12D08/7000325282/1702052880974-CosMc_s_QT_L.mp4",
            "title" : "Here's a first look at McDonald's new spinoff brand, CosMc's",
            "description" : "McDonald's unveiled its new spinoff brand known as CosMc's this week, announcing that the new brand's first location will open in Bolingbrook, Illinois. CosMc's drive-thru focused menu features brand new lemonades and teas, blended beverages, and cold coffee, as well as a small lineup of food. The burger chain first revealed it was creating CosMc's as a spinoff during its second-quarter earnings call in July.",
            "thumbnails" : [{'url': 'https://image.cnbcfm.com/api/v1/image/107344192-1701894812493-CosMcsskyHero_2336x1040_hero-desktop.jpg?v=1701894855'}],
            "duration" : 65.0,
            "timestamp" : 1701977810,
            "ext" : "mp4",
            "formats" : [{'format_id': 'hls-4939', 'format_index': None, 'url': 'https://cnbcawsmpvod.akamaized.net/out/v1/d78b4c99801348359c73d952ddb04cf4/54fbf64382f04b94bb69340d5528ff8b/26cdcccd8cb84f5398bc0124836d47ee/8f04d2a67a134a7d833c385e06674382/6d011a6dfa714175b3c7517a37afb231/master_1.m3u8', 'manifest_url': 'https://cnbcawsmpvod.akamaized.net/out/v1/d78b4c99801348359c73d952ddb04cf4/54fbf64382f04b94bb69340d5528ff8b/26cdcccd8cb84f5398bc0124836d47ee/master.m3u8', 'tbr': 4939.663, 'ext': 'mp4', 'fps': 23.976, 'protocol': 'm3u8_native', 'preference': None, 'quality': None, 'has_drm': False, 'width': 1920, 'height': 1080, 'vcodec': 'avc1.4D4028', 'acodec': 'mp4a.40.2', 'dynamic_range': None}, {'format_id': 'hls-267', 'format_index': None, 'url': 'https://cnbcawsmpvod.akamaized.net/out/v1/d78b4c99801348359c73d952ddb04cf4/54fbf64382f04b94bb69340d5528ff8b/26cdcccd8cb84f5398bc0124836d47ee/8f04d2a67a134a7d833c385e06674382/6d011a6dfa714175b3c7517a37afb231/master_2.m3u8', 'manifest_url': 'https://cnbcawsmpvod.akamaized.net/out/v1/d78b4c99801348359c73d952ddb04cf4/54fbf64382f04b94bb69340d5528ff8b/26cdcccd8cb84f5398bc0124836d47ee/master.m3u8', 'tbr': 267.225, 'ext': 'mp4', 'fps': 23.976, 'protocol': 'm3u8_native', 'preference': None, 'quality': None, 'has_drm': False, 'width': 400, 'height': 224, 'vcodec': 'avc1.42C00D', 'acodec': 'mp4a.40.5', 'dynamic_range': None}, {'format_id': 'hls-328', 'format_index': None, 'url': 'https://cnbcawsmpvod.akamaized.net/out/v1/d78b4c99801348359c73d952ddb04cf4/54fbf64382f04b94bb69340d5528ff8b/26cdcccd8cb84f5398bc0124836d47ee/8f04d2a67a134a7d833c385e06674382/6d011a6dfa714175b3c7517a37afb231/master_3.m3u8', 'manifest_url': 'https://cnbcawsmpvod.akamaized.net/out/v1/d78b4c99801348359c73d952ddb04cf4/54fbf64382f04b94bb69340d5528ff8b/26cdcccd8cb84f5398bc0124836d47ee/master.m3u8', 'tbr': 328.598, 'ext': 'mp4', 'fps': 23.976, 'protocol': 'm3u8_native', 'preference': None, 'quality': None, 'has_drm': False, 'width': 400, 'height': 224, 'vcodec': 'avc1.42C00D', 'acodec': 'mp4a.40.2', 'dynamic_range': None}, {'format_id': 'hls-544', 'format_index': None, 'url': 'https://cnbcawsmpvod.akamaized.net/out/v1/d78b4c99801348359c73d952ddb04cf4/54fbf64382f04b94bb69340d5528ff8b/26cdcccd8cb84f5398bc0124836d47ee/8f04d2a67a134a7d833c385e06674382/6d011a6dfa714175b3c7517a37afb231/master_4.m3u8', 'manifest_url': 'https://cnbcawsmpvod.akamaized.net/out/v1/d78b4c99801348359c73d952ddb04cf4/54fbf64382f04b94bb69340d5528ff8b/26cdcccd8cb84f5398bc0124836d47ee/master.m3u8', 'tbr': 544.258, 'ext': 'mp4', 'fps': 23.976, 'protocol': 'm3u8_native', 'preference': None, 'quality': None, 'has_drm': False, 'width': 400, 'height': 224, 'vcodec': 'avc1.42C00D', 'acodec': 'mp4a.40.2', 'dynamic_range': None}, {'format_id': 'hls-770', 'format_index': None, 'url': 'https://cnbcawsmpvod.akamaized.net/out/v1/d78b4c99801348359c73d952ddb04cf4/54fbf64382f04b94bb69340d5528ff8b/26cdcccd8cb84f5398bc0124836d47ee/8f04d2a67a134a7d833c385e06674382/6d011a6dfa714175b3c7517a37afb231/master_5.m3u8', 'manifest_url': 'https://cnbcawsmpvod.akamaized.net/out/v1/d78b4c99801348359c73d952ddb04cf4/54fbf64382f04b94bb69340d5528ff8b/26cdcccd8cb84f5398bc0124836d47ee/master.m3u8', 'tbr': 770.397, 'ext': 'mp4', 'fps': 23.976, 'protocol': 'm3u8_native', 'preference': None, 'quality': None, 'has_drm': False, 'width': 640, 'height': 360, 'vcodec': 'avc1.42C01E', 'acodec': 'mp4a.40.2', 'dynamic_range': None}, {'format_id': 'hls-982', 'format_index': None, 'url': 'https://cnbcawsmpvod.akamaized.net/out/v1/d78b4c99801348359c73d952ddb04cf4/54fbf64382f04b94bb69340d5528ff8b/26cdcccd8cb84f5398bc0124836d47ee/8f04d2a67a134a7d833c385e06674382/6d011a6dfa714175b3c7517a37afb231/master_6.m3u8', 'manifest_url': 'https://cnbcawsmpvod.akamaized.net/out/v1/d78b4c99801348359c73d952ddb04cf4/54fbf64382f04b94bb69340d5528ff8b/26cdcccd8cb84f5398bc0124836d47ee/master.m3u8', 'tbr': 982.922, 'ext': 'mp4', 'fps': 23.976, 'protocol': 'm3u8_native', 'preference': None, 'quality': None, 'has_drm': False, 'width': 640, 'height': 360, 'vcodec': 'avc1.4D401E', 'acodec': 'mp4a.40.2', 'dynamic_range': None}, {'format_id': 'hls-1421', 'format_index': None, 'url': 'https://cnbcawsmpvod.akamaized.net/out/v1/d78b4c99801348359c73d952ddb04cf4/54fbf64382f04b94bb69340d5528ff8b/26cdcccd8cb84f5398bc0124836d47ee/8f04d2a67a134a7d833c385e06674382/6d011a6dfa714175b3c7517a37afb231/master_7.m3u8', 'manifest_url': 'https://cnbcawsmpvod.akamaized.net/out/v1/d78b4c99801348359c73d952ddb04cf4/54fbf64382f04b94bb69340d5528ff8b/26cdcccd8cb84f5398bc0124836d47ee/master.m3u8', 'tbr': 1421.587, 'ext': 'mp4', 'fps': 23.976, 'protocol': 'm3u8_native', 'preference': None, 'quality': None, 'has_drm': False, 'width': 896, 'height': 504, 'vcodec': 'avc1.4D401F', 'acodec': 'mp4a.40.2', 'dynamic_range': None}, {'format_id': 'hls-1878', 'format_index': None, 'url': 'https://cnbcawsmpvod.akamaized.net/out/v1/d78b4c99801348359c73d952ddb04cf4/54fbf64382f04b94bb69340d5528ff8b/26cdcccd8cb84f5398bc0124836d47ee/8f04d2a67a134a7d833c385e06674382/6d011a6dfa714175b3c7517a37afb231/master_8.m3u8', 'manifest_url': 'https://cnbcawsmpvod.akamaized.net/out/v1/d78b4c99801348359c73d952ddb04cf4/54fbf64382f04b94bb69340d5528ff8b/26cdcccd8cb84f5398bc0124836d47ee/master.m3u8', 'tbr': 1878.632, 'ext': 'mp4', 'fps': 23.976, 'protocol': 'm3u8_native', 'preference': None, 'quality': None, 'has_drm': False, 'width': 1280, 'height': 720, 'vcodec': 'avc1.4D401F', 'acodec': 'mp4a.40.2', 'dynamic_range': None}],
            "id" : '7000325168'
        }
    }
    
    ]

    def _real_extract(self, url):
        path, display_id = self._match_valid_url(url).groups()
        video_id = self._download_json(
            "https://webql-redesign.cnbcfm.com/graphql",
            display_id,
            query={
                "query": """{
                    page(path: "%s") {
                    vcpsId
                }
            }"""
                % path,
            },
        )["data"]["page"]["vcpsId"]
        webpage = self._download_webpage(url, video_id)
        cleaned = clean_html(webpage)
        matched = re.search(r'window\.__s_data=(\{.*?\});', cleaned)
        if not matched:
            raise ValueError("JSON data not found")
        metadata = json.loads(matched.group(1))
        # assert(isinstance(json, str))
        url = metadata["page"]["page"]["layout"][1]["columns"][0]["modules"][0]["data"]["encodings"][0]["url"]

        # upload_date_string = metadata['page']['page']['layout'][1]['columns'][0]['modules'][0]['data']['uploadDate']
        # dt_object = datetime.strptime(upload_date_string, date_format)
        # timestamp = unified_timestamp(upload_date_string)

        # returns = self._json_ld(json.dumps(metadata), str(video_id))
        # json_ld = self._yield_json_ld(cleaned, str(video_id))
        info = self._search_json_ld(webpage, str(video_id), default={})
        info["formats"] = self._extract_akamai_formats(url, str(video_id))
        info["id"] = str(video_id)
        



        # import pdb
        # pdb.set_trace()
        # info = self._search_json_ld(cleaned, str(video_id), default={})


        # json_ld = json.dumps(metadata)

        # returns = self._json_ld(json_ld, str(video_id))
        # print(timestamp)

        return info