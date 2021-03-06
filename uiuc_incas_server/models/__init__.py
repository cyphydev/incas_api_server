# coding: utf-8

# flake8: noqa
"""
    INCAS TA2-UIUC Datatypes

    This API document is defined based on INCAS Common Datatypes version 0.0.7.  # noqa: E501

    OpenAPI spec version: 1.2.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

# import models into model package
from uiuc_incas_server.models.actor import Actor
from uiuc_incas_server.models.actor_actor_graph import ActorActorGraph
from uiuc_incas_server.models.actor_actor_graph_db import ActorActorGraphDB
from uiuc_incas_server.models.actor_batch_get_body import ActorBatchGetBody
from uiuc_incas_server.models.actor_id_response import ActorIdResponse
from uiuc_incas_server.models.actor_message_graph import ActorMessageGraph
from uiuc_incas_server.models.actor_message_graph_db import ActorMessageGraphDB
from uiuc_incas_server.models.actor_segment_collection import ActorSegmentCollection
from uiuc_incas_server.models.actor_segments_batch_delete_body import ActorSegmentsBatchDeleteBody
from uiuc_incas_server.models.actor_segments_batch_delete_validation_response import ActorSegmentsBatchDeleteValidationResponse
from uiuc_incas_server.models.actor_segments_batch_get_body import ActorSegmentsBatchGetBody
from uiuc_incas_server.models.actor_segments_batch_validation_response import ActorSegmentsBatchValidationResponse
from uiuc_incas_server.models.annotation import Annotation
from uiuc_incas_server.models.array_enrichment import ArrayEnrichment
from uiuc_incas_server.models.array_enrichment_meta import ArrayEnrichmentMeta
from uiuc_incas_server.models.base_enrichment import BaseEnrichment
from uiuc_incas_server.models.base_enrichment_meta import BaseEnrichmentMeta
from uiuc_incas_server.models.base_graph import BaseGraph
from uiuc_incas_server.models.category_enrichment import CategoryEnrichment
from uiuc_incas_server.models.category_enrichment_meta import CategoryEnrichmentMeta
from uiuc_incas_server.models.enrichment import Enrichment
from uiuc_incas_server.models.enrichment_meta import EnrichmentMeta
from uiuc_incas_server.models.enrichments_batch_delete_body import EnrichmentsBatchDeleteBody
from uiuc_incas_server.models.enrichments_batch_delete_validation_response import EnrichmentsBatchDeleteValidationResponse
from uiuc_incas_server.models.enrichments_batch_get_body import EnrichmentsBatchGetBody
from uiuc_incas_server.models.enrichments_batch_validation_response import EnrichmentsBatchValidationResponse
from uiuc_incas_server.models.extra_attribute import ExtraAttribute
from uiuc_incas_server.models.geo_location import GeoLocation
from uiuc_incas_server.models.graph_edge import GraphEdge
from uiuc_incas_server.models.links import Links
from uiuc_incas_server.models.list_enrichment import ListEnrichment
from uiuc_incas_server.models.list_enrichment_meta import ListEnrichmentMeta
from uiuc_incas_server.models.media_resource import MediaResource
from uiuc_incas_server.models.message import Message
from uiuc_incas_server.models.message_batch_get_body import MessageBatchGetBody
from uiuc_incas_server.models.message_id_response import MessageIdResponse
from uiuc_incas_server.models.message_message_graph import MessageMessageGraph
from uiuc_incas_server.models.message_message_graph_db import MessageMessageGraphDB
from uiuc_incas_server.models.numerical_enrichment import NumericalEnrichment
from uiuc_incas_server.models.numerical_enrichment_meta import NumericalEnrichmentMeta
from uiuc_incas_server.models.object_enrichment import ObjectEnrichment
from uiuc_incas_server.models.object_enrichment_meta import ObjectEnrichmentMeta
from uiuc_incas_server.models.offset import Offset
from uiuc_incas_server.models.one_of_enrichment import OneOfEnrichment
from uiuc_incas_server.models.one_of_enrichment_meta import OneOfEnrichmentMeta
from uiuc_incas_server.models.one_of_media_type_attributes import OneOfMediaTypeAttributes
from uiuc_incas_server.models.reddit_data import RedditData
from uiuc_incas_server.models.text_enrichment import TextEnrichment
from uiuc_incas_server.models.text_enrichment_meta import TextEnrichmentMeta
from uiuc_incas_server.models.twitter_data import TwitterData
from uiuc_incas_server.models.uiuc_actor import UiucActor
from uiuc_incas_server.models.uiuc_actor_db import UiucActorDB
from uiuc_incas_server.models.uiuc_message import UiucMessage
from uiuc_incas_server.models.uiuc_message_db import UiucMessageDB
from uiuc_incas_server.models.uiuc_segment import UiucSegment
from uiuc_incas_server.models.uiuc_segment_collection import UiucSegmentCollection
