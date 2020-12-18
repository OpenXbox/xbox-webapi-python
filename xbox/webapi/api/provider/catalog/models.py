from datetime import datetime
from enum import Enum
from typing import Any, List, Optional, Union

from pydantic import Field, validator

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
    file_id: Optional[str]
    eis_listing_identifier: Any = Field(alias="EISListingIdentifier")
    background_color: Optional[str]
    caption: Optional[str]
    file_size_in_bytes: int
    foreground_color: Optional[str]
    height: int
    image_position_info: Optional[str]
    image_purpose: str
    unscaled_image_sha256_hash: Optional[str] = Field(alias="UnscaledImageSHA256Hash")
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
    interactive_elements: Optional[List]


class UsageData(PascalCaseModel):
    aggregate_time_span: str
    average_rating: float
    play_count: Optional[int]
    rating_count: int
    rental_count: Optional[str]
    trial_count: Optional[str]
    purchase_count: Optional[str]


class ProductProperties(PascalCaseModel):
    attributes: Optional[List]
    can_install_to_sd_card: Optional[bool] = Field(alias="CanInstallToSDCard")
    category: Optional[str]
    sub_category: Optional[str]
    categories: Optional[List[str]]
    extensions: Any
    is_accessible: Optional[bool]
    is_line_of_business_app: Optional[bool]
    is_published_to_legacy_windows_phone_store: Optional[bool]
    is_published_to_legacy_windows_store: Optional[bool]
    is_settings_app: Optional[bool]
    package_family_name: Optional[str]
    package_identity_name: Optional[str]
    publisher_certificate_name: Optional[str]
    publisher_id: str
    xbox_live_tier: Any
    xbox_xpa: Any = Field(alias="XboxXPA")
    xbox_cross_gen_set_id: Any
    xbox_console_gen_optimized: Any
    xbox_console_gen_compatible: Any
    xbox_live_gold_required: Optional[bool]
    ownership_type: Any
    pdp_background_color: Optional[str]
    has_add_ons: Optional[bool]
    revision_id: str
    product_group_id: Optional[str]
    product_group_name: Optional[str]


class AlternateId(PascalCaseModel):
    id_type: str
    value: str


class ValidationData(PascalCaseModel):
    passed_validation: bool
    revision_id: str
    validation_result_uri: Optional[str]


class FulfillmentData(PascalCaseModel):
    product_id: str
    wu_bundle_id: Optional[str]
    wu_category_id: str
    package_family_name: str
    sku_id: str
    content: Any
    package_features: Any


class HardwareProperties(PascalCaseModel):
    minimum_hardware: List
    recommended_hardware: List
    minimum_processor: Any
    recommended_processor: Any
    minimum_graphics: Any
    recommended_graphics: Any


class Application(PascalCaseModel):
    application_id: str
    declaration_order: int
    extensions: List[str]


class FrameworkDependency(PascalCaseModel):
    max_tested: int
    min_version: int
    package_identity: str


class PlatformDependency(PascalCaseModel):
    max_tested: Optional[int]
    min_version: Optional[int]
    platform_name: str


class Package(PascalCaseModel):
    applications: Optional[List[Application]]
    architectures: List[str]
    capabilities: Optional[List[str]]
    device_capabilities: Optional[List[str]]
    experience_ids: Optional[List]
    framework_dependencies: Optional[List[FrameworkDependency]]
    hardware_dependencies: Optional[List]
    hardware_requirements: Optional[List]
    hash: Optional[str]
    hash_algorithm: Optional[str]
    is_streaming_app: Optional[bool]
    languages: Optional[List[str]]
    max_download_size_in_bytes: int
    max_install_size_in_bytes: Optional[int]
    package_format: str
    package_family_name: Optional[str]
    main_package_family_name_for_dlc: Any
    package_full_name: Optional[str]
    package_id: str
    content_id: str
    key_id: Optional[str]
    package_rank: Optional[int]
    package_uri: Optional[str]
    platform_dependencies: Optional[List[PlatformDependency]]
    platform_dependency_xml_blob: Optional[str]
    resource_id: Optional[str]
    version: Optional[str]
    package_download_uris: Any
    driver_dependencies: Optional[List]
    fulfillment_data: Optional[FulfillmentData]


class LegalText(PascalCaseModel):
    additional_license_terms: str
    copyright: str
    copyright_uri: str
    privacy_policy: str
    privacy_policy_uri: str
    tou: str
    tou_uri: str


class SkuLocalizedProperty(PascalCaseModel):
    contributors: Optional[List]
    features: Optional[List]
    minimum_notes: Optional[str]
    recommended_notes: Optional[str]
    release_notes: Optional[str]
    display_platform_properties: Any
    sku_description: str
    sku_title: str
    sku_button_title: Optional[str]
    delivery_date_overlay: Any
    sku_display_rank: Optional[List]
    text_resources: Any
    images: Optional[List]
    legal_text: Optional[LegalText]
    language: str
    markets: List[str]


class SkuMarketProperty(PascalCaseModel):
    first_available_date: Optional[Union[datetime, str]]
    supported_languages: Optional[List[str]]
    package_ids: Any
    pi_filter: Any = Field(alias="PIFilter")
    markets: List[str]


class SkuProperties(PascalCaseModel):
    early_adopter_enrollment_url: Any
    fulfillment_data: Optional[FulfillmentData]
    fulfillment_type: Optional[str]
    fulfillment_plugin_id: Any
    has_third_party_iaps: Optional[bool] = Field(alias="HasThirdPartyIAPs")
    last_update_date: Optional[datetime]
    hardware_properties: Optional[HardwareProperties]
    hardware_requirements: Optional[List]
    hardware_warning_list: Optional[List]
    installation_terms: str
    packages: Optional[List[Package]]
    version_string: Optional[str]
    visible_to_b2b_service_ids: List = Field(alias="VisibleToB2BServiceIds")
    xbox_xpa: Optional[bool] = Field(alias="XboxXPA")
    bundled_skus: Optional[List]
    is_repurchasable: bool
    sku_display_rank: int
    display_physical_store_inventory: Any
    additional_identifiers: List
    is_trial: bool
    is_pre_order: bool
    is_bundle: bool

    @validator("last_update_date", pre=True, always=True)
    def set_to_none(cls, v):
        return v or None


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
    recurrence_policy: Any
    subscription_policy_id: Any


class AllowedPlatform(PascalCaseModel):
    max_version: Optional[int]
    min_version: Optional[int]
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
    granted_entitlement_keys: Optional[List]
    pi_filter: Optional[PIFilter] = Field(None, alias="PIFilter")
    price: Price


class AvailabilityProperties(PascalCaseModel):
    original_release_date: Optional[datetime]


class SatisfyingEntitlementKey(PascalCaseModel):
    entitlement_keys: List[str]
    licensing_key_ids: List[str]


class LicensingData(PascalCaseModel):
    satisfying_entitlement_keys: List[SatisfyingEntitlementKey]


class Availability(PascalCaseModel):
    actions: List[str]
    availability_a_schema: Optional[str]
    availability_b_schema: Optional[str]
    availability_id: Optional[str]
    conditions: Optional[Conditions]
    last_modified_date: Optional[datetime]
    markets: Optional[List[str]]
    order_management_data: Optional[OrderManagementData]
    properties: Optional[AvailabilityProperties]
    sku_id: Optional[str]
    display_rank: Optional[int]
    remediation_required: Optional[bool]
    licensing_data: Optional[LicensingData]


class DisplaySkuAvailability(PascalCaseModel):
    sku: Optional[Sku]
    availabilities: List[Availability]


class LocalizedProperty(PascalCaseModel):
    developer_name: Optional[str]
    display_platform_properties: Optional[Any]
    publisher_name: Optional[str]
    publisher_website_uri: Optional[str]
    support_uri: Optional[str]
    eligibility_properties: Optional[Any]
    franchises: Optional[List]
    images: List[Image]
    videos: Optional[List[Video]]
    product_description: Optional[str]
    product_title: str
    short_title: Optional[str]
    sort_title: Optional[str]
    friendly_title: Optional[str]
    short_description: Optional[str]
    search_titles: Optional[List[SearchTitle]]
    voice_title: Optional[str]
    render_group_details: Optional[Any]
    product_display_ranks: Optional[List]
    interactive_model_config: Optional[Any]
    interactive_3d_enabled: Optional[bool] = Field(alias="Interactive3DEnabled")
    language: Optional[str]
    markets: Optional[List[str]]


class MarketProperty(PascalCaseModel):
    original_release_date: Optional[datetime]
    original_release_friendly_name: Optional[str]
    minimum_user_age: Optional[int]
    content_ratings: Optional[List[ContentRating]]
    related_products: Optional[List]
    usage_data: List[UsageData]
    bundle_config: Optional[Any]
    markets: Optional[List[str]]


class Product(PascalCaseModel):
    last_modified_date: Optional[datetime]
    localized_properties: List[LocalizedProperty]
    market_properties: List[MarketProperty]
    product_a_schema: Optional[str]
    product_b_schema: Optional[str]
    product_id: str
    properties: Optional[ProductProperties]
    alternate_ids: Optional[List[AlternateId]]
    domain_data_version: Optional[Any]
    ingestion_source: Optional[str]
    is_microsoft_product: Optional[bool]
    preferred_sku_id: Optional[str]
    product_type: Optional[str]
    validation_data: Optional[ValidationData]
    merchandizing_tags: Optional[List]
    part_d: Optional[str]
    product_family: str
    schema_version: Optional[str]
    product_kind: str
    display_sku_availabilities: List[DisplaySkuAvailability]


class CatalogResponse(PascalCaseModel):
    big_ids: Optional[List[str]]
    has_more_pages: Optional[bool]
    products: List[Product]
    total_result_count: Optional[int]


class SearchProduct(PascalCaseModel):
    background_color: Optional[str]
    height: Optional[int]
    image_type: Optional[str]
    width: Optional[int]
    platform_properties: List
    icon: Optional[str]
    product_id: str
    type: str
    title: str


class CatalogSearchResult(PascalCaseModel):
    product_family_name: str
    products: List[SearchProduct]


class CatalogSearchResponse(PascalCaseModel):
    results: List[CatalogSearchResult]
    total_result_count: int
