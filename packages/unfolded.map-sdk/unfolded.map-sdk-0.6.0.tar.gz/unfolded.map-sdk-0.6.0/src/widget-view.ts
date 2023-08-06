import { DOMWidgetView } from '@jupyter-widgets/base';

import '../css/widget.css';
import { MapInterface, UnfoldedMap } from '@unfolded/map-sdk';
import { UnfoldedMapModel } from './widget-model';
import { loadScript } from './utils/script-utils';
import { createAwsBasemap } from './utils/aws-location-utils';

const WIDGET_CSS_CLASS = 'unfolded-widget';
const STUDIO_URL = 'https://studio.unfolded.ai';

const importLocalUnfoldedMap = async (
  studioUrl: string
): Promise<MapInterface | undefined> => {
  // @ts-expect-error No types on globalThis
  const _get = () => globalThis.Unfolded?.LocalUnfoldedMap;
  let LocalUnfoldedMap = _get();
  if (!LocalUnfoldedMap) {
    // Try to load the studio bundle and get access to `LocalUnfoldedMap`
    try {
      await loadScript(`${studioUrl || STUDIO_URL}/studio-bundle.js`);
      LocalUnfoldedMap = _get();
    } catch (err) {
      console.error('Could not load Studio bundle', err);
    }
  }
  return LocalUnfoldedMap;
};

export class UnfoldedMapView extends DOMWidgetView {
  async initialize() {
    const width = this.model.get('width');
    const height = this.model.get('height');
    const mapUUID = this.model.get('mapUUID');
    const mapUrl = this.model.get('mapUrl');
    const shouldUseIframe = this.model.get('iframe');
    const studioUrl = this.model.get('sdkUrl');

    let map: MapInterface | undefined;
    if (!shouldUseIframe) {
      const basemapStyle = this.model.get('_basemap_style');
      const identityPoolId = this.model.get('_identity_pool_id');

      let mapOptions = {};
      if (basemapStyle && identityPoolId) {
        const { transformRequest, initialState } = await createAwsBasemap({
          basemapStyle,
          identityPoolId,
        });
        mapOptions = { _transformRequest: transformRequest, initialState };
      }

      const LocalUnfoldedMap = await importLocalUnfoldedMap(studioUrl);
      // Try to create a local map
      if (LocalUnfoldedMap) {
        // @ts-expect-error No types on globalThis
        map = new LocalUnfoldedMap({
          mapUUID,
          width,
          height,
          onLoad: (this.model as UnfoldedMapModel).onMapLoaded,
          ...mapOptions,
        });
      }
    }

    // Fall back to a traditional iframe map
    if (!map) {
      map = new UnfoldedMap({
        mapUUID,
        mapUrl,
        appendToDocument: false,
        width,
        height,
        embed: true,
        onLoad: (this.model as UnfoldedMapModel).onMapLoaded,
      });
    }

    this.model.set('map', map);
    this.model.save_changes();

    // Make sure to render since we are doing async loading
    this.render();
  }

  render() {
    if (this.el.classList.contains(WIDGET_CSS_CLASS)) {
      // Map has already been rendered, make sure that we only render once
      return;
    }
    const map: MapInterface = this.model.get('map');
    if (map) {
      // Rendering the map
      this.el.classList.add(WIDGET_CSS_CLASS);
      map.render(this.el);
    } else {
      // Map hasn't been initialized yet, skipping
    }
  }
}
