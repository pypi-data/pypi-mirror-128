import json
import re
from io import StringIO
from uuid import uuid4

import pandas as pd

from unfolded.map_sdk import HTMLUnfoldedMap, models

FEATURE_COLLECTION = {
    'type': 'FeatureCollection',
    'features': [
        {
            'type': 'Feature',
            'properties': {
                'osm_id': '5607525',
                'highway': 'path',
                'z_order': 0,
                'other_tags': '"bicycle"=>"designated","cycleway"=>"track","oneway"=>"no","segregated"=>"no","surface"=>"concrete"',
            },
            'geometry': {
                'type': 'LineString',
                'coordinates': [
                    [-105.0832007, 40.5643133],
                    [-105.0831921, 40.5642452],
                    [-105.0831719, 40.563753],
                    [-105.0831924, 40.5637403],
                ],
            },
        }
    ],
}

earthquakes_small_csv = """\
DateTime,Latitude,Longitude,Depth,Magnitude,MagType,NbStations,Gap,Distance,RMS,Source,EventID
1967/08/01 10:33:50.47,36.08000,-121.07083,80.339,2.50,Mx,10,292,42,0.25,NCSN,1000872
1967/08/02 02:49:12.55,35.63433,-120.75716,3.980,2.60,Mx,9,322,108,0.24,NCSN,1000887
1967/08/03 05:55:26.73,36.37967,-121.00850,39.609,2.70,Mx,10,298,21,0.41,NCSN,1000912
1967/08/03 06:57:01.25,36.39550,-121.01667,40.159,2.70,Mx,10,293,19,0.46,NCSN,1000916
1967/08/03 20:21:26.52,36.54350,-121.17216,5.945,2.60,Mx,10,132,6,0.07,NCSN,1000926
"""
EARTHQUAKES = pd.read_csv(StringIO(earthquakes_small_csv))


class TestHTMLUnfoldedMap:
    def test_has_same_iframe_id(self):
        m = HTMLUnfoldedMap()
        html_source = m._repr_html_()
        get_elem_match = re.search(r'getElementById\(\'([a-zA-Z0-9\-]+)', html_source)
        uuid1 = get_elem_match.groups()[0]

        iframe_match = re.search(r'iframe\s*id=\"(([a-zA-Z0-9\-]+))', html_source)
        uuid2 = iframe_match.groups()[0]

        assert uuid1 == uuid2, 'UUID in iframe should equal UUID in getElementById'

    def test_dataset_automatic(self):
        dataset = models.Dataset(data=json.dumps(FEATURE_COLLECTION))
        m = HTMLUnfoldedMap(datasets=[dataset])
        html_source = m._repr_html_()

        assert re.search(
            r'map-sdk-add-dataset-to-map', html_source
        ), 'Event with type map-sdk-add-dataset-to-map should be created in HTML'
        assert re.search(
            r'autoCreateLayers:\s*true', html_source
        ), 'autoCreateLayers should be true'
        assert not re.search(
            r'map-sdk-add-layer', html_source
        ), 'Event with type map-sdk-add-layer should *not* be created in HTML'

    def test_dataset_not_automatic(self):
        dataset_id = uuid4()
        dataset = models.Dataset(uuid=dataset_id, data=json.dumps(FEATURE_COLLECTION))

        # Layer dict copied from this map config:
        # https://cdn.published.unfolded.ai/maps/7ca774ec-f061-465c-8b43-41943d220917/published/0f650a07-0b6c-47a7-ba19-e8194251e9a0/studio-state.json
        layer_dict = {
            'id': 'k6c2rq',
            'type': 'geojson',
            'config': {
                'dataId': dataset_id,
                'columnMode': 'geojson',
                'label': 'trails_with_elev',
                'color': [231, 159, 213],
                'columns': {'geojson': '_geojson'},
                'isVisible': True,
                'visConfig': {
                    'opacity': 0.8,
                    'strokeOpacity': 0.8,
                    'thickness': 0.8,
                    'strokeColor': [254, 179, 26],
                    'colorRange': {
                        'name': 'Global Warming',
                        'type': 'sequential',
                        'category': 'Uber',
                        'colors': [
                            '#4C0035',
                            '#880030',
                            '#B72F15',
                            '#D6610A',
                            '#EF9100',
                            '#FFC300',
                        ],
                    },
                    'strokeColorRange': {
                        'name': 'Global Warming',
                        'type': 'sequential',
                        'category': 'Uber',
                        'colors': [
                            '#4C0035',
                            '#880030',
                            '#B72F15',
                            '#D6610A',
                            '#EF9100',
                            '#FFC300',
                        ],
                    },
                    'radius': 10,
                    'sizeRange': [0, 10],
                    'radiusRange': [0, 50],
                    'heightRange': [0, 500],
                    'elevationScale': 5,
                    'stroked': True,
                    'filled': False,
                    'enable3d': False,
                    'wireframe': False,
                    'fixedHeight': False,
                },
                'hidden': False,
                'textLabel': [
                    {
                        'field': None,
                        'color': [255, 255, 255],
                        'size': 18,
                        'offset': [0, 0],
                        'anchor': 'start',
                        'alignment': 'center',
                    }
                ],
            },
            'visualChannels': {
                'colorField': None,
                'colorScale': 'quantile',
                'strokeColorField': None,
                'strokeColorScale': 'quantile',
                'sizeField': None,
                'sizeScale': 'linear',
                'heightField': None,
                'heightScale': 'linear',
                'radiusField': None,
                'radiusScale': 'linear',
            },
        }

        m = HTMLUnfoldedMap(datasets=[dataset], layers=[layer_dict])
        html_source = m._repr_html_()
        assert re.search(
            r'map-sdk-add-dataset-to-map', html_source
        ), 'Event with type map-sdk-add-dataset-to-map should be created in HTML'
        assert re.search(
            r'autoCreateLayers:\s*false', html_source
        ), 'autoCreateLayers should be false'
        assert re.search(
            r'map-sdk-add-layer', html_source
        ), 'Event with type map-sdk-add-layer should be created in HTML'
        assert (
            len(re.findall(str(dataset_id), html_source)) == 2
        ), 'The dataset ID should be present twice. Once in the add_dataset call and once in the add_layer call.'

    def test_dataset_filter(self):
        dataset_id = uuid4()
        dataset = models.Dataset(uuid=dataset_id, label='Earthquakes', data=EARTHQUAKES)
        filter_info = models.FilterInfo(
            id='filter_id', data_id=dataset_id, field='Magnitude', value=[2.5, 2.6]
        )

        m = HTMLUnfoldedMap(datasets=[dataset], filters=[filter_info])
        html_source = m._repr_html_()

        assert re.search(
            r'map-sdk-add-dataset-to-map', html_source
        ), 'Event with type map-sdk-add-dataset-to-map should be created in HTML'
        assert re.search(
            r'autoCreateLayers:\s*true', html_source
        ), 'autoCreateLayers should be true'
        assert re.search(
            r'map-sdk-set-filter', html_source
        ), 'Event with type map-sdk-set-filter should be created in HTML'
        assert (
            len(re.findall(str(dataset_id), html_source)) == 2
        ), 'The dataset ID should be present twice. Once in the add_dataset call and once in the set_filter call.'

    def test_map_config(self):
        dataset_id = uuid4()
        dataset = models.Dataset(uuid=dataset_id, data=json.dumps(FEATURE_COLLECTION))

        coord = FEATURE_COLLECTION['features'][0]['geometry']['coordinates'][0]

        map_config = {
            "version": "v1",
            "config": {
                "visState": {
                    "filters": [],
                    "layers": [
                        {
                            "id": "y4osz29",
                            "type": "rasterTile",
                            "config": {
                                "dataId": "18163f9e-f086-4ff2-9a71-8ff0f7bcbbe0",
                                "label": "National Agriculture Imagery Program (NAIP)",
                                "color": [30, 150, 190],
                                "columns": {},
                                "isVisible": True,
                                "visConfig": {
                                    "preset": "trueColor",
                                    "mosaicId": "dynamodb://us-west-2/naip:analytic_2016-2019.v1",
                                    "useSTACSearching": False,
                                    "stacSearchProvider": "earth-search",
                                    "startDate": "2019-02-02",
                                    "endDate": "2019-03-02",
                                    "colormapId": "cfastie",
                                    "linearRescalingFactor": [0, 1],
                                    "nonLinearRescaling": True,
                                    "gammaContrastFactor": 1,
                                    "sigmoidalContrastFactor": 6,
                                    "sigmoidalBiasFactor": 0.3,
                                    "saturationValue": 1.2,
                                    "filterEnabled": False,
                                    "filterRange": [-1, 1],
                                    "opacity": 1,
                                },
                                "hidden": False,
                                "textLabel": [
                                    {
                                        "field": None,
                                        "color": [255, 255, 255],
                                        "size": 18,
                                        "offset": [0, 0],
                                        "anchor": "start",
                                        "alignment": "center",
                                    }
                                ],
                            },
                            "visualChannels": {},
                        },
                        {
                            "id": "k6c2rq",
                            "type": "geojson",
                            "config": {
                                "dataId": str(dataset_id),
                                "columnMode": "geojson",
                                "label": "trails_with_elev",
                                "color": [231, 159, 213],
                                "columns": {"geojson": "_geojson"},
                                "isVisible": True,
                                "visConfig": {
                                    "opacity": 0.8,
                                    "strokeOpacity": 0.4,
                                    "thickness": 0.8,
                                    "strokeColor": [254, 179, 26],
                                    "colorRange": {
                                        "name": "Global Warming",
                                        "type": "sequential",
                                        "category": "Uber",
                                        "colors": [
                                            "#4C0035",
                                            "#880030",
                                            "#B72F15",
                                            "#D6610A",
                                            "#EF9100",
                                            "#FFC300",
                                        ],
                                    },
                                    "strokeColorRange": {
                                        "name": "Global Warming",
                                        "type": "sequential",
                                        "category": "Uber",
                                        "colors": [
                                            "#4C0035",
                                            "#880030",
                                            "#B72F15",
                                            "#D6610A",
                                            "#EF9100",
                                            "#FFC300",
                                        ],
                                    },
                                    "radius": 20,
                                    "sizeRange": [0, 10],
                                    "radiusRange": [0, 50],
                                    "heightRange": [0, 500],
                                    "elevationScale": 5,
                                    "stroked": True,
                                    "filled": False,
                                    "enable3d": False,
                                    "wireframe": False,
                                    "fixedHeight": False,
                                },
                                "hidden": False,
                                "textLabel": [
                                    {
                                        "field": None,
                                        "color": [255, 255, 255],
                                        "size": 18,
                                        "offset": [0, 0],
                                        "anchor": "start",
                                        "alignment": "center",
                                    }
                                ],
                            },
                            "visualChannels": {
                                "colorField": None,
                                "colorScale": "quantile",
                                "strokeColorField": None,
                                "strokeColorScale": "quantile",
                                "sizeField": None,
                                "sizeScale": "linear",
                                "heightField": None,
                                "heightScale": "linear",
                                "radiusField": None,
                                "radiusScale": "linear",
                            },
                        },
                    ],
                    "interactionConfig": {
                        "tooltip": {
                            "fieldsToShow": {
                                str(dataset_id): [
                                    {"name": "osm_id", "format": None},
                                    {"name": "highway", "format": None},
                                    {"name": "z_order", "format": None},
                                    {"name": "other_tags", "format": None},
                                    {"name": "name", "format": None},
                                ],
                                "18163f9e-f086-4ff2-9a71-8ff0f7bcbbe0": [],
                            },
                            "compareMode": False,
                            "compareType": "absolute",
                            "enabled": True,
                        },
                        "brush": {"size": 0.5, "enabled": False},
                        "geocoder": {"enabled": False},
                        "coordinate": {"enabled": False},
                    },
                    "layerBlending": "normal",
                    "splitMaps": [],
                    "animationConfig": {"currentTime": None, "speed": 1},
                    "metrics": [],
                    "geoKeys": [],
                    "groupBys": [],
                    "datasets": {
                        "fieldDisplayNames": {
                            str(dataset_id): {},
                            "18163f9e-f086-4ff2-9a71-8ff0f7bcbbe0": {},
                        }
                    },
                    "joins": [],
                    "charts": [],
                },
                "mapState": {
                    "bearing": -25.029700048947777,
                    "dragRotate": True,
                    "latitude": coord[1],
                    "longitude": coord[0],
                    "pitch": 0,
                    "zoom": 14,
                    "isSplit": False,
                    "mapViewMode": "MODE_3D",
                    "mapSplitMode": "SINGLE_MAP",
                    "globe": {
                        "enabled": False,
                        "config": {
                            "atmosphere": True,
                            "azimuth": False,
                            "azimuthAngle": 45,
                            "basemap": True,
                            "labels": False,
                            "terminator": True,
                            "terminatorOpacity": 0.35,
                        },
                    },
                },
                "mapStyle": {
                    "styleType": "light",
                    "topLayerGroups": {"label": True},
                    "visibleLayerGroups": {
                        "label": True,
                        "road": True,
                        "border": False,
                        "building": True,
                        "water": True,
                        "land": True,
                        "3d building": False,
                    },
                    "threeDBuildingColor": [
                        9.665468314072013,
                        17.18305478057247,
                        31.1442867897876,
                    ],
                    "mapStyles": {},
                },
            },
        }

        m = HTMLUnfoldedMap(datasets=[dataset], map_config=map_config)
        html_source = m._repr_html_()

        assert re.search(
            r'map-sdk-add-dataset-to-map', html_source
        ), 'Event with type map-sdk-add-dataset-to-map should be created in HTML'
        assert re.search(
            r'autoCreateLayers:\s*false', html_source
        ), 'autoCreateLayers should be false'
        assert not re.search(
            r'map-sdk-set-filter', html_source
        ), 'Event with type map-sdk-set-filter should *not* be created in HTML'
        assert not re.search(
            r'map-sdk-add-layer', html_source
        ), 'Event with type map-sdk-add-layer should *not* be created in HTML'
        assert re.search(
            r'map-sdk-set-map-config', html_source
        ), 'Event with type map-sdk-set-map-config should be created in HTML'

        assert not re.search(
            r'map_config:', html_source
        ), 'mapConfig should be camelCase not snake_case'
        assert re.search(
            r'mapConfig:', html_source
        ), 'mapConfig should be camelCase not snake_case'

    def test_map_config_earthquakes(self):
        dataset_id = str(uuid4())
        dataset = models.Dataset(uuid=dataset_id, data=EARTHQUAKES)

        map_config = {
            "version": "v1",
            "config": {
                "visState": {
                    "filters": [
                        {
                            "dataId": [dataset_id],
                            "id": "k7319uc78",
                            "name": ["time"],
                            "type": "timeRange",
                            "value": [1603701166243.6045, 1603787566242.6052],
                            "enlarged": True,
                            "plotType": {
                                "interval": "12-hour",
                                "type": "lineChart",
                                "aggregation": "maximum",
                            },
                            "animationWindow": "free",
                            "yAxis": {"name": "mag", "type": "real"},
                            "speed": 1,
                        }
                    ],
                    "layers": [
                        {
                            "id": "k30kgcr",
                            "type": "geojson",
                            "config": {
                                "dataId": dataset_id,
                                "columnMode": "geojson",
                                "label": "all_month",
                                "color": [18, 147, 154],
                                "columns": {"geojson": "_geojson"},
                                "isVisible": True,
                                "visConfig": {
                                    "opacity": 0.8,
                                    "strokeOpacity": 0.8,
                                    "thickness": 0.5,
                                    "strokeColor": None,
                                    "colorRange": {
                                        "name": "Global Warming",
                                        "type": "sequential",
                                        "category": "Uber",
                                        "colors": [
                                            "#5A1846",
                                            "#900C3F",
                                            "#C70039",
                                            "#E3611C",
                                            "#F1920E",
                                            "#FFC300",
                                        ],
                                    },
                                    "strokeColorRange": {
                                        "name": "Global Warming",
                                        "type": "sequential",
                                        "category": "Uber",
                                        "colors": [
                                            "#5A1846",
                                            "#900C3F",
                                            "#C70039",
                                            "#E3611C",
                                            "#F1920E",
                                            "#FFC300",
                                        ],
                                    },
                                    "radius": 10,
                                    "sizeRange": [0, 10],
                                    "radiusRange": [0, 50],
                                    "heightRange": [0, 500],
                                    "elevationScale": 5,
                                    "stroked": False,
                                    "filled": True,
                                    "enable3d": False,
                                    "wireframe": False,
                                    "fixedHeight": False,
                                },
                                "hidden": False,
                                "textLabel": [
                                    {
                                        "field": None,
                                        "color": [255, 255, 255],
                                        "size": 18,
                                        "offset": [0, 0],
                                        "anchor": "start",
                                        "alignment": "center",
                                    }
                                ],
                            },
                            "visualChannels": {
                                "colorField": {"name": "mag", "type": "real"},
                                "colorScale": "quantile",
                                "strokeColorField": None,
                                "strokeColorScale": "quantile",
                                "sizeField": None,
                                "sizeScale": "linear",
                                "heightField": None,
                                "heightScale": "linear",
                                "radiusField": None,
                                "radiusScale": "linear",
                            },
                        },
                        {
                            "id": "g8n1vni",
                            "type": "geojson",
                            "config": {
                                "dataId": dataset_id,
                                "columnMode": "geojson",
                                "label": "new layer",
                                "color": [34, 63, 154],
                                "columns": {"geojson": "_geojson"},
                                "isVisible": True,
                                "visConfig": {
                                    "opacity": 0.8,
                                    "strokeOpacity": 0.8,
                                    "thickness": 0.5,
                                    "strokeColor": None,
                                    "colorRange": {
                                        "name": "Global Warming",
                                        "type": "sequential",
                                        "category": "Uber",
                                        "colors": [
                                            "#5A1846",
                                            "#900C3F",
                                            "#C70039",
                                            "#E3611C",
                                            "#F1920E",
                                            "#FFC300",
                                        ],
                                    },
                                    "strokeColorRange": {
                                        "name": "Global Warming",
                                        "type": "sequential",
                                        "category": "Uber",
                                        "colors": [
                                            "#5A1846",
                                            "#900C3F",
                                            "#C70039",
                                            "#E3611C",
                                            "#F1920E",
                                            "#FFC300",
                                        ],
                                    },
                                    "radius": 79.7,
                                    "sizeRange": [0, 10],
                                    "radiusRange": [0, 50],
                                    "heightRange": [0, 500],
                                    "elevationScale": 5,
                                    "stroked": True,
                                    "filled": False,
                                    "enable3d": False,
                                    "wireframe": False,
                                    "fixedHeight": False,
                                },
                                "hidden": False,
                                "textLabel": [
                                    {
                                        "field": None,
                                        "color": [255, 255, 255],
                                        "size": 18,
                                        "offset": [0, 0],
                                        "anchor": "start",
                                        "alignment": "center",
                                    }
                                ],
                            },
                            "visualChannels": {
                                "colorField": None,
                                "colorScale": "quantile",
                                "strokeColorField": {"name": "felt", "type": "integer"},
                                "strokeColorScale": "quantile",
                                "sizeField": None,
                                "sizeScale": "linear",
                                "heightField": None,
                                "heightScale": "linear",
                                "radiusField": None,
                                "radiusScale": "linear",
                            },
                        },
                    ],
                    "interactionConfig": {
                        "tooltip": {
                            "fieldsToShow": {
                                dataset_id: [
                                    {"name": "mag", "format": None},
                                    {"name": "place", "format": None},
                                    {"name": "time", "format": None},
                                    {"name": "updated", "format": None},
                                    {"name": "tz", "format": None},
                                ]
                            },
                            "compareMode": False,
                            "compareType": "absolute",
                            "enabled": True,
                        },
                        "brush": {"size": 0.5, "enabled": False},
                        "geocoder": {"enabled": False},
                        "coordinate": {"enabled": False},
                    },
                    "layerBlending": "additive",
                    "splitMaps": [],
                    "animationConfig": {"currentTime": None, "speed": 1},
                    "metrics": [],
                    "geoKeys": [],
                    "groupBys": [],
                    "datasets": {"fieldDisplayNames": {dataset_id: {}}},
                    "joins": [],
                    "charts": [],
                },
                "mapState": {
                    "bearing": 0,
                    "dragRotate": False,
                    "latitude": 45.98714824780471,
                    "longitude": -112.25342718053346,
                    "pitch": 0,
                    "zoom": 2.6539953739060738,
                    "isSplit": False,
                    "mapViewMode": "MODE_2D",
                    "mapSplitMode": "SINGLE_MAP",
                    "globe": {
                        "enabled": False,
                        "config": {
                            "atmosphere": True,
                            "azimuth": False,
                            "azimuthAngle": 45,
                            "basemap": True,
                            "labels": False,
                            "terminator": True,
                            "terminatorOpacity": 0.35,
                        },
                    },
                },
                "mapStyle": {
                    "styleType": "dark",
                    "topLayerGroups": {},
                    "visibleLayerGroups": {
                        "label": True,
                        "road": True,
                        "border": False,
                        "building": True,
                        "water": True,
                        "land": True,
                        "3d building": False,
                    },
                    "threeDBuildingColor": [
                        9.665468314072013,
                        17.18305478057247,
                        31.1442867897876,
                    ],
                    "mapStyles": {},
                },
            },
        }

        m = HTMLUnfoldedMap(datasets=[dataset], map_config=map_config)

        html_source = m._repr_html_()
        assert re.search(
            r'map-sdk-add-dataset-to-map', html_source
        ), 'Event with type map-sdk-add-dataset-to-map should be created in HTML'
        assert re.search(
            r'autoCreateLayers:\s*false', html_source
        ), 'autoCreateLayers should be false'
        assert not re.search(
            r'map-sdk-set-filter', html_source
        ), 'Event with type map-sdk-set-filter should *not* be created in HTML'
        assert not re.search(
            r'map-sdk-add-layer', html_source
        ), 'Event with type map-sdk-add-layer should *not* be created in HTML'
        assert re.search(
            r'map-sdk-set-map-config', html_source
        ), 'Event with type map-sdk-set-map-config should be created in HTML'

        assert not re.search(
            r'map_config:', html_source
        ), 'mapConfig should be camelCase not snake_case'
        assert re.search(
            r'mapConfig:', html_source
        ), 'mapConfig should be camelCase not snake_case'
