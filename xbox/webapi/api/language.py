"""
Language definitions
"""


class XboxLiveLanguage:
    def __init__(self, name, short_id, identifier, locale):
        """
        Initialize a new instance of :class:`XboxLiveLanguage`

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


class DefaultXboxLiveLanguages:
    """
    Collection of locales compatible with XBL
    """

    Argentina = XboxLiveLanguage("Argentina", "AR", "es_AR", "es-AR")
    Australia = XboxLiveLanguage("Australia", "AU", "en_AU", "en-AU")
    Austria = XboxLiveLanguage("Austria", "AT", "de_AT", "de-AT")
    Belgium = XboxLiveLanguage("Belgium", "BE", "fr_BE", "fr-BE")
    Belgium_NL = XboxLiveLanguage("Belgium (NL)", "NL", "nl_BE", "nl-BE")
    Brazil = XboxLiveLanguage("Brazil", "BR", "pt_BR", "pt-BR")
    Canada = XboxLiveLanguage("Canada", "CA", "en_CA", "en-CA")
    Canada_FR = XboxLiveLanguage("Canada (FR)", "CA", "fr_CA", "fr-CA")
    Czech_Republic = XboxLiveLanguage("Czech Republic", "CZ", "en_CZ", "en-CZ")
    Denmark = XboxLiveLanguage("Denmark", "DK", "da_DK", "da-DK")
    Finland = XboxLiveLanguage("Finland", "FI", "fi_FI", "fi-FI")
    France = XboxLiveLanguage("France", "FR", "fr_FR", "fr-FR")
    Germany = XboxLiveLanguage("Germany", "DE", "de_DE", "de-DE")
    Greece = XboxLiveLanguage("Greece", "GR", "en_GR", "en-GR")
    Hong_Kong = XboxLiveLanguage("Hong Kong", "HK", "en_HK", "en-HK")
    Hungary = XboxLiveLanguage("Hungary", "HU", "en_HU", "en-HU")
    India = XboxLiveLanguage("India", "IN", "en_IN", "en-IN")
    Great_Britain = XboxLiveLanguage("Great Britain", "GB", "en_GB", "en-GB")
    Israel = XboxLiveLanguage("Israel", "IL", "en_IL", "en-IL")
    Italy = XboxLiveLanguage("Italy", "IT", "it_IT", "it-IT")
    Japan = XboxLiveLanguage("Japan", "JP", "ja_JP", "ja-JP")
    Mexico = XboxLiveLanguage("Mexico", "MX", "es_MX", "es-MX")
    Chile = XboxLiveLanguage("Chile", "CL", "es_CL", "es-CL")
    Colombia = XboxLiveLanguage("Colombia", "CO", "es_CO", "es-CO")
    Netherlands = XboxLiveLanguage("Netherlands", "NL", "nl_NL", "nl-NL")
    New_Zealand = XboxLiveLanguage("New Zealand", "NZ", "en_NZ", "en-NZ")
    Norway = XboxLiveLanguage("Norway", "NO", "nb_NO", "nb-NO")
    Poland = XboxLiveLanguage("Poland", "PL", "pl_PL", "pl-PL")
    Portugal = XboxLiveLanguage("Portugal", "PT", "pt_PT", "pt-PT")
    Russia = XboxLiveLanguage("Russia", "RU", "ru_RU", "ru-RU")
    Saudi_Arabia = XboxLiveLanguage("Saudi Arabia", "SA", "en_SA", "en-SA")
    Singapore = XboxLiveLanguage("Singapore", "SG", "en_SG", "en-SG")
    Slovakia = XboxLiveLanguage("Slovakia", "SK", "en_SK", "en-SK")
    South_Africa = XboxLiveLanguage("South Afrida", "ZA", "en_ZA", "en-ZA")
    Korea = XboxLiveLanguage("Korea", "KR", "ko_KR", "ko-KR")
    Spain = XboxLiveLanguage("Spain", "ES", "es_ES", "es-ES")
    Switzerland = XboxLiveLanguage("Switzerland", "CH", "de_CH", "de-CH")
    Switzerland_FR = XboxLiveLanguage("Switzerland (FR)", "CH", "fr_CH", "fr-CH")
    United_Arab_Emirates = XboxLiveLanguage(
        "United Arab Emirates", "AE", "en_AE", "en-AE"
    )
    United_States = XboxLiveLanguage("United States", "US", "en_US", "en-US")
    Ireland = XboxLiveLanguage("Ireland", "IE", "en_IE", "en-IE")
