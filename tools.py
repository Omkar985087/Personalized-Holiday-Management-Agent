
import requests
import time

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

OVERPASS_URLS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]

HEADERS = {
    "User-Agent": "PersonalizedHolidayAgent/1.0",
    "Accept": "application/json",
}


def search_places(city: str):
    params = {
        "q": city,
        "format": "jsonv2",
        "limit": 1,
    }

    response = requests.get(
        NOMINATIM_URL,
        params=params,
        headers=HEADERS,
        timeout=15,
    )
    response.raise_for_status()

    results = response.json()

    if not results:
        return []

    location = results[0]

    return [{
        "name": location["display_name"],
        "latitude": location["lat"],
        "longitude": location["lon"],
        "source": "OpenStreetMap",
        "url": "https://www.openstreetmap.org/",
    }]


def find_attraction(longitude: float, latitude: float):
    query = f"""
    [out:json][timeout:15];
    node["tourism"~"^(attraction|museum)$"]
        (around:5000,{latitude},{longitude});
    out body 15;
    """

    for url in OVERPASS_URLS:
        try:
            print(f"Trying endpoint: {url}")

            response = requests.post(
                url,
                data={"data": query},
                headers=HEADERS,
                timeout=30,
            )

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
                    ),
                })

            return attractions

        except requests.RequestException as error:
            print(f"Endpoint failed: {error}")
            time.sleep(2)

    print("All Overpass endpoints failed.")
    return []


if __name__ == "__main__":
    locations = search_places("Tokyo, Japan")

    if not locations:
        print("Location not found.")
    else:
        tokyo = locations[0]

        attractions = find_attraction(
            float(tokyo["longitude"]),
            float(tokyo["latitude"]),
        )

        print(f"Found {len(attractions)} attractions")

        for place in attractions:
            print(place)
