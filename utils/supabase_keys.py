from supabase import create_client, Client
import pandas as pd

url = "https://xzjqbirfkdwpbglypukc.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh6anFiaXJma2R3cGJnbHlwdWtjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NjM3MjQ5MCwiZXhwIjoyMDYxOTQ4NDkwfQ.YrATnv59pVSk9y_j1peh-1MjWlQcCLKS2w2nUbNCP4c"  
supabase: Client = create_client(url, key)