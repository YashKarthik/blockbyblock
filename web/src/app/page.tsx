"use client"
import { Map } from './map';
import { useState, useRef } from 'react';

export default function Home() {
  const [center, setCenter] = useState<[number, number]>([-79.38651, 43.65098])
  const [zoom, setZoom] = useState<number>(12)

  const mapRef = useRef<mapboxgl.Map | null>(null)
  const mapContainerRef = useRef<HTMLDivElement | null>(null)

  function flyHome() {
    if (mapRef.current) {
      mapRef.current.flyTo({
        center: center,
        zoom: zoom,
      })
    }
  }

  return (
    <div className="h-screen w-screen font-serif">
      <div className="absolute flex items-center gap-2 top-3 right-5 z-10 text-yellow-600 fill-black bg-orange-100 rounded-sm border-yellow-600 border-2 pr-1">
        <input type="text" className="bg-transparent border-none outline-none p-1 rounded-sm placeholder:text-yellow-500" placeholder='CN Tower' />

        <button onClick={() => flyHome()}>
          {/* Search icon */}
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-5">
            <path strokeLinecap="round" strokeLinejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
          </svg>
        </button>

        <button onClick={() => flyHome()}>
          {/* Home Icon */}
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-5">
            <path strokeLinecap="round" strokeLinejoin="round" d="m2.25 12 8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
          </svg>
        </button>
      </div>

      <Map center={center} zoom={zoom} mapRef={mapRef} mapContainerRef={mapContainerRef} />
    </div>
  );
}
