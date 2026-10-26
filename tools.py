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
    
if __name__ == "__main__":
    places = search_places("Tokyo, Japan")
    print(places)