import httpx

async def fetch_hotels_from_api(sw_lat, sw_lon, ne_lat, ne_lon, session):
    """
    Calls a hotel provider API to get properties within a specific box.
    """
    api_url = "https://api.provider.com/v1/hotels/search"
    params = {
        "box": f"{sw_lat},{sw_lon},{ne_lat},{ne_lon}",
        "types": "hotel,hostel,motel,guest_house", # Excludes vacation rentals
        "fields": "id,name,location,images,rating,reviews"
    }

    try:
        response = await session.get(api_url, params=params, timeout=10.0)
        response.raise_for_status()
        data = response.json()

        # Extracting the specific fields the client wants
        extracted_data = []
        for item in data.get("properties", []):
            extracted_data.append({
                "id": item.get("id"),
                "name": item.get("name"),
                "lat": item.get("location", {}).get("lat"),
                "lon": item.get("location", {}).get("lon"),
                "star_rating": item.get("stars"),
                "user_rating": item.get("score"),
                "review_count": item.get("reviews_count"),
                "images": [img['url'] for img in item.get("images", [])],
                "image_tags": [img['label'] for img in item.get("images", [])] # Critical field
            })
        return extracted_data

    except Exception as e:
        print(f"Error fetching data for box {sw_lat},{sw_lon}: {e}")
        return []

def split_bounding_box(sw_lat, sw_lon, ne_lat, ne_lon):
    """
    Splits one bounding box into 4 smaller quadrants.
    """
    mid_lat = (sw_lat + ne_lat) / 2
    mid_lon = (sw_lon + ne_lon) / 2

    return {
        "NW": (mid_lat, sw_lon, ne_lat, mid_lon),
        "NE": (mid_lat, mid_lon, ne_lat, ne_lon),
        "SW": (sw_lat, sw_lon, mid_lat, mid_lon),
        "SE": (sw_lat, mid_lon, mid_lat, ne_lon)
    }

async def recursive_search(sw_lat, sw_lon, ne_lat, ne_lon, session):
    # 1. Get hotels in this box
    results = await fetch_hotels_from_api(sw_lat, sw_lon, ne_lat, ne_lon, session)
    
    # 2. Check if we hit the limit (e.g., 50 hotels)
    if len(results) >= 50:
        print("High density area found! Splitting box...")
        quadrants = split_bounding_box(sw_lat, sw_lon, ne_lat, ne_lon)
        
        all_sub_results = []
        for quad in quadrants.values():
            # Recursively zoom in
            sub_results = await recursive_search(*quad, session)
            all_sub_results.extend(sub_results)
        return all_sub_results
    
    return results