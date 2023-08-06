import { Widget } from '@lumino/widgets';
import { IRenderMime } from '@jupyterlab/rendermime-interfaces';
import { UnfoldedMap } from '@unfolded/map-sdk';

/**
 * The CSS class to add to the Unfolded Map Widget.
 */
const CSS_CLASS = 'unfolded-rendermime';

/**
 * The MIME type for GeoJSON data
 */
const GEOJSON_MIME_TYPE = 'application/geo+json';

/**
 * The MIME type for CSV data
 */
const CSV_MIME_TYPE = 'text/csv';

/**
 * A list of MIME types that are supported in Unfolded Studio
 */
const UNFOLDED_SUPPORTED_MIME_TYPES = [GEOJSON_MIME_TYPE, CSV_MIME_TYPE];

class RenderedGeoJson extends Widget implements IRenderMime.IRenderer {
  /**
   * Create a new widget for rendering an Unfolded Map.
   */
  constructor(options: IRenderMime.IRendererOptions) {
    super();
    this.addClass(CSS_CLASS);
    this.options = options;
  }

  /**
   * Render Unfolded Studio into this widget's node.
   */
  async renderModel(model: IRenderMime.IMimeModel): Promise<void> {
    if (this.hasMapElement()) {
      return;
    }

    const data = model.data[this.options.mimeType] as string;
    const map = new UnfoldedMap({
      mapUrl: 'https://studio.unfolded.ai/incognito',
      appendToDocument: false,
      width: '100%',
      height: '100%',
      embed: true,
      onLoad: () => {
        if (data) {
          map.addDataset(
            {
              // TODO: Do we need to create an actual unique uuid? Or since this is an incognito map
              // it doesn't matter?
              uuid: 'd406c4ef-b570-4832-9e47-9c4a0a0dfe2e',

              // options.resolver.path contains the filename but isn't a public API
              // Is there a public API to get the filename?
              // @ts-expect-error Property 'path' does not exist on type 'IResolver'.
              label: this.options?.resolver?.path || 'Dataset',
              data,
            },
            true
          );
        }
      },
    });

    map.render(this.node);
  }

  /**
   * Check for the presence of an unfolded_iframe iframe element
   */
  private hasMapElement() {
    return this.node.querySelector('iframe#unfolded_iframe') !== null;
  }

  private options: IRenderMime.IRendererOptions;
}

/**
 * A mime renderer factory for data that can be displayed in Unfolded.
 */
export const unfoldedRendererFactory: IRenderMime.IRendererFactory = {
  safe: true,
  mimeTypes: UNFOLDED_SUPPORTED_MIME_TYPES,
  createRenderer: (options) => new RenderedGeoJson(options),
};

/**
 * Extension ID for Unfolded rendermime plugin
 */
const EXTENSION_ID = '@unfolded/jupyter-map-sdk:rendermime-plugin';

/**
 * Unfolded Rendermime extension
 */
const EXTENSION: IRenderMime.IExtension = {
  id: EXTENSION_ID,
  rendererFactory: unfoldedRendererFactory,
  rank: 0,
  dataType: 'string',
  fileTypes: [
    {
      name: 'geojson',
      mimeTypes: [GEOJSON_MIME_TYPE],
      extensions: ['.geojson', '.json'],
    },
    {
      name: 'csv',
      mimeTypes: [CSV_MIME_TYPE],
      extensions: ['.csv'],
    },
  ],
  documentWidgetFactoryOptions: {
    name: 'Unfolded Studio',
    primaryFileType: 'geojson',
    fileTypes: ['geojson', 'json', 'csv'],
    defaultFor: ['geojson'],
  },
};

const extensions: IRenderMime.IExtension[] = [EXTENSION];

export default extensions;
