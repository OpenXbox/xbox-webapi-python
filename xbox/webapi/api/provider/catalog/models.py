from datetime import datetime
from enum import Enum
from typing import Any, List, Optional, Union

from pydantic import Field, field_validator

from xbox.webapi.common.models import PascalCaseModel


class AlternateIdType(str, Enum):
    LEGACY_XBOX_PRODUCT_ID = "LegacyXboxProductId"
    XBOX_TITLE_ID = "XboxTitleId"
    PACKAGE_FAMILY_NAME = "PackageFamilyName"


class FieldsTemplate(str, Enum):
    BROWSE = "browse"
    DETAILS = "details"


class PlatformType(str, Enum):
    XBOX = "windows.xbox"
    DESKTOP = "windows.desktop"


class Image(PascalCaseModel):
    file_id: Optional[str] = None
    eis_listing_identifier: Any = Field(None, alias="EISListingIdentifier")
    background_color: Optional[str] = None
    caption: Optional[str] = None
    file_size_in_bytes: int
    foreground_color: Optional[str] = None
    height: int
    image_position_info: Optional[str] = None
    image_purpose: str
    unscaled_image_sha256_hash: Optional[str] = Field(None, alias="UnscaledImageSHA256Hash")
    uri: str
    width: int


class Video(PascalCaseModel):
    uri: str
    video_purpose: str
    height: int
    width: int
    audio_encoding: str
    video_encoding: str
    video_position_info: str
    caption: str
    file_size_in_bytes: int
    preview_image: Image
    sort_order: int


class SearchTitle(PascalCaseModel):
    search_title_string: str
    search_title_type: str


class ContentRating(PascalCaseModel):
    rating_system: str
    rating_id: str
    rating_descriptors: List[str]
    rating_disclaimers: List
    interactive_elements: Optional[List] = None


class UsageData(PascalCaseModel):
    aggregate_time_span: str
    average_rating: float
    play_count: Optional[int] = None
    rating_count: int
    rental_count: Optional[str] = None
    trial_count: Optional[str] = None
    purchase_count: Optional[str] = None


class ProductProperties(PascalCaseModel):
    attributes: Optional[List] = None
    can_install_to_sd_card: Optional[bool] = Field(None, alias="CanInstallToSDCard")
    category: Optional[str] = None
    sub_category: Optional[str] = None
    categories: Optional[List[str]] = None
    extensions: Any = None
    is_accessible: Optional[bool] = None
    is_line_of_business_app: Optional[bool] = None
    is_published_to_legacy_windows_phone_store: Optional[bool] = None
    is_published_to_legacy_windows_store: Optional[bool] = None
    is_settings_app: Optional[bool] = None
    package_family_name: Optional[str] = None
    package_identity_name: Optional[str] = None
    publisher_certificate_name: Optional[str] = None
    publisher_id: str
    xbox_live_tier: Any = None
    xbox_xpa: Any = Field(None, alias="XboxXPA")
    xbox_cross_gen_set_id: Any = None
    xbox_console_gen_optimized: Any = None
    xbox_console_gen_compatible: Any = None
    xbox_live_gold_required: Optional[bool] = None
    ownership_type: Any = None
    pdp_background_color: Optional[str] = None
    has_add_ons: Optional[bool] = None
    revision_id: str
    product_group_id: Optional[str] = None
    product_group_name: Optional[str] = None


class AlternateId(PascalCaseModel):
    id_type: str
    value: str


class ValidationData(PascalCaseModel):
    passed_validation: bool
    revision_id: str
    validation_result_uri: Optional[str] = None


class FulfillmentData(PascalCaseModel):
    product_id: str
    wu_bundle_id: Optional[str] = None
    wu_category_id: str
    package_family_name: str
    sku_id: str
    content: Any = None
    package_features: Any = None


class HardwareProperties(PascalCaseModel):
    minimum_hardware: List
    recommended_hardware: List
    minimum_processor: Any = None
    recommended_processor: Any = None
    minimum_graphics: Any = None
    recommended_graphics: Any = None


class Application(PascalCaseModel):
    application_id: str
    declaration_order: int
    extensions: List[str]


class FrameworkDependency(PascalCaseModel):
    max_tested: int
    min_version: int
    package_identity: str


class PlatformDependency(PascalCaseModel):
    max_tested: Optional[int] = None
    min_version: Optional[int] = None
    platform_name: str


class Package(PascalCaseModel):
    applications: Optional[List[Application]] = None
    architectures: List[str]
    capabilities: Optional[List[str]] = None
    device_capabilities: Optional[List[str]] = None
    experience_ids: Optional[List] = None
    framework_dependencies: Optional[List[FrameworkDependency]] = None
    hardware_dependencies: Optional[List] = None
    hardware_requirements: Optional[List] = None
    hash: Optional[str] = None
    hash_algorithm: Optional[str] = None
    is_streaming_app: Optional[bool] = None
    languages: Optional[List[str]] = None
    max_download_size_in_bytes: int
    max_install_size_in_bytes: Optional[int] = None
    package_format: str
    package_family_name: Optional[str] = None
    main_package_family_name_for_dlc: Any = None
    package_full_name: Optional[str] = None
    package_id: str
    content_id: str
    key_id: Optional[str] = None
    package_rank: Optional[int] = None
    package_uri: Optional[str] = None
    platform_dependencies: Optional[List[PlatformDependency]] = None
    platform_dependency_xml_blob: Optional[str] = None
    resource_id: Optional[str] = None
    version: Optional[str] = None
    package_download_uris: Any = None
    driver_dependencies: Optional[List] = None
    fulfillment_data: Optional[FulfillmentData] = None


class LegalText(PascalCaseModel):
    additional_license_terms: str
    copyright: str
    copyright_uri: str
    privacy_policy: str
    privacy_policy_uri: str
    tou: str
    tou_uri: str


class SkuLocalizedProperty(PascalCaseModel):
    contributors: Optional[List] = None
    features: Optional[List] = None
    minimum_notes: Optional[str] = None
    recommended_notes: Optional[str] = None
    release_notes: Optional[str] = None
    display_platform_properties: Any = None
    sku_description: str
    sku_title: str
    sku_button_title: Optional[str] = None
    delivery_date_overlay: Any = None
    sku_display_rank: Optional[List] = None
    text_resources: Any = None
    images: Optional[List] = None
    legal_text: Optional[LegalText] = None
    language: str
    markets: List[str]


class SkuMarketProperty(PascalCaseModel):
    first_available_date: Optional[Union[datetime, str]] = None
    supported_languages: Optional[List[str]] = None
    package_ids: Any = None
    pi_filter: Any = Field(None, alias="PIFilter")
    markets: List[str]


class SkuProperties(PascalCaseModel):
    early_adopter_enrollment_url: Any = None
    fulfillment_data: Optional[FulfillmentData] = None
    fulfillment_type: Optional[str] = None
    fulfillment_plugin_id: Any = None
    has_third_party_iaps: Optional[bool] = Field(None, alias="HasThirdPartyIAPs")
    last_update_date: Optional[datetime] = None
    hardware_properties: Optional[HardwareProperties] = None
    hardware_requirements: Optional[List] = None
    hardware_warning_list: Optional[List] = None
    installation_terms: str
    packages: Optional[List[Package]] = None
    version_string: Optional[str] = None
    visible_to_b2b_service_ids: List = Field(alias="VisibleToB2BServiceIds")
    xbox_xpa: Optional[bool] = Field(None, alias="XboxXPA")
    bundled_skus: Optional[List] = None
    is_repurchasable: bool
    sku_display_rank: int
    display_physical_store_inventory: Any = None
    additional_identifiers: List
    is_trial: bool
    is_pre_order: bool
    is_bundle: bool

    @field_validator("last_update_date", mode="before", check_fields=True)
    def validator(x):
        return x or None

class Sku(PascalCaseModel):
    last_modified_date: datetime
    localized_properties: List[SkuLocalizedProperty]
    market_properties: List[SkuMarketProperty]
    product_id: str
    properties: SkuProperties
    sku_a_schema: str
    sku_b_schema: str
    sku_id: str
    sku_type: str
    recurrence_policy: Any = None
    subscription_policy_id: Any = None


class AllowedPlatform(PascalCaseModel):
    max_version: Optional[int] = None
    min_version: Optional[int] = None
    platform_name: str


class ClientConditions(PascalCaseModel):
    allowed_platforms: List[AllowedPlatform]


class Conditions(PascalCaseModel):
    client_conditions: ClientConditions
    end_date: datetime
    resource_set_ids: List[str]
    start_date: datetime


class PIFilter(PascalCaseModel):
    exclusion_properties: List
    inclusion_properties: List


class Price(PascalCaseModel):
    currency_code: str
    is_pi_required: bool = Field(alias="IsPIRequired")
    list_price: float
    msrp: float = Field(alias="MSRP")
    tax_type: str
    wholesale_currency_code: str


class OrderManagementData(PascalCaseModel):
    granted_entitlement_keys: Optional[List] = None
    pi_filter: Optional[PIFilter] = Field(None, alias="PIFilter")
    price: Price


class AvailabilityProperties(PascalCaseModel):
    original_release_date: Optional[datetime] = None


class SatisfyingEntitlementKey(PascalCaseModel):
    entitlement_keys: List[str]
    licensing_key_ids: List[str]


class LicensingData(PascalCaseModel):
    satisfying_entitlement_keys: List[SatisfyingEntitlementKey]


class Availability(PascalCaseModel):
    actions: List[str]
    availability_a_schema: Optional[str] = None
    availability_b_schema: Optional[str] = None
    availability_id: Optional[str] = None
    conditions: Optional[Conditions] = None
    last_modified_date: Optional[datetime] = None
    markets: Optional[List[str]] = None
    order_management_data: Optional[OrderManagementData] = None
    properties: Optional[AvailabilityProperties] = None
    sku_id: Optional[str] = None
    display_rank: Optional[int] = None
    remediation_required: Optional[bool] = None
    licensing_data: Optional[LicensingData] = None


class DisplaySkuAvailability(PascalCaseModel):
    sku: Optional[Sku] = None
    availabilities: List[Availability]


class LocalizedProperty(PascalCaseModel):
    developer_name: Optional[str] = None
    display_platform_properties: Optional[Any] = None
    publisher_name: Optional[str] = None
    publisher_website_uri: Optional[str] = None
    support_uri: Optional[str] = None
    eligibility_properties: Optional[Any] = None
    franchises: Optional[List] = None
    images: List[Image]
    videos: Optional[List[Video]] = None
    product_description: Optional[str] = None
    product_title: str
    short_title: Optional[str] = None
    sort_title: Optional[str] = None
    friendly_title: Optional[str] = None
    short_description: Optional[str] = None
    search_titles: Optional[List[SearchTitle]] = None
    voice_title: Optional[str] = None
    render_group_details: Optional[Any] = None
    product_display_ranks: Optional[List] = None
    interactive_model_config: Optional[Any] = None
    interactive_3d_enabled: Optional[bool] = Field(None, alias="Interactive3DEnabled")
    language: Optional[str] = None
    markets: Optional[List[str]] = None


class MarketProperty(PascalCaseModel):
    original_release_date: Optional[datetime] = None
    original_release_friendly_name: Optional[str] = None
    minimum_user_age: Optional[int] = None
    content_ratings: Optional[List[ContentRating]] = None
    related_products: Optional[List] = None
    usage_data: List[UsageData]
    bundle_config: Optional[Any] = None
    markets: Optional[List[str]] = None


class Product(PascalCaseModel):
    last_modified_date: Optional[datetime] = None
    localized_properties: List[LocalizedProperty]
    market_properties: List[MarketProperty]
    product_a_schema: Optional[str] = None
    product_b_schema: Optional[str] = None
    product_id: str
    properties: Optional[ProductProperties] = None
    alternate_ids: Optional[List[AlternateId]] = None
    domain_data_version: Optional[Any] = None
    ingestion_source: Optional[str] = None
    is_microsoft_product: Optional[bool] = None
    preferred_sku_id: Optional[str] = None
    product_type: Optional[str] = None
    validation_data: Optional[ValidationData] = None
    merchandizing_tags: Optional[List] = None
    part_d: Optional[str] = None
    product_family: str
    schema_version: Optional[str] = None
    product_kind: str
    display_sku_availabilities: List[DisplaySkuAvailability]


class CatalogResponse(PascalCaseModel):
    big_ids: Optional[List[str]] = None
    has_more_pages: Optional[bool] = None
    products: List[Product]
    total_result_count: Optional[int] = None


class SearchProduct(PascalCaseModel):
    background_color: Optional[str] = None
    height: Optional[int] = None
    image_type: Optional[str] = None
    width: Optional[int] = None
    platform_properties: List
    icon: Optional[str] = None
    product_id: str
    type: str
    title: str


class CatalogSearchResult(PascalCaseModel):
    product_family_name: str
    products: List[SearchProduct]


class CatalogSearchResponse(PascalCaseModel):
    results: List[CatalogSearchResult]
    total_result_count: int
