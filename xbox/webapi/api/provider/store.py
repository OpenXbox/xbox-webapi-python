import requests


class StoreProvider(object):

    LOCALIZED_GAME_PROPERTY_ENDPOINT = "https://displaycatalog.mp.microsoft.com/v7/productFamilies/games?market=%s&languages=%s"
    PRODUCTS_FROM_IDS_ENDPOINT = "https://displaycatalog.mp.microsoft.com/v7.0/products/?fieldsTemplate=%s&bigIds=%s&market=%s&languages=%s"
    PRODUCT_ADDON_LOOK_UP_ENDPOINT = "https://reco-public.rec.mp.microsoft.com/channels/Reco/V8.0/Lists/Mapping/addonsbyparentwithdetails/%s?ItemTypes=Consumable,Durable&Market=%s&Language=%s&deviceFamily=Windows.Xbox&count=10"
    PRODUCT_ID_LOOK_UP_ENDPOINT = "https://displaycatalog.md.mp.microsoft.com/v7.0/products/lookup?market=%s&languages=%s&alternateId=%s&value=%s&fieldsTemplate=details"
    PRODUCT_IN_BUNDLE_LIST_ENDPOINT = "https://reco-public.rec.mp.microsoft.com/channels/reco/v8.0/Lists/Mapping/BundlesBySeed/%s?itemTypes=Game,Consumable,Durable&DeviceFamily=Windows.Xbox&count=%d&skipitems=%d&market=%s&language=%s"
    PRODUCT_RELATED_ITEM_LIST_ENDPOINT = "https://reco-public.rec.mp.microsoft.com/channels/reco/v8.0/related/Game/%s?itemTypes=Game&DeviceFamily=Windows.Xbox&count=10&market=%s&language=%s"
  
    CORRELATION_VECTOR_KEY = "MS-CV"

    BASE_URL_COLLECTIONS = "https://collections.mp.microsoft.com/v7.0"
    BASE_URL_DISPLAYCATALOG_MP = "https://displaycatalog.mp.microsoft.com/v7.0"
    BASE_URL_DISPLAYCATALOG_MD_MP = "https://displaycatalog.md.mp.microsoft.com/v7.0"
    BASE_URL_MARKETPLACE = "https://reco-public.rec.mp.microsoft.com/channels"

    SEPARATOR = ","
    HEADERS_STORE = {
        CORRELATION_VECTOR_KEY: "aabdec924sadfh8342.0",
        "User-Agent": "WindowsStoreSDK",
        #"X-ClientCorrelationId": None,
        #"X-UserAgent": None
    }

    def __init__(self):
        self.session = requests.session()

    def get_backwards_compatible_games(self):
        url = "https://settings.data.microsoft.com/settings/v2.0/xbox/backcompatcatalogidmapall?scenarioid=all"
        return self.session.get(url, headers=self.HEADERS_STORE)

    #Recommendations
    def get_store_recommendation_list_with_gold(self, unknown, market, language, uid, count, skip_items):
        url = self.BASE_URL_MARKETPLACE + "/reco/v8.0/lists/collection/%s?" % unknown
        params = {
            "itemTypes": ItemType.GAME,
            "Market": market,
            "PreferredLanguages": language,
            "deviceFamily": PlatformType.XBOX,
            "uid": uid,
            "count": count,
            "skipItems": skip_items
        }
        return self.session.get(url, params=params, headers=self.HEADERS_STORE)

    def get_store_recommendation_list(self, unknown, count, market, language, skip_items):
        url = self.BASE_URL_MARKETPLACE + "/reco/v8.0/lists/computed/%s?" % unknown
        params = {
            "itemTypes": ItemType.GAME,
            "deviceFamily": PlatformType.XBOX,
            "count": count,
            "clientType": ClientType.XBOX_APP,
            "market": market,
            "PreferredLanguages": language,
            "skipItems": skip_items
        }
        return self.session.get(url, params=params, headers=self.HEADERS_STORE)

    def get_store_recommendation_app_list(self, unknown, market, language, count, skip_items):
        url = self.BASE_URL_MARKETPLACE + "/reco/V8.0/Lists/Collection/%s?" % unknown
        params = {
            "itemTypes": ItemType.APPS,
            "market": market,
            "language": language,
            "deviceFamily": PlatformType.XBOX,
            "count": count,
            "skipItems": skip_items
        }
        return self.session.get(url, params=params, headers=self.HEADERS_STORE)

    def get_store_recommendation_addon_list(self, unknown, count, market, language, skip_items):
        url = self.BASE_URL_MARKETPLACE + "/reco/v8.0/lists/computed/%s?" % unknown
        params = {
            "itemTypes": ItemType.DURABLE,
            "deviceFamily": PlatformType.XBOX,
            "count": count,
            "clientType": ClientType.XBOX_APP,
            "market": market,
            "PreferredLanguages": language,
            "skipItems": skip_items
        }
        return self.session.get(url, params=params, headers=self.HEADERS_STORE)

    def get_store_collection_list(self, ):
        url = self.BASE_URL_COLLECTIONS + "/collections/query"
        post_data = {
            "Beneficiaries": [],
            "CheckSatisfyingEntitlements": True,
            "EntitlementFilters": [],
            "Market": "DE",
            "ProductSkuIds": [
                {"productId": "BZ5VLVX84STW"}
            ],
            "ShowSatisfiedBy": True,
            "ValidityType": "ValidAndFuture"
        }
        return self.session.post(url, json=post_data, headers=self.HEADERS_STORE)

    # unknown -> probably of BigCatProductType-type
    def get_search_results(self, product_family, query):
        url = "https://displaycatalog.mp.microsoft.com/v7.0/productFamilies/%s/products?" % product_family
        params = {
            "query": query,
            "market": "US",
            "languages": "en-US",
            "fieldsTemplate": "details",
            "platformdependencyname": "windows.xbox"
        }
        import requests
        return requests.get(url, params=params, headers=self.HEADERS_STORE)

    def get_search_autosuggestions(self, search_query, market, languages):
        url = self.BASE_URL_DISPLAYCATALOG_MP + "/productFamilies/autosuggest?"
        params = {
            "query": search_query,
            "productFamilyNames": "Games",
            "market": market,
            "languages": languages,
            "platformdependencyname": PlatformType.XBOX
        }
        return self.session.get(url, params=params, headers=self.HEADERS_STORE)

    def get_ratings(self, market, languages):
        url = self.BASE_URL_DISPLAYCATALOG_MD_MP + "/ratings?"
        params = {
            "market": market,
            "languages": languages
        }
        return self.session.get(url, params=params, headers=self.HEADERS_STORE)

    def get_recents_list(self):
        pass
    
    def get_products_reduced_info_from_ids_with_filter(self, fields_template, big_ids, market, languages):
        url = self.BASE_URL_DISPLAYCATALOG_MP + "/products/?"
        params = {
            "fieldsTemplate": fields_template,
            "bigIds": big_ids,
            "market": market,
            "languages": languages
        }
        return self.session.get(url, params=params, headers=self.HEADERS_STORE)

    def get_product_from_alternate_id(self, market, languages, id, id_type):
        url = self.BASE_URL_DISPLAYCATALOG_MD_MP + "/products/lookup?"
        params = {
            "market": market,
            "languages": languages,
            "alternateId": id_type,
            "value": id,
            "fieldsTemplate": "details"
        }
        return self.session.get(url, params=params, headers=self.HEADERS_STORE)

    def get_products_from_ids(self, fields_template, big_ids, market, languages):
        url = self.BASE_URL_DISPLAYCATALOG_MP + "/products/?"
        params = {
            "fieldsTemplate": fields_template,
            "bigIds": big_ids,
            "market": market,
            "languages": languages
        }
        return self.session.get(url, params=params, headers=self.HEADERS_STORE)

    def get_product_related_itemlist(self, unknown, count, market, language):
        url = self.BASE_URL_MARKETPLACE + "/reco/v8.0/related/Game/%s?" % unknown
        params = {
            "itemTypes": ItemType.GAME,
            "deviceFamily": PlatformType.XBOX,
            "count": count,
            "market": market,
            "language": language
        }
        return self.session.get(url, params=params, headers=self.HEADERS_STORE)

    def get_product_in_bundle_list(self, unknown, count, skip_items, market, language):
        url = self.BASE_URL_MARKETPLACE + "/reco/v8.0/Lists/Mapping/BundlesBySeed/%s?" % unknown
        params = {
            "itemTypes": self.SEPARATOR.join([ItemType.GAME, ItemType.CONSUMABLE, ItemType.DURABLE]),
            "deviceFamily": PlatformType.XBOX,
            "count": count,
            "skipItems": skip_items,
            "market": market,
            "language": language
        }
        return self.session.get(url, params=params, headers=self.HEADERS_STORE)

    def get_product_addons(self, unknown, market, language, count):
        url = self.BASE_URL_MARKETPLACE + "/reco/V8.0/Lists/Mapping/addonsbyparentwithdetails/%s?" % unknown
        params = {
            "itemTypes": self.SEPARATOR.join([ItemType.CONSUMABLE, ItemType.DURABLE]),
            "market": market,
            "language": language,
            "count": count,
            "deviceFamily": PlatformType.XBOX
        }
        return self.session.get(url, params=params, headers=self.HEADERS_STORE)


class SubscriptionType(object):
    Unknown = 0
    XboxGold = 1
    EAAccess = 2


class SubscriptionTypeMap(object):
    SubscriptionType.XboxGold = "CFQ7TTC0K5DJ"
    SubscriptionType.EAAccess = "CFQ7TTC0K5DH"


class UserRatingTimeSpan(object):
    ALLTIME = "alltime"
    SEVEN_DAYS = "7days"
    THIRTY_DAYS = "30days"


class PlatformType(object):
    XBOX = "windows.xbox"
    DESKTOP = "windows.desktop"


class BigCatProductType(object):
    GAME = "Game"
    DURABLE = "Durable"
    CONSUMABLE = "Consumable"
    APPLICATION = "Application"


class AlternateIdType(object):
    LEGACY_XBOX_PRODUCT_ID = "LegacyXboxProductId"
    XBOX_TITLE_ID = "XboxTitleId"
    PACKAGE_FAMILY_NAME = "PackageFamilyName"


class StoreListType(object):
    GAMES_RECENT = "New"
    GAMES_MOST_PLAYED = "MostPlayed"
    GAMES_COMING_SOON = "ComingSoon"
    ADDONS_NEW = "New"
    ADDONS_TOP_PAID = "TopPaid"
    ADDONS_TOP_FREE = "TopFree"
    APPS_NEW = "AppsNew"
    APPS_LIST_POPULAR_ON_XBOX = "AppsListsPopularOnXbox"
    GOLD_GAME = "GamesWithGold"
    GOLD_DEALS = "DealsWithGold"


class LocalizedGamePropertyDataTypes(object):
    DISPLAY_DATA_HW_FIELDS_KEY = "hardwarefields"
    DISPLAY_DATA_HW_FIELD_VALUES_KEY = "hardwarefieldvalues"


class ItemType(object):
    GAME = "Game"
    APPS = "Apps"
    DURABLE = "Durable"
    CONSUMABLE = "Consumable"


class ClientType(object):
    XBOX_APP = "XboxApp"
