#!/usr/bin/env python3
"""
Script to find the nearest route from Kateel to Udupi without tolls.
Uses OSRM (Open Source Routing Machine) API for routing.
"""

import requests
import json
from typing import Dict, List, Optional

# Coordinates for Kateel and Udupi (Karnataka, India)
KATEEL_COORDS = [74.85, 13.09]  # [longitude, latitude]
UDUPI_COORDS = [74.75, 13.34]   # [longitude, latitude]

# OSRM public demo server (you can also use your own instance)
OSRM_BASE_URL = "http://router.project-osrm.org/route/v1/driving"


def get_route_without_tolls(start: List[float], end: List[float]) -> Optional[Dict]:
    """
    Get route from start to end coordinates using OSRM.
    Note: OSRM doesn't directly support toll avoidance, but we can get alternative routes
    and check them. For toll avoidance, you'd need Google Maps API or similar.
    """
    # Format: longitude,latitude;longitude,latitude
    coordinates = f"{start[0]},{start[1]};{end[0]},{end[1]}"
    
    # Request parameters
    params = {
        'overview': 'full',
        'geometries': 'geojson',
        'alternatives': 'true',  # Get alternative routes
        'steps': 'true'
    }
    
    url = f"{OSRM_BASE_URL}/{coordinates}"
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching route: {e}")
        return None


def format_distance(distance_meters: float) -> str:
    """Convert distance from meters to kilometers."""
    if distance_meters < 1000:
        return f"{distance_meters:.0f} meters"
    return f"{distance_meters / 1000:.2f} km"


def format_duration(duration_seconds: float) -> str:
    """Convert duration from seconds to hours and minutes."""
    hours = int(duration_seconds // 3600)
    minutes = int((duration_seconds % 3600) // 60)
    if hours > 0:
        return f"{hours}h {minutes}m"
    return f"{minutes}m"


def print_route_info(route_data: Dict):
    """Print route information in a readable format."""
    if route_data.get('code') != 'Ok':
        print(f"Error: {route_data.get('message', 'Unknown error')}")
        return
    
    routes = route_data.get('routes', [])
    if not routes:
        print("No routes found.")
        return
    
    print(f"\n{'='*60}")
    print(f"Found {len(routes)} route(s) from Kateel to Udupi")
    print(f"{'='*60}\n")
    
    for i, route in enumerate(routes, 1):
        distance = route.get('distance', 0)
        duration = route.get('duration', 0)
        geometry = route.get('geometry', {})
        
        print(f"Route {i}:")
        print(f"  Distance: {format_distance(distance)}")
        print(f"  Duration: {format_duration(duration)}")
        print(f"  Coordinates: {len(geometry.get('coordinates', []))} points")
        
        # Get steps if available
        legs = route.get('legs', [])
        if legs:
            steps = legs[0].get('steps', [])
            if steps:
                print(f"  Number of steps: {len(steps)}")
                print(f"\n  First few steps:")
                for j, step in enumerate(steps[:5], 1):
                    step_distance = format_distance(step.get('distance', 0))
                    step_duration = format_duration(step.get('duration', 0))
                    maneuver = step.get('maneuver', {}).get('type', 'unknown')
                    print(f"    {j}. {maneuver} - {step_distance} ({step_duration})")
                if len(steps) > 5:
                    print(f"    ... and {len(steps) - 5} more steps")
        
        print()


def main():
    """Main function to find and display routes."""
    print("Finding route from Kateel to Udupi...")
    print(f"Start: Kateel ({KATEEL_COORDS[1]}, {KATEEL_COORDS[0]})")
    print(f"End: Udupi ({UDUPI_COORDS[1]}, {UDUPI_COORDS[0]})")
    
    route_data = get_route_without_tolls(KATEEL_COORDS, UDUPI_COORDS)
    
    if route_data:
        print_route_info(route_data)
        
        # Save route data to JSON file
        with open('route_data.json', 'w') as f:
            json.dump(route_data, f, indent=2)
        print("\nRoute data saved to 'route_data.json'")
        
        print("\n" + "="*60)
        print("NOTE: OSRM doesn't provide toll information.")
        print("For accurate toll-free routes, consider using:")
        print("  - Google Maps API (with avoid=tolls parameter)")
        print("  - OpenRouteService API (with avoid_features=tollways)")
        print("="*60)
    else:
        print("Failed to retrieve route information.")


if __name__ == "__main__":
    main()
