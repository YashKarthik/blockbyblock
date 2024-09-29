"use client"
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css';

import data from "../../data6.json"

import { useEffect, MutableRefObject, useState, Dispatch, SetStateAction } from 'react'

import { MAPBOX_PUBLIC_TOKEN } from '../../constants';

export function Map({ center, zoom, mapRef, mapContainerRef }: { center: [number, number], zoom: number, mapRef: MutableRefObject<mapboxgl.Map | null>, mapContainerRef: MutableRefObject<HTMLDivElement | null> }) {
  const [offset, setOffset] = useState(-1);
  const [startCoords, setStartCoords] = useState([-79.39087785766945, 43.67171211911842]);
  const [destCoords, setDestCoords] = useState([-79.3790669409802, 43.64364522322814]);
  const [bestStart,  setBestStart] = useState<number[] | null>(null);

  useEffect(() => {
    mapboxgl.accessToken = MAPBOX_PUBLIC_TOKEN as string
    mapRef.current = new mapboxgl.Map({
      container: mapContainerRef.current as HTMLDivElement,
      center: center,
      zoom: zoom,
      style: 'mapbox://styles/yashkarthik/cm1mbnuh2003b01p3dhjt6vr6',
      maxBounds: [[-79.47431, 43.63528], [-79.25573, 43.77538]]
    });

    const destMarker = new mapboxgl.Marker({
      draggable: true,
      color: "red",
    })
      .setLngLat([-79.3790669409802, 43.64364522322814])
      .addTo(mapRef.current);

    const startMarker = new mapboxgl.Marker({
      draggable: true,
      color: "blue",
    })
      .setLngLat([-79.3964842837308, 43.67473658056805])
      .addTo(mapRef.current);

    function onDragEndDest() {
      const lngLat = destMarker.getLngLat();
      setDestCoords([lngLat.lng, lngLat.lat]);
    }

    function onDragEndStart() {
      const lngLat = startMarker.getLngLat();
      setStartCoords([lngLat.lng, lngLat.lat]);
    }

    destMarker.on('dragend', onDragEndDest);
    startMarker.on('dragend', onDragEndStart);

    mapRef.current.on('load', () => {
      getHeatmap();
      // @ts-ignore
      mapRef.current.getSource('earthquakes').setData(data);
      if (offset <= -1) {
        setOffset(0);
      }
    })

    return () => {
      mapRef.current!.remove()
    }
  }, [])

  useEffect(() => {
    if (offset >= 0) {
      console.log("here", offset)
      mapRef.current!.setFilter('earthquakes-heat', ['==', ['get', 'offset'], offset])
      mapRef.current!.setFilter('earthquakes-viz', ['==', ['get', 'offset'], offset])
    }
  }, [offset]);

  useEffect(() => {
    if (offset < 0) return;
    if (bestStart === null || mapRef.current == null) return;

    const bestMarker = new mapboxgl.Marker({
      color: "violet",
    })
    .setLngLat([bestStart[0], bestStart[1]])
    .addTo(mapRef.current);

    setOffset(bestStart[2]);

  }, [bestStart]);

  useEffect(() => {
    async function getData(){
      setBestStart([-79.3790669409802, 43.64865522322814, 10]);
      const data = await fetch("http://localhost:5000/api", {
      headers: {
        "Content-Type": "application/json",
      },
      method: "POST",
      body: JSON.stringify({
        start: startCoords,
        dest: destCoords,
       })
      })
      const res = await data.json();
      console.log(res)
      // @ts-ignore
      mapRef.current.getSource('earthquakes').setData(res);
    }

    getData();

    }, [startCoords, destCoords]);

  function getHeatmap() {
    if (mapRef.current) {
      if (!mapRef.current.getSource("earthquakes")) {
        mapRef.current.addSource("earthquakes", {
          type: "geojson",
          // @ts-ignore
          data: []
        });

        mapRef.current.addLayer({
          id: 'earthquakes-viz',
          type: 'circle',
          source: 'earthquakes',
          paint: {
            'circle-stroke-color': '#000',
            'circle-stroke-width': 0.1,
            'circle-color': '#000'
          }
        });

        mapRef.current.addLayer(
          {
            id: 'earthquakes-heat',
            type: 'heatmap',
            source: 'earthquakes',
            paint: {
              'heatmap-color': [
                "interpolate",
                ["linear"],
                ["heatmap-density"],
                0, "rgba(0, 0, 255, 0)",
                0.2, "royalblue",
                0.3, "cyan",
                0.7, "lime",
                0.9, "yellow",
                1, "red"
              ],
              'heatmap-radius': [
                "interpolate",
                ["linear"],
                ["zoom"],
                1, 10,
                12, 30
              ],
              'heatmap-opacity': 0.5
            }
          },
        );
      }
    }
  }


  return (
    <>
      <div className="h-screen w-screen" id="map-container" ref={mapContainerRef}>
      </div>

      <div className="absolute bottom-3 right-0 m-4 bg-orange-100 text-yellow-600 p-2 border-2 border-orange-400 rounded-md">
        <h2>Time: <label id="active-hour">{ offset }</label></h2>
        <input
          id="slider"
          className="row"
          type="range"
          min="0"
          max="60"
          step="5"
          value={ offset }
          onChange={(e) => setOffset(parseInt(e.target.value))}
        />
      </div>
    </>
  );
}
