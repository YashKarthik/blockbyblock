"use client"
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css';

import data from "../../data6.json"

import { useEffect, MutableRefObject, useState, Dispatch, SetStateAction } from 'react'

import { MAPBOX_PUBLIC_TOKEN } from '../../constants';

export function Map({ center, zoom, mapRef, mapContainerRef }: { center: [number, number], zoom: number, mapRef: MutableRefObject<mapboxgl.Map | null>, mapContainerRef: MutableRefObject<HTMLDivElement | null> }) {
  const [minute, setHour] = useState(-1);
  const [startCoords, setStartCoords] = useState([-79.39087785766945, 43.67171211911842]);
  const [destCoords, setDestCoords] = useState([-79.3790669409802, 43.64364522322814]);

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

  useEffect(() => {
    async function getData(){
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

      <div className="absolute bottom-3 right-0 m-4 bg-orange-100 text-yellow-600 p-2 border-2 border-orange-400 rounded-md">
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
