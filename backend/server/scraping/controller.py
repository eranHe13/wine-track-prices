from concurrent.futures import ThreadPoolExecutor, as_completed
from . import haturki, paneco, wineroute

def scrape_all_sites(wine_name):
    results = {}
    sites = {"haturki": haturki, "paneco": paneco, "wineroute": wineroute}

    with ThreadPoolExecutor() as executor:
        future_to_site = {executor.submit(site.scrape, wine_name): site_name for site_name, site in sites.items()}
        
        for future in as_completed(future_to_site):
            site_name = future_to_site[future]
            try:
                results[site_name] = future.result()
            except Exception as e:
                results[site_name] = {"error": str(e)}

    return results

# Example usage
if __name__ == "__main__":
    wine_name = "Merlot"
    all_results = scrape_all_sites(wine_name)
    print(all_results)
