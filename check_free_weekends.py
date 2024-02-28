import os
import requests

def check_free_weekends():
    # Retrieve Steam API key from environment variables
    steam_api_key = os.environ.get('STEAM_API_KEY')
    
    # Check if API key is available
    if steam_api_key is None:
        print("Error: Steam API key not found. Make sure to set up the STEAM_API_KEY secret in your GitHub repository.")
        return
    
    # URL for the Steam store API to retrieve information about games
    url = "http://api.steampowered.com/ISteamApps/GetAppList/v2"

    # Request the list of apps from the Steam store API
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        
        # Extract list of apps
        apps = data["applist"]["apps"]
        
        # Check for free weekends
        free_weekend_apps = []
        for app in apps:
            if "name" in app:
                app_name = app["name"]
                # Check if the app name contains "Free Weekend"
                if "Free Weekend" in app_name:
                    app_id = app["appid"]
                    # URL for the Steam store API to retrieve detailed information about a specific app
                    app_url = f"http://store.steampowered.com/api/appdetails?appids={app_id}&cc=us"
                    # Request app details from the Steam store API
                    app_response = requests.get(app_url)
                    # Check if the request was successful
                    if app_response.status_code == 200:
                        app_data = app_response.json().get(str(app_id))
                        # Check if the app ID is present in the response
                        if app_data:
                            app_info = app_data.get("data")
                            # Check if the app is currently having a free weekend
                            if app_info and app_info.get("is_free_weekend"):
                                # Extract start and end dates of the free weekend
                                start_date = app_info.get("start_date", "Unknown")
                                end_date = app_info.get("end_date", "Unknown")
                                free_weekend_apps.append((app_name, {"start_date": start_date, "end_date": end_date}))
        
        # Generate Markdown content for README.md
        markdown_content = ""
        if free_weekend_apps:
            markdown_content += "## Free Weekends\n\n"
            for app_name, info in free_weekend_apps:
                markdown_content += f"### {app_name}\n"
                markdown_content += f"**Start Date:** {info['start_date']}\n"
                markdown_content += f"**End Date:** {info['end_date']}\n\n"
        else:
            markdown_content += "## No Free Weekends\n\n"
        
        # Write Markdown content to README.md file
        with open("README.md", "w") as readme_file:
            readme_file.write(markdown_content)
        
        print("README.md generated successfully.")
    else:
        print("Failed to retrieve data from the Steam store API.")

if __name__ == "__main__":
    check_free_weekends()