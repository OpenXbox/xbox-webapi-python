"""
Language definitions
"""


class XboxLiveLocale(object):
    def __init__(self, name, short_id, identifier, locale):
        """
        Initialize a new instance of :class:`XboxLiveLocale`

        Args:
            name (str): Full name describing the language / country
            short_id (str): Short Id (e.g. "AT" for Austria)
            identifier (str): Identifier (e.g. "de_AT" for Austria)
            locale (str): Locale (e.g. "de-AT" for Austria)
        """
        self.name = name
        self.short_id = short_id
        self.identifier = identifier
        self.locale = locale


class XboxLiveLanguage(object):
    """
    Collection of languages compatible with XBL
    """
    Argentina = XboxLiveLocale("Argentina", "AR", "es_AR", "es-AR")
    Australia = XboxLiveLocale("Australia", "AU", "en_AU", "en-AU")
    Austria = XboxLiveLocale("Austria", "AT", "de_AT", "de-AT")
    Belgium = XboxLiveLocale("Belgium", "BE", "fr_BE", "fr-BE")
    Belgium_NL = XboxLiveLocale("Belgium (NL)", "NL", "nl_BE", "nl-BE")
    Brazil = XboxLiveLocale("Brazil", "BR", "pt_BR", "pt-BR")
    Canada = XboxLiveLocale("Canada", "CA", "en_CA", "en-CA")
    Canada_FR = XboxLiveLocale("Canada (FR)", "CA", "fr_CA", "fr-CA")
    Czech_Republic = XboxLiveLocale("Czech Republic", "CZ", "en_CZ", "en-CZ")
    Denmark = XboxLiveLocale("Denmark", "DK", "da_DK", "da-DK")
    Finland = XboxLiveLocale("Finland", "FI", "fi_FI", "fi-FI")
    France = XboxLiveLocale("France", "FR", "fr_FR", "fr-FR")
    Germany = XboxLiveLocale("Germany", "DE", "de_DE", "de-DE")
    Greece = XboxLiveLocale("Greece", "GR", "en_GR", "en-GR")
    Hong_Kong = XboxLiveLocale("Hong Kong", "HK", "en_HK", "en-HK")
    Hungary = XboxLiveLocale("Hungary", "HU", "en_HU", "en-HU")
    India = XboxLiveLocale("India", "IN", "en_IN", "en-IN")
    Great_Britain = XboxLiveLocale("Great Britain", "GB", "en_GB", "en-GB")
    Israel = XboxLiveLocale("Israel", "IL", "en_IL", "en-IL")
    Italy = XboxLiveLocale("Italy", "IT", "it_IT", "it-IT")
    Japan = XboxLiveLocale("Japan", "JP", "ja_JP", "ja-JP")
    Mexico = XboxLiveLocale("Mexico", "MX", "es_MX", "es-MX")
    Chile = XboxLiveLocale("Chile", "CL", "es_CL", "es-CL")
    Colombia = XboxLiveLocale("Colombia", "CO", "es_CO", "es-CO")
    Netherlands = XboxLiveLocale("Netherlands", "NL", "nl_NL", "nl-NL")
    New_Zealand = XboxLiveLocale("New Zealand", "NZ", "en_NZ", "en-NZ")
    Norway = XboxLiveLocale("Norway", "NO", "nb_NO", "nb-NO")
    Poland = XboxLiveLocale("Poland", "PL", "pl_PL", "pl-PL")
    Portugal = XboxLiveLocale("Portugal", "PT", "pt_PT", "pt-PT")
    Russia = XboxLiveLocale("Russia", "RU", "ru_RU", "ru-RU")
    Saudi_Arabia = XboxLiveLocale("Saudi Arabia", "SA", "en_SA", "en-SA")
    Singapore = XboxLiveLocale("Singapore", "SG", "en_SG", "en-SG")
    Slovakia = XboxLiveLocale("Slovakia", "SK", "en_SK", "en-SK")
    South_Africa = XboxLiveLocale("South Afrida", "ZA", "en_ZA", "en-ZA")
    Korea = XboxLiveLocale("Korea", "KR", "ko_KR", "ko-KR")
    Spain = XboxLiveLocale("Spain", "ES", "es_ES", "es-ES")
    Switzerland = XboxLiveLocale("Switzerland", "CH", "de_CH", "de-CH")
    Switzerland_FR = XboxLiveLocale("Switzerland (FR)", "CH", "fr_CH", "fr-CH")
    United_Arab_Emirates = XboxLiveLocale("United Arab Emirates", "AE", "en_AE", "en-AE")
    United_States = XboxLiveLocale("United States", "US", "en_US", "en-US")
    Ireland = XboxLiveLocale("Ireland", "IE", "en_IE", "en-IE")
