# coding: utf-8

# flake8: noqa
"""
    INCAS TA2-UIUC Datatypes

    This API document is defined based on INCAS Common Datatypes version 0.0.3.  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

# import models into model package
from uiuc_incas_server.models.actor import Actor
from uiuc_incas_server.models.actor_actor_graph import ActorActorGraph
from uiuc_incas_server.models.actor_actor_graph_db import ActorActorGraphDB
from uiuc_incas_server.models.actor_batch_get_body import ActorBatchGetBody
from uiuc_incas_server.models.actor_enrichment import ActorEnrichment
from uiuc_incas_server.models.actor_enrichment_meta import ActorEnrichmentMeta
from uiuc_incas_server.models.actor_enrichments_batch_delete_body import ActorEnrichmentsBatchDeleteBody
from uiuc_incas_server.models.actor_enrichments_batch_get_body import ActorEnrichmentsBatchGetBody
from uiuc_incas_server.models.actor_message_edge import ActorMessageEdge
from uiuc_incas_server.models.actor_message_graph import ActorMessageGraph
from uiuc_incas_server.models.actor_message_graph_db import ActorMessageGraphDB
from uiuc_incas_server.models.actor_to_actor_edge import ActorToActorEdge
from uiuc_incas_server.models.actor_to_message_edge import ActorToMessageEdge
from uiuc_incas_server.models.annotation import Annotation
from uiuc_incas_server.models.array_actor_enrichment import ArrayActorEnrichment
from uiuc_incas_server.models.array_actor_enrichment_meta import ArrayActorEnrichmentMeta
from uiuc_incas_server.models.array_message_enrichment import ArrayMessageEnrichment
from uiuc_incas_server.models.array_message_enrichment_meta import ArrayMessageEnrichmentMeta
from uiuc_incas_server.models.base_actor_enrichment import BaseActorEnrichment
from uiuc_incas_server.models.base_actor_enrichment_meta import BaseActorEnrichmentMeta
from uiuc_incas_server.models.base_edge import BaseEdge
from uiuc_incas_server.models.base_graph import BaseGraph
from uiuc_incas_server.models.base_message_enrichment import BaseMessageEnrichment
from uiuc_incas_server.models.base_message_enrichment_meta import BaseMessageEnrichmentMeta
from uiuc_incas_server.models.category_actor_enrichment import CategoryActorEnrichment
from uiuc_incas_server.models.category_actor_enrichment_meta import CategoryActorEnrichmentMeta
from uiuc_incas_server.models.category_message_enrichment import CategoryMessageEnrichment
from uiuc_incas_server.models.category_message_enrichment_meta import CategoryMessageEnrichmentMeta
from uiuc_incas_server.models.extra_attribute import ExtraAttribute
from uiuc_incas_server.models.extra_attributes import ExtraAttributes
from uiuc_incas_server.models.geo_location import GeoLocation
from uiuc_incas_server.models.links import Links
from uiuc_incas_server.models.media_resource import MediaResource
from uiuc_incas_server.models.message import Message
from uiuc_incas_server.models.message_batch_get_body import MessageBatchGetBody
from uiuc_incas_server.models.message_enrichment import MessageEnrichment
from uiuc_incas_server.models.message_enrichment_meta import MessageEnrichmentMeta
from uiuc_incas_server.models.message_enrichments_batch_delete_body import MessageEnrichmentsBatchDeleteBody
from uiuc_incas_server.models.message_enrichments_batch_get_body import MessageEnrichmentsBatchGetBody
from uiuc_incas_server.models.message_message_graph import MessageMessageGraph
from uiuc_incas_server.models.message_message_graph_db import MessageMessageGraphDB
from uiuc_incas_server.models.message_to_actor_edge import MessageToActorEdge
from uiuc_incas_server.models.message_to_message_edge import MessageToMessageEdge
from uiuc_incas_server.models.numerical_actor_enrichment import NumericalActorEnrichment
from uiuc_incas_server.models.numerical_actor_enrichment_meta import NumericalActorEnrichmentMeta
from uiuc_incas_server.models.numerical_message_enrichment import NumericalMessageEnrichment
from uiuc_incas_server.models.numerical_message_enrichment_meta import NumericalMessageEnrichmentMeta
from uiuc_incas_server.models.offset import Offset
from uiuc_incas_server.models.one_of_actor_enrichment import OneOfActorEnrichment
from uiuc_incas_server.models.one_of_actor_enrichment_meta import OneOfActorEnrichmentMeta
from uiuc_incas_server.models.one_of_actor_message_edge import OneOfActorMessageEdge
from uiuc_incas_server.models.one_of_media_type_attributes import OneOfMediaTypeAttributes
from uiuc_incas_server.models.one_of_message_enrichment import OneOfMessageEnrichment
from uiuc_incas_server.models.one_of_message_enrichment_meta import OneOfMessageEnrichmentMeta
from uiuc_incas_server.models.reddit_data import RedditData
from uiuc_incas_server.models.response import Response
from uiuc_incas_server.models.text_actor_enrichment import TextActorEnrichment
from uiuc_incas_server.models.text_actor_enrichment_meta import TextActorEnrichmentMeta
from uiuc_incas_server.models.text_message_enrichment import TextMessageEnrichment
from uiuc_incas_server.models.text_message_enrichment_meta import TextMessageEnrichmentMeta
from uiuc_incas_server.models.twitter_data import TwitterData
from uiuc_incas_server.models.uiuc_actor import UiucActor
from uiuc_incas_server.models.uiuc_actor_db import UiucActorDB
from uiuc_incas_server.models.uiuc_message import UiucMessage
from uiuc_incas_server.models.uiuc_message_db import UiucMessageDB
from uiuc_incas_server.models.uiuc_segment import UiucSegment
