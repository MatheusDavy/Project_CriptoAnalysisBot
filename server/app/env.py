import os
from dotenv import load_dotenv

load_dotenv()

AUTH_EMAIL = os.getenv("AUTH_EMAIL")
AUTH_PASSWORD = os.getenv("AUTH_PASSWORD")

JWT_SUB = os.getenv("JWT_SUB")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_SECRET = os.getenv("JWT_SECRET")

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")

SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ6c3BscmhpZnJuc3hqaHh2dGNzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTczODI2MTQsImV4cCI6MjA3Mjk1ODYxNH0.nUNrDVQ7_OowAlc0PJM4FwuEIqmZqrcnJkRmBdFVrFY"
SUPABASE_URL="https://rzsplrhifrnsxjhxvtcs.supabase.co"
SUPABASE_DB_PASSWORD="MD84L3avEWYn!5w"
