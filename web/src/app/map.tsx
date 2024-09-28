"use client"
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css';

import { useRef, useEffect, MutableRefObject } from 'react'

import { MAPBOX_PUBLIC_TOKEN } from '../../constants';

export function Map({ center, zoom, mapRef, mapContainerRef }: { center: [number, number], zoom: number, mapRef: MutableRefObject<mapboxgl.Map | null>, mapContainerRef: MutableRefObject<HTMLDivElement | null> }) {

  useEffect(() => {
    mapboxgl.accessToken = MAPBOX_PUBLIC_TOKEN as string
    mapRef.current = new mapboxgl.Map({
      container: mapContainerRef.current as HTMLDivElement,
      center: center,
      zoom: zoom,
      minZoom: zoom,
      style: 'mapbox://styles/yashkarthik/cm1mbnuh2003b01p3dhjt6vr6',
      maxBounds: [[-79.47431, 43.63528], [-79.25573, 43.77538]]
    });
    
    setTimeout(() => getEarthquakeData(), 1000);

    return () => {
      mapRef.current!.remove()
    }
  }, [])

  function getEarthquakeData() {
    if (mapRef.current) {
      mapRef.current.addSource("earthquakes", {
        type: "geojson",
      data: "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&eventtype=earthquake&minmagnitude=1&starttime=",
      generateId: true
    })

    mapRef.current.addLayer({
      id: 'earthquakes-viz',
      type: 'circle',
      source: 'earthquakes',
      paint: {
        'circle-stroke-color': '#000',
        'circle-stroke-width': 1,
        'circle-color': '#000'
      }
    });
  }
}

  return (
    <div className="h-screen w-screen" id="map-container" ref={mapContainerRef}>
    </div>
  );
}
