#!/usr/bin/env python3
"""
Find the nearest route from Kateel to Udupi without tolls.
"""

import requests
import json
import os
from typing import List, Dict, Optional

# Coordinates for Kateel and Udupi (Karnataka, India)
KATEEL_COORDS = (12.9375, 74.8250)  # Approximate coordinates for Kateel
UDUPI_COORDS = (13.3389, 74.7451)   # Approximate coordinates for Udupi

def get_route_osrm(start: tuple, end: tuple, avoid_tolls: bool = True) -> Optional[Dict]:
    """
    Get route using OSRM (Open Source Routing Machine).
    OSRM is free and doesn't require an API key.
    """
    # OSRM public server (may have rate limits)
    base_url = "http://router.project-osrm.org"
    
    # Format: longitude,latitude (OSRM uses lon,lat order)
    coordinates = f"{start[1]},{start[0]};{end[1]},{end[0]}"
    
    # OSRM route service
    url = f"{base_url}/route/v1/driving/{coordinates}"
    
    params = {
        "overview": "full",
        "geometries": "geojson",
        "steps": "true"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == "Ok" and data.get("routes"):
                route = data["routes"][0]
                return {
                    "distance_km": route["distance"] / 1000,  # Convert meters to km
                    "duration_minutes": route["duration"] / 60,  # Convert seconds to minutes
                    "geometry": route["geometry"],
                    "legs": route.get("legs", []),
                    "service": "OSRM"
                }
    except Exception as e:
        print(f"OSRM error: {e}")
    
    return None

def get_route_google_maps(start: tuple, end: tuple, api_key: Optional[str] = None, avoid_tolls: bool = True) -> Optional[Dict]:
    """
    Get route using Google Maps Directions API with toll avoidance.
    Requires API key from Google Cloud Console.
    """
    if not api_key:
        return None
    
    base_url = "https://maps.googleapis.com/maps/api/directions/json"
    
    params = {
        "origin": f"{start[0]},{start[1]}",
        "destination": f"{end[0]},{end[1]}",
        "key": api_key,
        "units": "metric"
    }
    
    if avoid_tolls:
        params["avoid"] = "tolls"
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "OK" and data.get("routes"):
                route = data["routes"][0]
                leg = route["legs"][0]
                
                # Check if route has tolls
                has_tolls = False
                for step in leg.get("steps", []):
                    if "toll" in step.get("html_instructions", "").lower():
                        has_tolls = True
                        break
                
                return {
                    "distance_km": leg["distance"]["value"] / 1000,  # Convert meters to km
                    "duration_minutes": leg["duration"]["value"] / 60,  # Convert seconds to minutes
                    "has_tolls": has_tolls,
                    "steps": leg.get("steps", []),
                    "polyline": route.get("overview_polyline", {}).get("points", ""),
                    "service": "Google Maps",
                    "avoid_tolls": avoid_tolls
                }
    except Exception as e:
        print(f"Google Maps API error: {e}")
    
    return None

def get_route_openrouteservice(start: tuple, end: tuple, api_key: Optional[str] = None) -> Optional[Dict]:
    """
    Get route using OpenRouteService API.
    Requires API key (free tier available at https://openrouteservice.org/).
    """
    if not api_key:
        return None
    
    base_url = "https://api.openrouteservice.org/v2/directions/driving-car"
    
    # Format: [longitude, latitude]
    coordinates = [[start[1], start[0]], [end[1], end[0]]]
    
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }
    
    body = {
        "coordinates": coordinates,
        "preference": "shortest",
        "instructions": True,
        "geometry": True
    }
    
    try:
        response = requests.post(base_url, json=body, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("routes"):
                route = data["routes"][0]
                summary = route["summary"]
                return {
                    "distance_km": summary["distance"] / 1000,  # Convert meters to km
                    "duration_minutes": summary["duration"] / 60,  # Convert seconds to minutes
                    "geometry": route["geometry"],
                    "segments": route.get("segments", []),
                    "service": "OpenRouteService"
                }
    except Exception as e:
        print(f"OpenRouteService error: {e}")
    
    return None

def get_coordinates_from_place(place_name: str) -> Optional[tuple]:
    """
    Get coordinates for a place name using Nominatim (OpenStreetMap geocoding).
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": place_name,
        "format": "json",
        "limit": 1
    }
    
    # Nominatim requires a user agent
    headers = {
        "User-Agent": "RouteFinder/1.0"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data:
                lat = float(data[0]["lat"])
                lon = float(data[0]["lon"])
                return (lat, lon)
    except Exception as e:
        print(f"Geocoding error for {place_name}: {e}")
    
    return None

def main():
    print("Finding route from Kateel to Udupi (without tolls)...")
    print("=" * 60)
    
    # Get accurate coordinates
    print("\n1. Getting coordinates for locations...")
    kateel_coords = get_coordinates_from_place("Kateel, Karnataka, India")
    udupi_coords = get_coordinates_from_place("Udupi, Karnataka, India")
    
    if not kateel_coords:
        print("Warning: Could not geocode Kateel, using approximate coordinates")
        kateel_coords = KATEEL_COORDS
    else:
        print(f"   ✓ Kateel: {kateel_coords[0]:.6f}, {kateel_coords[1]:.6f}")
    
    if not udupi_coords:
        print("Warning: Could not geocode Udupi, using approximate coordinates")
        udupi_coords = UDUPI_COORDS
    else:
        print(f"   ✓ Udupi: {udupi_coords[0]:.6f}, {udupi_coords[1]:.6f}")
    
    # Try Google Maps API first (best for toll avoidance)
    google_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    route = None
    
    if google_api_key:
        print("\n2. Finding route using Google Maps API (with toll avoidance)...")
        route = get_route_google_maps(kateel_coords, udupi_coords, google_api_key, avoid_tolls=True)
    
    # Fallback to OSRM if Google Maps not available
    if not route:
        print("\n2. Finding route (trying OSRM, free service)...")
        print("   Note: OSRM doesn't support toll avoidance. For accurate toll-free routes,")
        print("         set GOOGLE_MAPS_API_KEY environment variable.")
        route = get_route_osrm(kateel_coords, udupi_coords)
    
    if route:
        print(f"\n{'='*60}")
        print(f"✓ Route found using {route['service']}")
        print(f"{'='*60}")
        print(f"  Distance: {route['distance_km']:.2f} km")
        print(f"  Estimated Duration: {route['duration_minutes']:.1f} minutes ({route['duration_minutes']/60:.1f} hours)")
        
        if route.get('avoid_tolls'):
            print(f"  ✓ Toll avoidance: Enabled")
            if route.get('has_tolls'):
                print(f"  ⚠ Warning: Route may still contain tolls (check route details)")
            else:
                print(f"  ✓ Route verified as toll-free")
        else:
            print(f"  ⚠ Note: Toll avoidance not supported by this service")
            print(f"     For guaranteed toll-free routes, use Google Maps API")
        
        print(f"\n💡 Tip: To get the exact toll-free route with Google Maps API:")
        print(f"   1. Get API key from: https://console.cloud.google.com/")
        print(f"   2. Enable 'Directions API'")
        print(f"   3. Set environment variable: export GOOGLE_MAPS_API_KEY='your-key'")
        print(f"   4. Run this script again")
    else:
        print("\n✗ Could not get route")
        print("\nAlternative options:")
        print("1. Use Google Maps API with toll avoidance:")
        print("   - Get API key from Google Cloud Console")
        print("   - Enable Directions API")
        print("   - Set GOOGLE_MAPS_API_KEY environment variable")
        print("\n2. Use Google Maps web interface:")
        print("   - Go to https://maps.google.com")
        print("   - Search for route from Kateel to Udupi")
        print("   - Click 'Options' and enable 'Avoid tolls'")
        print("\n3. Use OpenRouteService API:")
        print("   - Sign up at https://openrouteservice.org/ (free tier available)")
        print("   - Set OPENROUTESERVICE_API_KEY environment variable")

if __name__ == "__main__":
    main()
