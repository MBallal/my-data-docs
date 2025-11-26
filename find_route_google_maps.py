#!/usr/bin/env python3
"""
Alternative script using Google Maps API to find toll-free routes.
Requires Google Maps API key with Directions API enabled.
"""

import requests
import json
import os
from typing import Dict, Optional

# Coordinates for Kateel and Udupi (Karnataka, India)
KATEEL_COORDS = "13.09,74.85"  # latitude,longitude
UDUPI_COORDS = "13.34,74.75"   # latitude,longitude

# Google Maps Directions API endpoint
GOOGLE_MAPS_API_URL = "https://maps.googleapis.com/maps/api/directions/json"


def get_toll_free_route(start: str, end: str, api_key: str) -> Optional[Dict]:
    """
    Get toll-free route from start to end using Google Maps API.
    
    Args:
        start: Starting coordinates as "latitude,longitude"
        end: Ending coordinates as "latitude,longitude"
        api_key: Google Maps API key
    
    Returns:
        JSON response from Google Maps API
    """
    params = {
        'origin': start,
        'destination': end,
        'avoid': 'tolls',  # Avoid toll roads
        'alternatives': 'true',  # Get alternative routes
        'key': api_key
    }
    
    try:
        response = requests.get(GOOGLE_MAPS_API_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching route: {e}")
        return None


def format_distance(distance_text: str) -> str:
    """Return distance as-is (already formatted by Google Maps)."""
    return distance_text


def format_duration(duration_text: str) -> str:
    """Return duration as-is (already formatted by Google Maps)."""
    return duration_text


def print_route_info(route_data: Dict):
    """Print route information in a readable format."""
    if route_data.get('status') != 'OK':
        print(f"Error: {route_data.get('status')} - {route_data.get('error_message', 'Unknown error')}")
        return
    
    routes = route_data.get('routes', [])
    if not routes:
        print("No routes found.")
        return
    
    print(f"\n{'='*60}")
    print(f"Found {len(routes)} toll-free route(s) from Kateel to Udupi")
    print(f"{'='*60}\n")
    
    for i, route in enumerate(routes, 1):
        legs = route.get('legs', [])
        if not legs:
            continue
        
        total_distance = sum(leg.get('distance', {}).get('value', 0) for leg in legs)
        total_duration = sum(leg.get('duration', {}).get('value', 0) for leg in legs)
        
        # Get formatted distance and duration from first leg
        distance_text = legs[0].get('distance', {}).get('text', 'Unknown')
        duration_text = legs[0].get('duration', {}).get('text', 'Unknown')
        
        # Calculate total formatted values
        if len(legs) > 1:
            # Sum up all distances and durations
            total_distance_km = total_distance / 1000
            total_duration_hours = total_duration / 3600
            
            if total_distance_km < 1:
                distance_text = f"{total_distance:.0f} m"
            else:
                distance_text = f"{total_distance_km:.2f} km"
            
            if total_duration_hours < 1:
                duration_text = f"{int(total_duration / 60)} min"
            else:
                hours = int(total_duration_hours)
                minutes = int((total_duration % 3600) / 60)
                duration_text = f"{hours}h {minutes}min"
        
        print(f"Route {i}:")
        print(f"  Distance: {distance_text}")
        print(f"  Duration: {duration_text}")
        
        # Print summary
        summary = route.get('summary', 'No summary available')
        print(f"  Summary: {summary}")
        
        # Print steps
        steps = legs[0].get('steps', [])
        if steps:
            print(f"  Number of steps: {len(steps)}")
            print(f"\n  First few steps:")
            for j, step in enumerate(steps[:5], 1):
                step_distance = step.get('distance', {}).get('text', 'Unknown')
                step_duration = step.get('duration', {}).get('text', 'Unknown')
                instruction = step.get('html_instructions', 'No instruction')
                # Remove HTML tags for cleaner output
                import re
                instruction = re.sub('<[^<]+?>', '', instruction)
                print(f"    {j}. {instruction}")
                print(f"       {step_distance} ({step_duration})")
            if len(steps) > 5:
                print(f"    ... and {len(steps) - 5} more steps")
        
        print()


def main():
    """Main function to find and display toll-free routes."""
    # Get API key from environment variable
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    
    if not api_key:
        print("="*60)
        print("Google Maps API key not found!")
        print("="*60)
        print("\nTo use this script:")
        print("1. Get a Google Maps API key from:")
        print("   https://console.cloud.google.com/google/maps-apis")
        print("2. Enable the Directions API")
        print("3. Set the API key as an environment variable:")
        print("   export GOOGLE_MAPS_API_KEY='your-api-key-here'")
        print("4. Run the script again")
        print("\nAlternatively, use find_route.py which uses OSRM (free, no API key)")
        print("="*60)
        return
    
    print("Finding toll-free route from Kateel to Udupi using Google Maps API...")
    print(f"Start: Kateel ({KATEEL_COORDS})")
    print(f"End: Udupi ({UDUPI_COORDS})")
    
    route_data = get_toll_free_route(KATEEL_COORDS, UDUPI_COORDS, api_key)
    
    if route_data:
        print_route_info(route_data)
        
        # Save route data to JSON file
        with open('route_data_google.json', 'w') as f:
            json.dump(route_data, f, indent=2)
        print("\nRoute data saved to 'route_data_google.json'")
    else:
        print("Failed to retrieve route information.")


if __name__ == "__main__":
    main()
