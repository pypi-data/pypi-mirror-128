import json
import sys
from asyncio import Future
from time import time
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Sequence,
    Type,
    TypeVar,
    Union,
    cast,
)
from uuid import UUID, uuid4

from deprecated import deprecated
from ipywidgets import DOMWidget, Widget
from pydantic import parse_obj_as
from traitlets import Bool, Int, Unicode
from traitlets import Union as TraitletsUnion

from unfolded.map_sdk import models
from unfolded.map_sdk._frontend import module_name, module_version
from unfolded.map_sdk.environment import default_height
from unfolded.map_sdk.models import Action
from unfolded.map_sdk.poll import run_ui_poll_loop

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = ['UnfoldedMap', 'HTMLUnfoldedMap']

T = TypeVar('T')


class StoredFuture(TypedDict):
    """Shape of object stored in UnfoldedMap.futures"""

    future: Future
    response_callback: Callable[[Any], Optional[T]]


# Use total=False to mark keys as optional
class EventResponse(TypedDict, total=False):
    """Shape of object returned for event handling"""

    eventType: str
    data: Any


class MessageResponse(TypedDict, total=False):
    """Shape of object returned for messages"""

    messageId: str
    data: Any


class UnfoldedMap(DOMWidget):
    _model_name = Unicode('UnfoldedMapModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('UnfoldedMapView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    # TODO: support all of MapOptions arguments?
    mapUrl = Unicode('').tag(sync=True)
    mapUUID = Unicode('').tag(sync=True)
    width = TraitletsUnion(
        [Unicode(), Int()], allow_none=True, default_value='100%'
    ).tag(sync=True)
    height = TraitletsUnion(
        [Unicode(), Int()], allow_none=True, default_value=default_height()
    ).tag(sync=True)
    iframe = Bool(True).tag(sync=True)
    sdkUrl = Unicode('').tag(sync=True)
    _basemap_style = Unicode('').tag(sync=True)
    _identity_pool_id = Unicode('').tag(sync=True)

    def __init__(
        self,
        *,
        on_load: models.OnLoadHandlerType = None,
        on_timeline_interval_change: models.OnTimelineIntervalChangeHandlerType = None,
        on_layer_timeline_time_change: models.OnLayerTimelineTimeChangeHandlerType = None,
        on_filter: models.OnFilterHandlerType = None,
        _sync: bool = False,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)

        self._sync = _sync

        # Register callback for receiving messages
        self.on_msg(self._receive_message)

        # Mapping from message id to related future
        self.futures: Dict[str, StoredFuture] = {}
        self.map_event_handlers = models.MapEventHandlers(
            on_load=on_load,
            on_timeline_interval_change=on_timeline_interval_change,
            on_layer_timeline_time_change=on_layer_timeline_time_change,
            on_filter=on_filter,
        )

    def _send_and_wait_for_message(
        self,
        action: Action,
        response_class: Type[T],
    ) -> Optional[Union['Future[T]', T]]:
        """Send message to JS and optionally wait for response

        Args:
            action: Content of message to send to JS
            response_class: Pydantic class to be used for response

        Returns:
            if self._sync is True, returns an instance of T, otherwise returns a Future that resolves to an instance of T.
        """
        self._send_message(action)

        def response_callback(resp: Any) -> Optional[T]:
            if resp:
                try:
                    # parse_obj_as should work with any arbitrary pydantic-compatible
                    # types
                    # https://pydantic-docs.helpmanual.io/usage/models/#parsing-data-into-a-specified-type
                    return parse_obj_as(response_class, resp)
                except:
                    pass

            return None

        future: Future = Future()
        self.futures[str(action.message_id)] = {
            'future': future,
            'response_callback': response_callback,
        }

        if not self._sync:
            return future

        return self._wait_for_future(future)

    def _send_message(
        self, message: Action, buffers: Optional[Sequence[bytes]] = None
    ) -> None:
        """Send message to JS using Jupyter Widgets' messaging protocol

        Args:
            message: an instance of models.Action or of a subclass containing data that should be serialized and sent to the JS bindings.
            buffers: Binary buffers to send with message
        """
        # In order to properly serialize the Pydantic model to a dict, this
        # serializes to JSON and then loads it back as a dict. Currently,
        # exporting a Pydantic model to a dict does not make the contained
        # objects serializable. (https://stackoverflow.com/q/65622045). This
        # means that later calling `json.dumps` on this dict will fail.
        # On the other hand, ipywidgets requires dict input so it can do its own
        # JSON serialization.
        # https://github.com/jupyter-widgets/ipywidgets/blob/24628f006c8a468994eba7a6e964fe619c992267/ipywidgets/widgets/widget.py#L516-L526
        content = json.loads(message.json())

        # See definition of send here:
        # https://github.com/jupyter-widgets/ipywidgets/blob/c7bd32948ba677ab564e4cada84ca3306340c40e/ipywidgets/widgets/widget.py#L516-L526
        self.send(content, buffers)

    def _wait_for_future(self, future: 'Future[T]', timeout: float = 5) -> Optional[T]:
        """Wait in a blocking way for future to be completed

        Args:
            future: Future object to wait on
            timeout: Timeout period in seconds after which polling will finish

        Returns:
            None or result of future object
        """
        start_time = time()
        sentinel_object = object()

        def poll_callback():
            """Callback to be run in run_ui_poll_loop

            Polls for completion of future up to specified timeout
            """
            if future.done():
                # Returning None from the callback will not break out of the polling
                if future.result() is None:
                    return sentinel_object

                return future.result()

            if time() - start_time > timeout:
                # Return something other than None to break out of polling
                # We use a sentinel object so that it can't conflict with an actual
                # desired response
                # TODO: should we raise an exception here?
                return sentinel_object

            return None

        poll_response = run_ui_poll_loop(poll_callback, 1 / 10, 4)

        if poll_response is sentinel_object:
            return None

        return poll_response

    # TODO: check type of `buffers`
    def _receive_message(
        self, widget: Widget, content: Dict, buffers: List[bytes]
    ) -> None:
        """Receive message from JS"""
        # pylint:disable=unused-argument
        if 'eventType' in content:
            return self._receive_message_event(cast(EventResponse, content))

        if 'messageId' in content:
            return self._receive_message_response(cast(MessageResponse, content))

    def _receive_message_response(self, content: MessageResponse) -> None:
        """Receive response message from JS"""
        message_id = content.get('messageId')
        data = content.get('data')

        if not message_id or message_id not in self.futures:
            return

        future_ref = self.futures.pop(message_id)
        response_callback = future_ref['response_callback']
        future_ref['future'].set_result(response_callback(data))

    def _receive_message_event(self, content: EventResponse) -> None:
        """Receive event notification from JS"""
        event_type = content.get('eventType')
        if not event_type:
            return

        data = content.get('data')
        callback = getattr(self.map_event_handlers, event_type)

        if callback and data is not None:
            callback(data)

    # PUBLIC MAP METHODS
    @staticmethod
    def get_map_url(map_uuid: Union[UUID, str]) -> str:
        """Get the full URL for the published map

        Args:
            map_uuid - Universally unique identifier (UUID) for the published map

        Returns:
            (string): Full URL for the published map
        """
        return f'https://studio.unfolded.ai/public/{map_uuid}'

    def set_view_state(
        self, view_state: models.ViewState
    ) -> Union['Future[models.ViewState]', models.ViewState]:
        """Set the map view state

        Args:
            view_state: ViewState model instance or dict with `longitude`, `latitude`, and `zoom` keys.
        """
        action = models.SetViewState(view_state=view_state)
        return self._send_and_wait_for_message(
            action=action, response_class=models.ViewState
        )

    def get_layers(
        self,
    ) -> Optional[Union['Future[List[models.Layer]]', List[models.Layer]]]:
        """Get all layers for the provided map instance"""
        action = models.GetLayers()
        return self._send_and_wait_for_message(
            action=action, response_class=List[models.Layer]
        )

    def set_layer_visibility(
        self, layer_id: str, is_visible: bool
    ) -> Union['Future[models.Layer]', models.Layer]:
        """Set visibility of specified layer

        Args:
            layer_id: layer id
            is_visible: If True, make layer visible, else hide the layer
        """
        action = models.SetLayerVisibility(layer_id=layer_id, is_visible=is_visible)
        return self._send_and_wait_for_message(
            action=action, response_class=models.Layer
        )

    def set_theme(self, theme: str) -> Optional[Union['Future[str]', str]]:
        """Set the map theme to 'light' or 'dark'

        Args:
            theme: theme name, either 'light' or 'dark'
        """
        action = models.SetTheme(theme=theme)
        return self._send_and_wait_for_message(action=action, response_class=str)

    def get_timeline_info(
        self, idx: str
    ) -> Union['Future[models.TimelineInfo]', models.TimelineInfo]:
        """Get information object for the timeline filter

        Args:
            idx: Index of the timeline filter
        """
        action = models.GetTimelineInfo(idx=idx)
        return self._send_and_wait_for_message(
            action=action, response_class=models.TimelineInfo
        )

    @deprecated(reason="Use `setTimelineConfig` instead")
    def toggle_timeline_animation(self, idx: str) -> None:
        """Toggle timeline filter animation

        Args:
            idx: Index of the timeline filter
        """
        action = models.ToggleTimelineAnimation(idx=idx)
        self._send_message(action)

    @deprecated(reason="Use `setTimelineConfig` instead")
    def toggle_timeline_visibility(self, idx: str) -> None:
        """Toggle timeline filter visibility

        Args:
            idx: Index of the timeline filter
        """
        action = models.ToggleTimelineVisibility(idx=idx)
        self._send_message(action)

    @deprecated(reason="Use `setTimelineConfig` instead")
    def set_timeline_interval(
        self, idx: str, start_time: float, end_time: float
    ) -> None:
        """Set current timeline filter interval

        Args:
            idx: Index of the timeline filter
            start_time: Unix Time in milliseconds for the start of the interval
            end_time: Unix Time in milliseconds for the end of the interval
        """
        action = models.SetTimelineInterval(
            idx=idx, start_time=start_time, end_time=end_time
        )
        self._send_message(action)

    @deprecated(reason="Use `setTimelineConfig` instead")
    def set_timeline_animation_speed(self, idx: str, speed: float) -> None:
        """Set current time filter animation speed

        Args:
            idx: Index of the timeline filter
            speed: speed multiplier
        """
        action = models.SetTimelineAnimationSpeed(idx=idx, speed=speed)
        self._send_message(action)

    def set_timeline_config(
        self, config: models.TimelineConfig
    ) -> Union['Future[models.TimelineConfig]', models.TimelineConfig]:
        """Set timeline configuration

        Args:
            config: Timeline configuration object
        """
        action = models.SetTimelineConfig(config=config)
        return self._send_and_wait_for_message(
            action=action,
            response_class=models.TimelineConfig,
        )

    def refresh_map_data(self) -> Optional[Union['Future[bool]', bool]]:
        """Refresh map data sources"""
        action = models.RefreshMapData()
        return self._send_and_wait_for_message(
            action=action,
            response_class=bool,
        )

    def get_layer_timeline_info(
        self,
    ) -> Union['Future[models.LayerTimelineInfo]', models.LayerTimelineInfo]:
        """Get information object for the layer timeline control"""
        action = models.GetLayerTimelineInfo()
        return self._send_and_wait_for_message(
            action=action,
            response_class=models.LayerTimelineInfo,
        )

    def set_layer_timeline_config(
        self, config: models.LayerTimelineConfig
    ) -> Union['Future[models.LayerTimelineConfig]', models.LayerTimelineConfig]:
        """Set layer timeline configuration

        Args:
            config: Layer timeline configuration object
        """
        action = models.SetLayerTimelineConfig(config=config)
        return self._send_and_wait_for_message(
            action=action,
            response_class=models.LayerTimelineConfig,
        )

    def _add_tileset(
        self, tileset: models.Tileset
    ) -> Optional[Union['Future[bool]', bool]]:
        """Create a new tileset

        Args:
            tileset: tileset configuration
        """
        action = models.AddTileset(tileset=tileset)
        return self._send_and_wait_for_message(
            action=action,
            response_class=bool,
        )

    def add_dataset(
        self, dataset: Union[UUID, str, models.Dataset], auto_create_layers: bool = True
    ) -> Optional[Union['Future[bool]', bool]]:
        """Add a dataset to the map.

        If a dataset with data is provided, a new dataset will be created and added to the map (but not uploaded to Studio).
        Alternatively, if just a uuid is provided or a Dataset with no data specified in it, the method will attempt to add
        a previously uploaded dataset with the specified uuid to the map.

        Args:
            dataset: Dataset for creating and adding a new dataset to the map or a uuid of a previously uploaded dataset.
            auto_create_layers: When `True` Studio will attempt to create layers automatically
        """
        if isinstance(dataset, UUID) or isinstance(dataset, str):
            dataset = models.Dataset(uuid=dataset)

        action = models.AddDataset(
            dataset=dataset, auto_create_layers=auto_create_layers
        )

        return self._send_and_wait_for_message(
            action=action,
            response_class=bool,
        )

    def remove_dataset(self, uuid: UUID) -> Optional[Union['Future[bool]', bool]]:
        """Remove the dataset with the specified UUID from the map.

        Args:
            uuid: Dataset UUID
        """
        action = models.RemoveDataset(uuid=uuid)
        return self._send_and_wait_for_message(
            action=action,
            response_class=bool,
        )

    def get_map_config(
        self,
    ) -> Optional[Union['Future[models.MapConfig]', models.MapConfig]]:
        """Get map configuration object"""
        action = models.GetMapConfig()
        return self._send_and_wait_for_message(
            action=action, response_class=models.MapConfig
        )

    def set_map_config(
        self, map_config: models.MapConfig
    ) -> Optional[Union['Future[bool]', bool]]:
        """Set map configuration

        Args:
            map_config: Map Configuration to set
        """
        action = models.SetMapConfig(map_config=map_config)
        return self._send_and_wait_for_message(
            action=action,
            response_class=bool,
        )

    def add_layer(
        self, layer: models.LayerSpec
    ) -> Optional[Union['Future[bool]', bool]]:
        """Add a layer to the map

        Args:
            layer: Layer configuration
        """
        action = models.AddLayer(layer=layer)
        return self._send_and_wait_for_message(
            action=action,
            response_class=bool,
        )

    def remove_layer(self, layer_id: str) -> Optional[Union['Future[bool]', bool]]:
        """Remove layer from the map

        Args:
            id: Layer id
        """
        action = models.RemoveLayer(id=layer_id)
        return self._send_and_wait_for_message(
            action=action,
            response_class=bool,
        )

    def set_filter(
        self, info: models.FilterInfo
    ) -> Optional[Union['Future[bool]', bool]]:
        """Set filter value

        Args:
            info: Filter info to set
        """
        action = models.SetFilter(info=info)
        return self._send_and_wait_for_message(
            action=action,
            response_class=bool,
        )

    def remove_filter(self, filter_id: str) -> Optional[Union['Future[bool]', bool]]:
        """Remove filter from the map

        Args:
            id: Filter id
        """
        action = models.RemoveFilter(id=filter_id)
        return self._send_and_wait_for_message(
            action=action,
            response_class=bool,
        )

    def set_map_event_handlers(
        self, event_handlers: Optional[models.MapEventHandlers]
    ) -> None:
        """Sets event handlers for the specified map to get notifications.

        Only one event handler per message type can be registered, so subsequent calls
        will override previously set event handler for the specified message types. This
        method only updates callbacks for those message types which are passed. The
        others will remain unchanged. Set specific event handlers to None to unregister
        them, or pass None to the method to remove all handlers.

        Args:
            map_event_handlers: MapEventHandlers
        """
        if event_handlers is None:
            self.map_event_handlers = models.MapEventHandlers()
        else:
            update = (
                event_handlers.dict()
                if isinstance(event_handlers, models.MapEventHandlers)
                else event_handlers
            )
            self.map_event_handlers = self.map_event_handlers.copy(update=update)


class HTMLUnfoldedMap(UnfoldedMap):
    datasets: List[models.Dataset]
    layers: List[models.LayerSpec]
    filters: List[models.FilterInfo]
    map_config: Optional[models.MapConfig]

    def __init__(
        self,
        *,
        datasets: Sequence[Union[models.Dataset, Dict]] = (),
        layers: Sequence[Union[models.LayerSpec, Dict]] = (),
        filters: Sequence[Union[models.FilterInfo, Dict]] = (),
        map_config: Optional[Union[models.MapConfig, Dict]] = None,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)

        dataset_models: List[models.Dataset] = [
            models.Dataset(**dataset)
            if not isinstance(dataset, models.Dataset)
            else dataset
            for dataset in datasets
        ]
        layer_models = [
            models.LayerSpec(**layer)
            if not isinstance(layer, models.LayerSpec)
            else layer
            for layer in layers
        ]
        filter_models = [
            models.FilterInfo(**filter_)
            if not isinstance(filter_, models.FilterInfo)
            else filter_
            for filter_ in filters
        ]

        if map_config and not isinstance(map_config, models.MapConfig):
            map_config = models.MapConfig(**map_config)

        self.datasets = dataset_models
        self.layers = layer_models
        self.filters = filter_models
        self.map_config = map_config

    def _repr_html_(self):
        # Per-iframe identifier
        frame_uuid = uuid4()
        if self.mapUrl:
            url = self.mapUrl
        elif self.mapUUID:
            url = 'https://studio.unfolded.ai/map/' + self.mapUUID
        else:
            url = 'https://studio.unfolded.ai/incognito'

        # NOTE: in f-strings, double quotes '{{' and '}}' resolve to a literal '{', '}'
        # Begin script
        html = f"""
        <script>(function() {{
        var frame;
        var queue = [];
        var lastSentType;
        window.addEventListener('message', function(evt) {{
          var data = `${{evt.data}}`;
          if (data.indexOf('map-sdk-initialized-response') >= 0) onInit();
          if (lastSentType && data.indexOf(`${{lastSentType}}-response` >= 0)) sendNext();
        }});
        function onInit() {{
          frame = document.getElementById('{frame_uuid}');
        """

        # Add datasets
        html += self._repr_html_datasets()

        # Add layers
        html += self._repr_html_layers()

        # Add filters
        html += self._repr_html_filters()

        # Add map config
        html += self._repr_html_map_config()

        # End script
        html += """
            sendNext();
        }
        function sendNext() {
          if (queue.length === 0) {
            lastSentType = null;
            return;
          }
          var msg = queue.shift();
          if (frame) {
              frame.contentWindow.postMessage(JSON.stringify(msg), '*');
              lastSentType = msg.type;
          }
        }
        })();</script>
        """

        # The default 100% height leads to the iframe height
        # growing infinitely in Databricks due to their resizing logic
        height = self.height
        try:
            int(self.height)
        except ValueError:
            height = 500

        iframe_tag = f"""
        <iframe id="{frame_uuid}" src="{url}" width="{self.width}" height="{height}" />
        """

        return html + iframe_tag

    def _repr_html_datasets(self) -> str:
        """Helper to create HTML representation of self.datasets"""
        if not self.datasets:
            return ''

        template_str = """
          queue.push({{
            type: 'map-sdk-add-dataset-to-map',
            source: 'unfolded-sdk-client',
            data: {{ autoCreateLayers: {auto_layers}, dataset: {dataset} }}
          }});
        """
        auto_layers = 'false' if self.layers or self.map_config else 'true'

        encoded = [
            template_str.format(
                auto_layers=auto_layers, dataset=dataset.json(by_alias=True)
            )
            for dataset in self.datasets
        ]
        return '\n'.join(encoded)

    def _repr_html_layers(self) -> str:
        """Helper to create HTML representation of self.layers"""
        if not self.layers:
            return ''

        template_str = """
          queue.push({{
            type: 'map-sdk-add-layer',
            source: 'unfolded-sdk-client',
            data: {{layer: {layer}}}
          }});
        """
        encoded = [
            template_str.format(layer=layer.json(by_alias=True))
            for layer in self.layers
        ]
        return '\n'.join(encoded)

    def _repr_html_filters(self) -> str:
        """Helper to create HTML representation of self.filters"""
        if not self.filters:
            return ''

        template_str = """
          queue.push({{
            type: 'map-sdk-set-filter',
            source: 'unfolded-sdk-client',
            data: {{info: {filter}}}
          }});
        """
        encoded = [
            template_str.format(filter=filter_.json(by_alias=True))
            for filter_ in self.filters
        ]
        return '\n'.join(encoded)

    def _repr_html_map_config(self) -> str:
        """Helper to create HTML representation of self.map_config"""
        if not self.map_config:
            return ''

        template_str = """
          queue.push({{
            type: 'map-sdk-set-map-config',
            source: 'unfolded-sdk-client',
            data: {{mapConfig: {map_config}}}
          }});
        """
        return template_str.format(map_config=self.map_config.json(by_alias=True))
