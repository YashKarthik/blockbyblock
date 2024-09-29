"use client"
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css';

import data from "../../data4.json"

import { useEffect, MutableRefObject, useState } from 'react'

import { MAPBOX_PUBLIC_TOKEN } from '../../constants';

export function Map({ center, zoom, mapRef, mapContainerRef }: { center: [number, number], zoom: number, mapRef: MutableRefObject<mapboxgl.Map | null>, mapContainerRef: MutableRefObject<HTMLDivElement | null> }) {
  const [minute, setHour] = useState(-1);

  useEffect(() => {
    mapboxgl.accessToken = MAPBOX_PUBLIC_TOKEN as string
    mapRef.current = new mapboxgl.Map({
      container: mapContainerRef.current as HTMLDivElement,
      center: center,
      zoom: zoom,
      style: 'mapbox://styles/yashkarthik/cm1mbnuh2003b01p3dhjt6vr6',
      maxBounds: [[-79.47431, 43.63528], [-79.25573, 43.77538]]
    });

    const marker = new mapboxgl.Marker({
      color: "red",
    })
      .setLngLat([-79.3790669409802, 43.64364522322814])
      .addTo(mapRef.current);

    mapRef.current.on('load', () => {
      getHeatmap();
      if (minute <= -1) {
        setHour(0);
      }
    })

    return () => {
      mapRef.current!.remove()
    }
  }, [])

  useEffect(() => {
    if (minute >= 0) {
      console.log("here", minute)
      mapRef.current!.setFilter('earthquakes-heat', ['==', ['get', 'offset'], minute])
      mapRef.current!.setFilter('earthquakes-viz', ['==', ['get', 'offset'], minute])
    }
  }, [minute]);

  function getHeatmap() {
    if (mapRef.current) {
      if (!mapRef.current.getSource("earthquakes")) {
        mapRef.current.addSource("earthquakes", {
          type: "geojson",
          // @ts-ignore
          data: data
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
              'heatmap-radius': 40,
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

      <div className="absolute bottom-3 right-0 m-4 bg-white text-black p-2 rounded-md">
        <h2>Time: <label id="active-hour">{ minute }</label></h2>
        <input
          id="slider"
          className="row"
          type="range"
          min="0"
          max="60"
          step="5"
          value={ minute }
          onChange={(e) => setHour(parseInt(e.target.value))}
        />
      </div>
    </>
  );
}
