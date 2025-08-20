"""
Sistema di Analytics per il ChatBot
Raccoglie metriche su performance e utilizzo
"""

import json
import time
from datetime import datetime
from pathlib import Path
import sqlite3

class ChatbotAnalytics:
    """Classe per raccogliere e analizzare metriche del chatbot"""
    
    def __init__(self, db_path="analytics.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inizializza il database SQLite per le metriche"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabella per le query
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            query TEXT NOT NULL,
            response TEXT,
            response_time REAL,
            documents_retrieved INTEGER,
            should_redirect BOOLEAN,
            user_satisfied BOOLEAN
        )
        ''')
        
        # Tabella per le performance
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS performance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            metric_name TEXT NOT NULL,
            metric_value REAL,
            details TEXT
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def log_query(self, query, response, response_time, docs_count, should_redirect):
        """Registra una query nel database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO queries 
        (query, response, response_time, documents_retrieved, should_redirect)
        VALUES (?, ?, ?, ?, ?)
        ''', (query, response, response_time, docs_count, should_redirect))
        
        conn.commit()
        conn.close()
    
    def log_performance(self, metric_name, value, details=None):
        """Registra una metrica di performance"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO performance (metric_name, metric_value, details)
        VALUES (?, ?, ?)
        ''', (metric_name, value, details))
        
        conn.commit()
        conn.close()
    
    def get_stats(self, days=7):
        """Ottiene statistiche degli ultimi N giorni"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Query totali
        cursor.execute('''
        SELECT COUNT(*) FROM queries 
        WHERE timestamp > datetime('now', '-{} days')
        '''.format(days))
        total_queries = cursor.fetchone()[0]
        
        # Tempo medio di risposta
        cursor.execute('''
        SELECT AVG(response_time) FROM queries 
        WHERE timestamp > datetime('now', '-{} days')
        '''.format(days))
        avg_response_time = cursor.fetchone()[0] or 0
        
        # Tasso di redirect
        cursor.execute('''
        SELECT 
            COUNT(CASE WHEN should_redirect THEN 1 END) * 100.0 / COUNT(*) 
        FROM queries 
        WHERE timestamp > datetime('now', '-{} days')
        '''.format(days))
        redirect_rate = cursor.fetchone()[0] or 0
        
        # Query più frequenti
        cursor.execute('''
        SELECT query, COUNT(*) as count FROM queries 
        WHERE timestamp > datetime('now', '-{} days')
        GROUP BY LOWER(query)
        ORDER BY count DESC
        LIMIT 10
        '''.format(days))
        frequent_queries = cursor.fetchall()
        
        conn.close()
        
        return {
            'total_queries': total_queries,
            'avg_response_time': round(avg_response_time, 2),
            'redirect_rate': round(redirect_rate, 1),
            'frequent_queries': frequent_queries
        }
    
    def export_data(self, output_file="analytics_export.json"):
        """Esporta tutti i dati in JSON"""
        conn = sqlite3.connect(self.db_path)
        
        # Esporta queries
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM queries')
        queries = cursor.fetchall()
        
        cursor.execute('SELECT * FROM performance')
        performance = cursor.fetchall()
        
        data = {
            'export_timestamp': datetime.now().isoformat(),
            'queries': queries,
            'performance': performance,
            'stats': self.get_stats(30)  # Ultimi 30 giorni
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        conn.close()
        return output_file

# Decorator per misurare performance
def measure_performance(analytics_instance, operation_name):
    """Decorator per misurare il tempo di esecuzione"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                success = True
            except Exception as e:
                result = None
                success = False
                raise
            finally:
                end_time = time.time()
                execution_time = end_time - start_time
                
                analytics_instance.log_performance(
                    f"{operation_name}_time", 
                    execution_time,
                    f"Success: {success}"
                )
            
            return result
        return wrapper
    return decorator

if __name__ == "__main__":
    analytics = ChatbotAnalytics()
    print("Sistema analytics inizializzato correttamente")