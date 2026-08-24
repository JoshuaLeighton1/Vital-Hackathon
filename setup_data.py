import os
import django

# Tell the script where your Django settings are
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vital_project.settings')
django.setup()

from django.contrib.auth.models import User
from ordering.models import Product, EmployeeProfile

# --- 1. Create the Superuser ---
# You can change these default credentials if you like
ADMIN_USER = 'admin'
ADMIN_PASS = 'vital2026'

if not User.objects.filter(username=ADMIN_USER).exists():
    # Create the admin user
    admin_user = User.objects.create_superuser(
        username=ADMIN_USER, 
        email='admin@vital.co.za', 
        password=ADMIN_PASS
    )
    # Give the admin an employee profile so they can test the frontend too
    EmployeeProfile.objects.create(user=admin_user, monthly_allowance=1000.00)
    print(f"✅ Superuser '{ADMIN_USER}' created successfully.")
else:
    print(f"⚡ Superuser '{ADMIN_USER}' already exists. Skipping.")


# --- 2. Create Dummy Products ---
products = [
    {
        "name": "Vital Maxi B", 
        "description": "High potency B-complex for energy and nervous system support.", 
        "price": 120.00, 
        "stock_quantity": 50
    },
    {
            "name": "Vital C 1000mg", 
            "description": "High potency C-vitamin for immune system support.", 
            "price": 120.00, 
            "stock_quantity": 50
    },
    {
            "name": "Vital Zinc 50mg", 
            "description": "High potency zinc for immune system support.", 
            "price": 180.00, 
            "stock_quantity": 50
    },
    {
            "name": "Vital Ashwagandha 500mg", 
            "description": "High potency ashwagandha for stress and anxiety support.", 
            "price": 300.00, 
            "stock_quantity": 50
    },
    {
            "name": "Vital Energy Boost", 
            "description": "High potency energy and nervous system support.", 
            "price": 180.00,    
            "stock_quantity": 50
    },
 

    {
        "name": "Vital Omega 3", 
        "description": "1000mg Salmon oil for heart and brain health.", 
        "price": 150.00, 
        "stock_quantity": 100
    },
    {
        "name": "Vital Calcium Complex", 
        "description": "Advanced formula for bone density and muscle function.", 
        "price": 95.00, 
        "stock_quantity": 30
    },
]

for p_data in products:
    # get_or_create checks if the product name already exists before adding it
    obj, created = Product.objects.get_or_create(
        name=p_data['name'], 
        defaults={
            'description': p_data['description'],
            'price': p_data['price'],
            'stock_quantity': p_data['stock_quantity']
        }
    )
    if created:
        print(f"✅ Product '{obj.name}' added to database.")
    
print("🎉 Database setup complete!")