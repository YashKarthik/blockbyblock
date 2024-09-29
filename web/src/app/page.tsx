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
    <div className="min-h-screen w-full font-serif flex flex-col bg-[#edddd4]">
      <header className="flex flex-col items-center p-4 space-y-4 md:flex-row md:justify-between md:space-y-0 px-10">
        <div className="flex items-center">
          <img src="/icon-bxb.svg" alt="Icon" className="w-16 h-16" />
        </div>
        <div className="text-center">
          <img src="logo-bxb.png" alt="Block x Block Logo" w-10 h-10 />
        </div>
        <nav className="w-full md:w-auto">
          <ul className="flex justify-center md:justify-end space-x-4 text-black font-sans">
            <li><a href="/about" className="text-sm md:text-base">ABOUT</a></li>
            <li><a href="/members" className="text-sm md:text-base">MEMBERS</a></li>
            <li><a href="/contact" className="text-sm md:text-base">CONTACT</a></li>
          </ul>
        </nav>
      </header>

      <main className="flex-grow px-14 items-center">
        <div className="w-full space-y-4">
          <div className="flex space-x-6 text-black font-sans">
            <div className="w-1/2 flex flex-col">
              <label htmlFor="start" className="block mb-1 text-sm md:text-base">Starting Location</label>
              <input
                id="start"
                type="text"
                placeholder="Where are you?"
                className="w-full p-2 border rounded text-sm md:text-base"
              />
            </div>
            <div className="w-1/2">
              <label htmlFor="destination" className="block mb-1 text-sm md:text-base">Destination</label>
              <input
                id="destination"
                type="text"
                placeholder="Where to?"
                className="w-full p-2 border rounded text-sm md:text-base"
              />
            </div>
          </div>

          <div>
            <Map center={center} zoom={zoom} mapRef={mapRef} mapContainerRef={mapContainerRef} />
            <div className="absolute bottom-4 right-4 z-10">
              <button
                onClick={() => flyHome()}
                className="bg-orange-100 text-yellow-600 border-2 border-yellow-600 rounded-sm p-1"
              >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
                  <path strokeLinecap="round" strokeLinejoin="round" d="m2.25 12 8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
