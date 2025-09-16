from supabase import create_client, Client
from app.env import SUPABASE_KEY, SUPABASE_URL

supabase_url = SUPABASE_URL
supabase_key = SUPABASE_KEY
supabase: Client = create_client(supabase_url, supabase_key)