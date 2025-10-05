import requests

def fetch_wfs(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()
        features = data.get('features', [])
        result = []
        for f in features:
            geom = f.get('geometry')
            props = f.get('properties', {})
            delay = props.get('czas_opoznienia') or props.get('expectedDelay') or None
            result.append({
                'source': 'WFS',
                'type': props.get('TYP', 'unknown'),
                'description': props.get('OPIS', ''),
                'geometry': geom,
                'delay_minutes': delay,
                'raw': f
            })
        return result
    except Exception as e:
        print("WFS fetch error:", e)
        return []