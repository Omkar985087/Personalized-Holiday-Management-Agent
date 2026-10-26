import requests

def search_places(city:str):
    url="https://nominatim.openstreetmap.org/search"
    
    params={
        "q":city,
        "format":"jsonv2",
        "limit":1
    }
    
    headers={
       "User-Agent":"PersonalizedHolidayAgent/1.0"
    }
    
    response=requests.get(
        url,
        params=params,
        headers=headers,
        timeout=15   
    )
    
    response.raise_for_status()
    
    results=response.json()
    
    if not results:
        return []
    
    location=results[0]
    
    return [{
        "name": location["display_name"],
        "latitude": location["lat"],
        "longitude": location["lon"],
        "source": "OpenStreetMap",
        "url": "https://www.openstreetmap.org/"
    }]
    

import time
import requests

def find_attraction(longitude: float, latitude: float):
    url = "https://overpass-api.de/api/interpreter"

    query = f"""
    [out:json][timeout:15];
    node["tourism"~"^(attraction|museum)$"]
        (around:5000,{latitude},{longitude});
    out body 15;
    """

    headers = {
        "User-Agent": "PersonalizedHolidayAgent/1.0",
        "Accept": "application/json"
    }

    for attempt in range(3):
        try:
            response = requests.post(
                url,
                data={"data": query},
                headers=headers,
                timeout=30
            )

            if response.status_code in (429, 502, 503, 504):
                if attempt < 2:
                    wait_seconds = 2 ** (attempt + 1)
                    print(
                        f"Overpass busy. Retrying in "
                        f"{wait_seconds} seconds..."
                    )
                    time.sleep(wait_seconds)
                    continue

            response.raise_for_status()
            elements = response.json().get("elements", [])
            attractions = []

            for element in elements:
                tags = element.get("tags", {})
                name = tags.get("name")

                if not name:
                    continue

                attractions.append({
                    "name": name,
                    "longitude": element.get("lon"),
                    "latitude": element.get("lat"),
                    "category": tags.get("tourism"),
                    "source": "OpenStreetMap",
                    "url": (
                        "https://www.openstreetmap.org/"
                        f"{element['type']}/{element['id']}"
                    )
                })

            return attractions

        except requests.RequestException as error:
            if attempt == 2:
                print(f"Attraction search failed: {error}")
                return []

            wait_seconds = 2 ** (attempt + 1)
            print(f"Request failed. Retrying in {wait_seconds} seconds...")
            time.sleep(wait_seconds)

    return []

    
if __name__ == "__main__":
    locations = search_places("Tokyo, Japan")
    
    if locations:
        tokyo=locations[0]
        
        attractions=find_attraction(
            float(tokyo["longitude"]),
            float(tokyo["latitude"])
        )
        
        for places in attractions:
            print(places)
            
    else:
        print("Location not found.")