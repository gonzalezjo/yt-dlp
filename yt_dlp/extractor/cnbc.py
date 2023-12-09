from .common import InfoExtractor
from ..utils import smuggle_url, clean_html
import json
import re


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
    _TEST = {
        "url": "https://www.cnbc.com/video/2018/07/19/trump-i-dont-necessarily-agree-with-raising-rates.html",
        "info_dict": {
            "id": "7000031301",
            "ext": "mp4",
            "title": "Trump: I don't necessarily agree with raising rates",
            "description": "md5:878d8f0b4ebb5bb1dda3514b91b49de3",
            "timestamp": 1531958400,
            "upload_date": "20180719",
            "uploader": "NBCU-CNBC",
        },
        "params": {
            "skip_download": True,
        },
        "skip": "Dead link",
    }

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
        url = metadata["page"]["page"]["layout"][1]["columns"][0]["modules"][0]["data"]["encodings"][0]["url"]
        upload_date = metadata['page']['page']['layout'][1]['columns'][0]['modules'][0]['data']['uploadDate']
        video_status = metadata['page']['page']['layout'][1]['columns'][0]['modules'][0]['data']['videoStatus']
        if metadata['page']['page']['layout'][1]['columns'][0]['modules'][0]['data']['authorFormattedFull'] != 'NA': 
            author = metadata['page']['page']['layout'][1]['columns'][0]['modules'][0]['data']['authorFormattedFull']

        import pdb
        pdb.set_trace()

        return {
            "id": video_id,
            "formats": self._extract_akamai_formats(url, str(video_id)),
        }
