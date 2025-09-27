import requests
import os
import json
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MovieIDCollector:
    def __init__(self):
        self.tmdb_token = os.getenv('TMDB_BEARER_TOKEN')
        if not self.tmdb_token:
            raise ValueError("TMDB_BEARER_TOKEN not found in environment variables")
    
    def get_popular_movies(self, page=1):
        """Get popular movies from TMDB API"""
        url = f"https://api.themoviedb.org/3/movie/popular?page={page}"
        headers = {
            "Authorization": f"Bearer {self.tmdb_token}",
            "accept": "application/json"
        }
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"TMDB API error for page {page}: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Request failed for page {page}: {e}")
            return None
    
    def get_top_rated_movies(self, page=1):
        """Get top rated movies from TMDB API"""
        url = f"https://api.themoviedb.org/3/movie/top_rated?page={page}"
        headers = {
            "Authorization": f"Bearer {self.tmdb_token}",
            "accept": "application/json"
        }
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"TMDB API error for top rated page {page}: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Request failed for top rated page {page}: {e}")
            return None
    
    def get_now_playing_movies(self, page=1):
        """Get now playing movies from TMDB API"""
        url = f"https://api.themoviedb.org/3/movie/now_playing?page={page}"
        headers = {
            "Authorization": f"Bearer {self.tmdb_token}",
            "accept": "application/json"
        }
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"TMDB API error for now playing page {page}: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Request failed for now playing page {page}: {e}")
            return None
    
    def get_upcoming_movies(self, page=1):
        """Get upcoming movies from TMDB API"""
        url = f"https://api.themoviedb.org/3/movie/upcoming?page={page}"
        headers = {
            "Authorization": f"Bearer {self.tmdb_token}",
            "accept": "application/json"
        }
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"TMDB API error for upcoming page {page}: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Request failed for upcoming page {page}: {e}")
            return None
    
    def discover_movies(self, page=1, sort_by="popularity.desc", min_vote_count=100):
        """Discover movies with specific criteria"""
        url = f"https://api.themoviedb.org/3/discover/movie"
        params = {
            "page": page,
            "sort_by": sort_by,
            "vote_count.gte": min_vote_count,
            "include_adult": "false"
        }
        headers = {
            "Authorization": f"Bearer {self.tmdb_token}",
            "accept": "application/json"
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"TMDB Discover API error for page {page}: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Discover request failed for page {page}: {e}")
            return None
    
    def collect_movie_ids(self, target_count=500):
        """Collect movie IDs from various endpoints"""
        movie_ids = set()  # Use set to avoid duplicates
        movie_details = []  # Store basic movie info
        
        # Collection strategies with different endpoints
        strategies = [
            ("popular", self.get_popular_movies),
            ("top_rated", self.get_top_rated_movies),
            ("now_playing", self.get_now_playing_movies),
            ("upcoming", self.get_upcoming_movies),
            ("discover_popularity", lambda page: self.discover_movies(page, "popularity.desc")),
            ("discover_rating", lambda page: self.discover_movies(page, "vote_average.desc")),
            ("discover_revenue", lambda page: self.discover_movies(page, "revenue.desc")),
            ("discover_release", lambda page: self.discover_movies(page, "release_date.desc"))
        ]
        
        for strategy_name, strategy_func in strategies:
            logger.info(f"Collecting from {strategy_name}...")
            page = 1
            
            while len(movie_ids) < target_count and page <= 25:  # TMDB limits to 500 pages, but 25 should be enough
                data = strategy_func(page)
                
                if not data or 'results' not in data:
                    break
                
                for movie in data['results']:
                    if len(movie_ids) >= target_count:
                        break
                    
                    movie_id = movie['id']
                    if movie_id not in movie_ids:
                        movie_ids.add(movie_id)
                        movie_details.append({
                            'id': movie_id,
                            'title': movie['title'],
                            'release_date': movie.get('release_date', ''),
                            'vote_average': movie.get('vote_average', 0),
                            'popularity': movie.get('popularity', 0),
                            'source': strategy_name
                        })
                
                page += 1
                logger.info(f"{strategy_name}: Collected {len(movie_ids)} unique movies so far")
                
                if len(movie_ids) >= target_count:
                    break
            
            if len(movie_ids) >= target_count:
                break
        
        return list(movie_ids), movie_details
    
    def save_movie_ids(self, movie_ids, movie_details, filename="movie_ids_500.json"):
        """Save movie IDs and details to JSON file"""
        data = {
            "total_movies": len(movie_ids),
            "movie_ids": movie_ids,
            "movie_details": movie_details,
            "collection_date": "2025-09-26"
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(movie_ids)} movie IDs to {filename}")
    
    def save_ids_for_scrapper(self, movie_ids, filename="movie_ids_for_scrapper.py"):
        """Save movie IDs in Python format for the scrapper"""
        content = f"""# Auto-generated movie IDs for TMDB scrapper
# Generated on 2025-09-26
# Total movies: {len(movie_ids)}

MOVIE_IDS = {movie_ids}

# Split into batches of 50 for processing
BATCH_SIZE = 50
MOVIE_BATCHES = [MOVIE_IDS[i:i+BATCH_SIZE] for i in range(0, len(MOVIE_IDS), BATCH_SIZE)]

print(f"Total movies: {{len(MOVIE_IDS)}}")
print(f"Total batches: {{len(MOVIE_BATCHES)}}")
"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"Saved movie IDs for scrapper to {filename}")

def main():
    """Main execution function"""
    collector = MovieIDCollector()
    
    logger.info("Starting to collect 500 movie IDs from TMDB...")
    
    # Collect movie IDs
    movie_ids, movie_details = collector.collect_movie_ids(target_count=500)
    
    logger.info(f"✓ Collected {len(movie_ids)} unique movie IDs")
    
    # Save to JSON file
    collector.save_movie_ids(movie_ids, movie_details)
    
    # Save for scrapper usage
    collector.save_ids_for_scrapper(movie_ids)
    
    # Display some statistics
    sources = {}
    for detail in movie_details:
        source = detail['source']
        sources[source] = sources.get(source, 0) + 1
    
    logger.info("Collection sources breakdown:")
    for source, count in sources.items():
        logger.info(f"  {source}: {count} movies")
    
    logger.info("✓ Movie ID collection completed successfully")
    
    return movie_ids

if __name__ == "__main__":
    movie_ids = main()
    print(f"\nFirst 20 movie IDs: {movie_ids[:20]}")