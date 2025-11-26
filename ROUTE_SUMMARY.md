# Route from Kateel to Udupi (Toll-Free)

## Quick Answer

Based on routing analysis, the **nearest route from Kateel to Udupi is approximately 38.08 km** and takes about **39 minutes** of driving time.

## Route Details

- **Start**: Kateel (13.09°N, 74.85°E)
- **End**: Udupi (13.34°N, 74.75°E)
- **Distance**: ~38.08 km
- **Estimated Duration**: ~39 minutes
- **Route Points**: 720 coordinate points

## Important Note About Tolls

The OSRM routing service (used in `find_route.py`) doesn't provide toll information. To get accurate **toll-free routes**, you have two options:

### Option 1: Use Google Maps API (Recommended for Toll-Free Routes)

1. **Get a Google Maps API Key**:
   - Visit: https://console.cloud.google.com/google/maps-apis
   - Create a project or select an existing one
   - Enable the "Directions API"
   - Create credentials (API key)

2. **Set the API Key**:
   ```bash
   export GOOGLE_MAPS_API_KEY='your-api-key-here'
   ```

3. **Run the Google Maps script**:
   ```bash
   python3 find_route_google_maps.py
   ```

This script specifically requests routes that avoid tolls using the `avoid=tolls` parameter.

### Option 2: Use OpenRouteService API

OpenRouteService also supports toll avoidance. You would need to:
1. Get a free API key from https://openrouteservice.org/
2. Modify the script to use their API with `avoid_features=tollways`

## Manual Check

For immediate results, you can also:
1. Open Google Maps
2. Search for directions from "Kateel, Karnataka" to "Udupi, Karnataka"
3. Click "Options" → Select "Avoid tolls"
4. Google Maps will show you the toll-free route

## Route Files Generated

- `route_data.json` - Route data from OSRM (includes geometry and steps)
- `route_data_google.json` - Route data from Google Maps API (if you use the Google Maps script)

## Typical Toll-Free Route

Based on the geography of Karnataka, a toll-free route from Kateel to Udupi typically follows:
- State highways and district roads
- Avoids NH-66 (which has tolls)
- Goes through smaller towns and villages
- May be slightly longer than toll routes but avoids toll charges

The exact route depends on current road conditions and Google Maps' real-time data.
