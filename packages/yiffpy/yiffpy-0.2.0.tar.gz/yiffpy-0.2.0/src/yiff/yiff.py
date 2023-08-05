#!/usr/bin/env python3
import requests
from requests.auth import HTTPBasicAuth
import json
from ratelimit import limits, sleep_and_retry

CALLS = 2
RATE_LIMIT = 1

@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
def check_limit():
    # Empty function just to check for calls to API
    return

global codes
codes = {
    "200":"OK",
    "204":"No Content",
    "403":"Forbidden",
    "404":"Not Found",
    "412":"Precondition Failed",
    "420":"Invalid Record",
    "421":"User Throttled",
    "422":"Locked",
    "423":"Already Exists",
    "424":"Invalid Parameters",
    "500":"Internal Server Error",
    "502":"Bad Gateway",
    "503":"Service Unavailable",
    "520":"Unknown Error",
    "522":"Origin Connection Time-out",
    "524":"Origin Connection Time-out",
    "525":"SSL Handshake Failed"
    
}

class sub:
    def __init__(self, data):
        self.id = data["id"]
        self.create = data["created_at"]
        self.update = data["updated_at"]
        self.width = data["file"]["width"]
        self.height = data["file"]["width"]
        self.type = data["file"]["ext"]
        self.md5 = data["file"]["md5"] 
        self.url = data["file"]["url"]
        self.prev_width = data["preview"]["width"]
        self.prev_height = data["preview"]["height"]
        self.prev_url = data["preview"]["url"]
        self.has_sample = data["sample"]["has"]
        if data["sample"]["has"] == True:
            self.sam_height = data["sample"]["height"]
            self.sam_width = data["sample"]["width"]
            self.sam_url = data["sample"]["url"]
            self.sam_altern = data["sample"]["alternates"]
        self.up = data["score"]["up"]
        self.down = data["score"]["down"]
        self.score = data["score"]["total"]
        self.tags = data["tags"]["general"]
        self.species = data["tags"]["species"]
        self.character = data["tags"]["character"]
        self.copyright = data["tags"]["copyright"]
        self.artist = data["tags"]["artist"]
        self.invalid = data["tags"]["invalid"]
        self.lore = data["tags"]["lore"]
        self.meta = data["tags"]["meta"]
        self.lock_tags = data["locked_tags"]
        self.change_seq = data["change_seq"]
        self.pending = data["flags"]["pending"]
        self.flagged = data["flags"]["flagged"]
        self.note_lock = data["flags"]["note_locked"]
        self.status_lock = data["flags"]["status_locked"]
        self.rating_lock = data["flags"]["rating_locked"]
        self.deleted = data["flags"]["deleted"]
        self.rating = data["rating"]
        self.sources = data["sources"]
        self.pools = data["pools"]
        self.parent = data["relationships"]["parent_id"]
        self.has_childs = data["relationships"]["has_children"]
        self.has_active_childs = data["relationships"]["has_active_children"]
        self.childs = data["relationships"]["children"]
        self.approver = data["approver_id"]
        self.poster = data["uploader_id"]
        self.desc = data["description"]
        self.com_count = data["comment_count"]
        self.is_fav = data["is_favorited"]
        self.has_notes = data["has_notes"]
        self.duration = data["duration"]
        self.favs = data["fav_count"]

class user:
    def __init__(self, data):
        self.wiki_page_version_count = data["wiki_page_version_count"]
        self.artist_version_count = data["artist_version_count"]
        self.pool_version_count = data["pool_version_count"]
        self.forum_post_count = data["forum_post_count"]
        self.comments = data["comment_count"]
        self.appeals = data["appeal_count"]
        self.flags = data["flag_count"]
        self.pos_feedback = data["positive_feedback_count"]
        self.neu_feedback = data["neutral_feedback_count"]
        self.neg_feedback = data["negative_feedback_count"]
        self.upload_limit = data["upload_limit"]
        self.id = data["id"]
        self.created_at = data["created_at"]
        self.name = data["name"]
        self.level = data["level"]
        self.base_upload_limit = data["base_upload_limit"]
        self.posts = data["post_upload_count"]
        self.post_updates = data["post_update_count"]
        self.banned = data["is_banned"]
        self.can_approve = data["can_approve_posts"]
        self.can_upload_free = data["can_upload_free"]
        self.level_str = data["level_string"]
        self.avatar_id = data["avatar_id"]

global version
version = "v0.2"

# Actual code begins here

class api:
    def __init__(self, user, key, header):
        self.header = {"User-Agent": header}
        self.user = user
        self.key = key
        self.e621 = "https://e621.net/"
        self.e926 = "https://e926.net/"

    def e6get(self, lnk):
        check_limit()
        r = requests.get(self.e621 + lnk, headers=self.header, auth=HTTPBasicAuth(self.user, self.key))
        json1 = json.loads(r.text)
        self.handleCode(r.status_code)
        return json1

    def handleCode(self, code):
        if code != 200:
            raise ConnectionRefusedError(str(code) + " " + codes[str(code)])
        else:
            return

    def getpost(self ,pid):
        pid = str(pid)
        lnk = "posts/" + pid + ".json"
        data = self.e6get(lnk)
        return sub(data["post"])

    def search(self, tags, limit, page):
        lnk = "posts.json?limit=" + str(limit) + "&page=" + str(page) + "&tags="
        for id, tag in enumerate(tags):
            lnk += tag
            if id != (len(tags) - 1):
                lnk += "+"
        data = self.e6get(lnk)
        posts = []
        for post in data["posts"]:
            posts.append(sub(post))
        return posts

    def getuser(self, uid):
        lnk = "users/" + str(uid) + ".json"
        data = self.e6get(lnk)
        return user(data)

    def searchuser(self, name):
        lnk = "users.json?search[name_matches]=" + name
        data = self.e6get(lnk)
        users = []
        for user in data:
            users.append(self.getuser(user["id"]))
        return users