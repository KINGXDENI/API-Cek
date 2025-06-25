import json
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


class ScraperAPI:
    BASE_URL = "https://www.bukalapak.com/"
    API_URL = "https://api.bukalapak.com/"

    def __init__(self):
        self.access_token = None

    def _get_access_token(self, url):
        try:
            # Inisialisasi UserAgent dengan fallback
            ua = UserAgent(browsers=['firefox', 'chrome', 'edge'])
            try:
                user_agent = ua.random
            except Exception as e:
                print(f"Error occurred in fake_useragent: {e}")
                user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"  # Fallback

            # Menggunakan headers dengan User-Agent yang dipilih
            response = requests.get(
                url=self.BASE_URL + url,
                headers={"User-Agent": user_agent}
            )
            soup = BeautifulSoup(response.text, "html.parser")
            access_token = soup.findAll("script")[3].text.replace("localStorage.setItem('bl_token', '", "").replace("');", "")

            self.access_token = json.loads(access_token)['access_token']
            return self.access_token

        except IndexError:
            print("Error: IndexError occurred while parsing access token.")
            return None

        except json.decoder.JSONDecodeError:
            print("Error: JSONDecodeError occurred while decoding response.")
            return None

        except requests.exceptions.ConnectionError:
            print("Error: ConnectionError occurred while making the request.")
            return None
