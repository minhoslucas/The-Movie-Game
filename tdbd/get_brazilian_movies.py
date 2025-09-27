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

class BrazilianMovieCollector:
    def __init__(self):
        self.tmdb_token = os.getenv('TMDB_BEARER_TOKEN')
        if not self.tmdb_token:
            raise ValueError("TMDB_BEARER_TOKEN not found in environment variables")
    
    def discover_brazilian_movies(self, page=1, sort_by="popularity.desc", min_vote_count=10):
        """Discover Brazilian movies using TMDB API"""
        url = "https://api.themoviedb.org/3/discover/movie"
        params = {
            "page": page,
            "sort_by": sort_by,
            "with_origin_country": "BR",  # Brazil country code
            "vote_count.gte": min_vote_count,
            "include_adult": "false",
            "language": "pt-BR"  # Portuguese (Brazil)
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
                logger.error(f"TMDB Discover API error for Brazilian movies page {page}: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Brazilian movies request failed for page {page}: {e}")
            return None
    
    def search_brazilian_movies(self, query="brasil", page=1):
        """Search for Brazilian movies by query"""
        url = "https://api.themoviedb.org/3/search/movie"
        params = {
            "query": query,
            "page": page,
            "language": "pt-BR",
            "region": "BR",
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
                logger.error(f"TMDB Search API error for query '{query}' page {page}: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Search request failed for query '{query}' page {page}: {e}")
            return None
    
    def get_movie_details(self, movie_id):
        """Get detailed movie information to verify Brazilian origin"""
        url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        headers = {
            "Authorization": f"Bearer {self.tmdb_token}",
            "accept": "application/json"
        }
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Movie details API error for ID {movie_id}: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Movie details request failed for ID {movie_id}: {e}")
            return None
    
    def is_brazilian_movie(self, movie_details):
        """Check if movie is truly Brazilian based on production countries"""
        if not movie_details:
            return False
        
        production_countries = movie_details.get('production_countries', [])
        for country in production_countries:
            if country.get('iso_3166_1') == 'BR':
                return True
        
        # Also check original language
        original_language = movie_details.get('original_language', '')
        if original_language == 'pt':
            return True
        
        return False
    
    def collect_brazilian_movie_ids(self, target_count=100):
        """Collect Brazilian movie IDs from various strategies"""
        brazilian_movies = set()  # Use set to avoid duplicates
        movie_details_list = []  # Store detailed movie info
        
        # Strategy 1: Discover by origin country with different sorting
        discover_strategies = [
            ("popularity.desc", "Most Popular"),
            ("vote_average.desc", "Highest Rated"),
            ("release_date.desc", "Most Recent"),
            ("revenue.desc", "Highest Revenue")
        ]
        
        for sort_by, strategy_name in discover_strategies:
            logger.info(f"Collecting Brazilian movies by {strategy_name}...")
            page = 1
            
            while len(brazilian_movies) < target_count and page <= 50:
                data = self.discover_brazilian_movies(page, sort_by, min_vote_count=5)
                
                if not data or 'results' not in data or not data['results']:
                    break
                
                for movie in data['results']:
                    if len(brazilian_movies) >= target_count:
                        break
                    
                    movie_id = movie['id']
                    if movie_id not in brazilian_movies:
                        # Get detailed info to verify it's Brazilian
                        details = self.get_movie_details(movie_id)
                        
                        if self.is_brazilian_movie(details):
                            brazilian_movies.add(movie_id)
                            movie_details_list.append({
                                'id': movie_id,
                                'title': movie['title'],
                                'original_title': movie.get('original_title', ''),
                                'release_date': movie.get('release_date', ''),
                                'vote_average': movie.get('vote_average', 0),
                                'popularity': movie.get('popularity', 0),
                                'overview': movie.get('overview', ''),
                                'original_language': details.get('original_language', ''),
                                'production_countries': [country['name'] for country in details.get('production_countries', [])],
                                'strategy': f"discover_{sort_by}"
                            })
                            
                            logger.info(f"Found Brazilian movie: {movie['title']} ({movie_id})")
                
                page += 1
                logger.info(f"{strategy_name}: Found {len(brazilian_movies)} Brazilian movies so far")
                
                if len(brazilian_movies) >= target_count:
                    break
            
            if len(brazilian_movies) >= target_count:
                break
        
        # Strategy 2: Search with Brazilian-related terms if we need more
        if len(brazilian_movies) < target_count:
            search_terms = [
                "brazil", "brasil", "cinema brasileiro", "filme brasileiro",
                "rio de janeiro", "são paulo", "favela", "ditadura"
            ]
            
            for term in search_terms:
                if len(brazilian_movies) >= target_count:
                    break
                
                logger.info(f"Searching for movies with term: {term}")
                page = 1
                
                while len(brazilian_movies) < target_count and page <= 10:
                    data = self.search_brazilian_movies(term, page)
                    
                    if not data or 'results' not in data or not data['results']:
                        break
                    
                    for movie in data['results']:
                        if len(brazilian_movies) >= target_count:
                            break
                        
                        movie_id = movie['id']
                        if movie_id not in brazilian_movies:
                            details = self.get_movie_details(movie_id)
                            
                            if self.is_brazilian_movie(details):
                                brazilian_movies.add(movie_id)
                                movie_details_list.append({
                                    'id': movie_id,
                                    'title': movie['title'],
                                    'original_title': movie.get('original_title', ''),
                                    'release_date': movie.get('release_date', ''),
                                    'vote_average': movie.get('vote_average', 0),
                                    'popularity': movie.get('popularity', 0),
                                    'overview': movie.get('overview', ''),
                                    'original_language': details.get('original_language', ''),
                                    'production_countries': [country['name'] for country in details.get('production_countries', [])],
                                    'strategy': f"search_{term}"
                                })
                                
                                logger.info(f"Found Brazilian movie via search: {movie['title']} ({movie_id})")
                    
                    page += 1
                
                logger.info(f"Search '{term}': Found {len(brazilian_movies)} total Brazilian movies")
        
        return list(brazilian_movies), movie_details_list
    
    def save_brazilian_movies(self, movie_ids, movie_details, filename="brazilian_movies_100.json"):
        """Save Brazilian movie IDs and details to JSON file"""
        data = {
            "total_movies": len(movie_ids),
            "movie_ids": movie_ids,
            "movie_details": movie_details,
            "collection_date": "2025-09-26",
            "country": "Brazil (BR)",
            "description": "Collection of Brazilian movies from TMDB"
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(movie_ids)} Brazilian movie IDs to {filename}")
    
    def save_ids_for_scrapper(self, movie_ids, filename="brazilian_movies_for_scrapper.py"):
        """Save Brazilian movie IDs in Python format for the scrapper"""
        content = f"""# Auto-generated Brazilian movie IDs for TMDB scrapper
# Generated on 2025-09-26
# Total Brazilian movies: {len(movie_ids)}

BRAZILIAN_MOVIE_IDS = {movie_ids}

# Split into batches of 25 for processing (smaller batches for detailed movies)
BATCH_SIZE = 25
BRAZILIAN_MOVIE_BATCHES = [BRAZILIAN_MOVIE_IDS[i:i+BATCH_SIZE] for i in range(0, len(BRAZILIAN_MOVIE_IDS), BATCH_SIZE)]

print(f"Total Brazilian movies: {{len(BRAZILIAN_MOVIE_IDS)}}")
print(f"Total batches: {{len(BRAZILIAN_MOVIE_BATCHES)}}")
"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"Saved Brazilian movie IDs for scrapper to {filename}")

def main():
    """Main execution function for collecting Brazilian movies"""
    collector = BrazilianMovieCollector()
    
    logger.info("Starting to collect 100 Brazilian movie IDs from TMDB...")
    
    # Collect Brazilian movie IDs
    movie_ids, movie_details = collector.collect_brazilian_movie_ids(target_count=100)
    
    logger.info(f"✓ Collected {len(movie_ids)} unique Brazilian movie IDs")
    
    # Save to JSON file
    collector.save_brazilian_movies(movie_ids, movie_details)
    
    # Save for scrapper usage
    collector.save_ids_for_scrapper(movie_ids)
    
    # Display some statistics
    strategies = {}
    languages = {}
    decades = {}
    
    for detail in movie_details:
        # Strategy breakdown
        strategy = detail['strategy']
        strategies[strategy] = strategies.get(strategy, 0) + 1
        
        # Language breakdown
        lang = detail.get('original_language', 'unknown')
        languages[lang] = languages.get(lang, 0) + 1
        
        # Decade breakdown
        release_date = detail.get('release_date', '')
        if release_date and len(release_date) >= 4:
            year = int(release_date[:4])
            decade = f"{(year // 10) * 10}s"
            decades[decade] = decades.get(decade, 0) + 1
    
    logger.info("Collection strategies breakdown:")
    for strategy, count in strategies.items():
        logger.info(f"  {strategy}: {count} movies")
    
    logger.info("Languages breakdown:")
    for lang, count in languages.items():
        logger.info(f"  {lang}: {count} movies")
    
    logger.info("Decades breakdown:")
    for decade, count in sorted(decades.items()):
        logger.info(f"  {decade}: {count} movies")
    
    # Show top 10 movies by popularity
    top_movies = sorted(movie_details, key=lambda x: x['popularity'], reverse=True)[:10]
    logger.info("Top 10 most popular Brazilian movies found:")
    for i, movie in enumerate(top_movies, 1):
        logger.info(f"  {i}. {movie['title']} ({movie['release_date'][:4] if movie['release_date'] else 'N/A'}) - Rating: {movie['vote_average']}")
    
    logger.info("✓ Brazilian movie ID collection completed successfully")
    
    return movie_ids

if __name__ == "__main__":
    movie_ids = main()
    print(f"\nTotal Brazilian movies collected: {len(movie_ids)}")
    print(f"First 10 Brazilian movie IDs: {movie_ids[:10]}")