import requests
import json
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TMDBScrapper:
    def __init__(self):
        self.tmdb_token = os.getenv('TMDB_BEARER_TOKEN')
        self.db_url = os.getenv('DATABASE_URL')
        self.connection = None
        
        if not self.tmdb_token:
            raise ValueError("TMDB_BEARER_TOKEN not found in environment variables")
        if not self.db_url:
            raise ValueError("DATABASE_URL not found in environment variables")
    
    def connect_db(self):
        """Connect to Neon PostgreSQL database"""
        try:
            self.connection = psycopg2.connect(
                self.db_url,
                cursor_factory=RealDictCursor
            )
            logger.info("✓ Connected to Neon PostgreSQL database")
            return True
        except Exception as e:
            logger.error(f"✗ Database connection failed: {e}")
            return False
    
    def close_db(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")
    
    def execute_query(self, query, params=None):
        """Execute a single query"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                self.connection.commit()
                return True
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            self.connection.rollback()
            return False
    
    def execute_batch_queries(self, queries):
        """Execute multiple queries in a transaction"""
        try:
            with self.connection.cursor() as cursor:
                # Set search path
                cursor.execute("SET search_path TO movies_data;")
                
                for query_info in queries:
                    if isinstance(query_info, dict):
                        cursor.execute(query_info['query'], query_info.get('params'))
                    else:
                        cursor.execute(query_info)
                
                self.connection.commit()
                logger.info(f"✓ Executed {len(queries)} queries successfully")
                return True
        except Exception as e:
            logger.error(f"Batch query execution failed: {e}")
            self.connection.rollback()
            return False
    
    def get_movie_by_id(self, movie_id):
        """Fetch movie data from TMDB API"""
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
                logger.error(f"TMDB API error for movie {movie_id}: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Request failed for movie {movie_id}: {e}")
            return None
    
    def get_movie_credits(self, movie_id):
        """Get movie credits from TMDB API"""
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
        headers = {
            "Authorization": f"Bearer {self.tmdb_token}",
            "accept": "application/json"
        }
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"TMDB Credits API error for movie {movie_id}: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Credits request failed for movie {movie_id}: {e}")
            return None
    
    def escape_sql_string(self, value):
        """Escape single quotes and handle None values for SQL"""
        if value is None:
            return ''
        return str(value).replace("'", "''")
    
    def insert_movie_data(self, movie_data):
        """Insert movie data into database"""
        queries = []
        
        # Movie insert
        movie_query = """
        INSERT INTO movie (movie_id, title, release_date, duration_minutes, rating, synopsis, overview, adult, budget, revenue, tagline) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (movie_id) DO UPDATE SET
            title = EXCLUDED.title,
            release_date = EXCLUDED.release_date,
            duration_minutes = EXCLUDED.duration_minutes,
            rating = EXCLUDED.rating,
            synopsis = EXCLUDED.synopsis,
            overview = EXCLUDED.overview,
            adult = EXCLUDED.adult,
            budget = EXCLUDED.budget,
            revenue = EXCLUDED.revenue,
            tagline = EXCLUDED.tagline
        """
        
        movie_params = (
            movie_data['id'],
            movie_data['title'],
            movie_data['release_date'],
            movie_data.get('runtime', 0),
            movie_data.get('vote_average', 0),
            movie_data.get('overview', ''),
            movie_data.get('overview', ''),
            movie_data.get('adult', False),
            movie_data.get('budget', 0),
            movie_data.get('revenue', 0),
            movie_data.get('tagline', '')
        )
        
        queries.append({'query': movie_query, 'params': movie_params})
        
        # Genres
        if movie_data.get('genres'):
            for genre in movie_data['genres']:
                # Insert genre
                genre_query = "INSERT INTO genre (genre_id, genre_name) VALUES (%s, %s) ON CONFLICT (genre_id) DO NOTHING"
                queries.append({'query': genre_query, 'params': (genre['id'], genre['name'])})
                
                # Insert movie-genre relationship
                movie_genre_query = "INSERT INTO movie_genre (movie_id, genre_id) VALUES (%s, %s) ON CONFLICT DO NOTHING"
                queries.append({'query': movie_genre_query, 'params': (movie_data['id'], genre['id'])})
        
        # Production Companies as Producers
        if movie_data.get('production_companies'):
            for i, company in enumerate(movie_data['production_companies']):
                # Insert producer
                producer_query = "INSERT INTO producer (producer_id, company_name, origin_country) VALUES (%s, %s, %s) ON CONFLICT (producer_id) DO NOTHING"
                queries.append({'query': producer_query, 'params': (company['id'], company['name'], company.get('origin_country', ''))})
                
                # Update movie with first producer
                if i == 0:
                    update_movie_query = "UPDATE movie SET producer_id = %s WHERE movie_id = %s"
                    queries.append({'query': update_movie_query, 'params': (company['id'], movie_data['id'])})
        
        return queries
    
    def insert_credits_data(self, movie_id, credits_data):
        """Insert credits data into database"""
        queries = []
        
        # Actors
        if credits_data.get('cast'):
            for actor in credits_data['cast'][:10]:  # Limit to top 10 actors
                # Insert actor
                actor_query = "INSERT INTO actor (actor_id, name) VALUES (%s, %s) ON CONFLICT (actor_id) DO NOTHING"
                queries.append({'query': actor_query, 'params': (actor['id'], actor['name'])})
                
                # Insert movie-actor relationship
                acted_in_query = "INSERT INTO acted_in (movie_id, actor_id) VALUES (%s, %s) ON CONFLICT DO NOTHING"
                queries.append({'query': acted_in_query, 'params': (movie_id, actor['id'])})
        
        # Directors and Writers
        if credits_data.get('crew'):
            for crew_member in credits_data['crew']:
                if crew_member['job'] == 'Director':
                    # Insert director
                    director_query = "INSERT INTO director (director_id, full_name) VALUES (%s, %s) ON CONFLICT (director_id) DO NOTHING"
                    queries.append({'query': director_query, 'params': (crew_member['id'], crew_member['name'])})
                    
                    # Insert movie-director relationship
                    movie_director_query = "INSERT INTO movie_director (movie_id, director_id) VALUES (%s, %s) ON CONFLICT DO NOTHING"
                    queries.append({'query': movie_director_query, 'params': (movie_id, crew_member['id'])})
                
                elif crew_member['job'] in ['Writer', 'Screenplay', 'Story']:
                    # Insert writer
                    writer_query = "INSERT INTO writer (writer_id, full_name) VALUES (%s, %s) ON CONFLICT (writer_id) DO NOTHING"
                    queries.append({'query': writer_query, 'params': (crew_member['id'], crew_member['name'])})
                    
                    # Insert movie-writer relationship
                    movie_writer_query = "INSERT INTO movie_writer (movie_id, writer_id) VALUES (%s, %s) ON CONFLICT DO NOTHING"
                    queries.append({'query': movie_writer_query, 'params': (movie_id, crew_member['id'])})
        
        return queries
    
    def process_movie(self, movie_id):
        """Process a single movie and insert into database"""
        logger.info(f"Processing movie ID: {movie_id}")
        
        # Fetch data from TMDB
        movie_data = self.get_movie_by_id(movie_id)
        credits_data = self.get_movie_credits(movie_id)
        
        if not movie_data:
            logger.error(f"Failed to fetch movie data for ID {movie_id}")
            return False
        
        # Prepare queries
        all_queries = []
        
        # Movie data queries
        movie_queries = self.insert_movie_data(movie_data)
        all_queries.extend(movie_queries)
        
        # Credits data queries
        if credits_data:
            credits_queries = self.insert_credits_data(movie_id, credits_data)
            all_queries.extend(credits_queries)
        
        # Execute all queries
        if self.execute_batch_queries(all_queries):
            logger.info(f"✓ Movie {movie_id} ({movie_data['title']}) processed successfully")
            return True
        else:
            logger.error(f"✗ Failed to process movie {movie_id}")
            return False
    
    def process_multiple_movies(self, movie_ids):
        """Process multiple movies"""
        if not self.connect_db():
            return False
        
        successful = 0
        failed = 0
        
        try:
            for movie_id in movie_ids:
                if self.process_movie(movie_id):
                    successful += 1
                else:
                    failed += 1
                
                logger.info(f"Progress: {successful + failed}/{len(movie_ids)} movies processed")
        
        finally:
            self.close_db()
        
        logger.info(f"Processing complete: {successful} successful, {failed} failed")
        return successful > 0

def main():
    """Main execution function"""
    # Initialize scrapper
    scrapper = TMDBScrapper()
    
    # Import movie IDs from the collector
    try:
        from brazilian_movies_for_scrapper import MOVIE_IDS, MOVIE_BATCHES
        logger.info(f"Loaded {len(MOVIE_IDS)} movie IDs from collector")
        
        # Process all movies in batches
        total_successful = 0
        total_failed = 0
        
        for batch_num, batch_ids in enumerate(MOVIE_BATCHES, 1):
            logger.info(f"Processing batch {batch_num}/{len(MOVIE_BATCHES)} ({len(batch_ids)} movies)")
            
            success = scrapper.process_multiple_movies(batch_ids)
            
            if success:
                total_successful += len(batch_ids)
                logger.info(f"✓ Batch {batch_num} completed successfully")
            else:
                total_failed += len(batch_ids)
                logger.error(f"✗ Batch {batch_num} failed")
            
            # Small delay between batches to respect API limits
            import time
            time.sleep(1)
        
        logger.info(f"Final results: {total_successful} successful, {total_failed} failed")
        
    except ImportError:
        # Fallback to original smaller list
        logger.warning("movie_ids_for_scrapper.py not found, using fallback movie IDs")
        movie_ids = [11, 550, 13, 120, 680, 155, 598, 24428, 27205, 475557]
        
        logger.info(f"Starting to process {len(movie_ids)} movies")
        success = scrapper.process_multiple_movies(movie_ids)
        
        if success:
            logger.info("✓ Processing completed successfully")
        else:
            logger.error("✗ Processing failed")

if __name__ == "__main__":
    main()