# Steam
## Studenteninfo:
### David Sigmund (procesbegeleider), 1883920
### Daan van der Meulen, 1882011
### Ayden Sachania, 1879502
### Kane de Crook, 1841798



# Pip commands:
### pip3 install customtkinter (Voor GUI)
### pip3 install python-dotenv (Voor .env file)
### pip3 install Flask (Voor webserver)
### pip3 install requests (Voor API requests)
### pip3 install pillow (Voor images)
### pip3 install psycopg2-binary (Voor database)
### pip3 install bs4 (Voor iets wat Daan heeft gemaakt)
### pip3 install matplotlib (Voor iets wat Ayden heeft gemaakt)

# Database query
### -- Create the admin_users table
### CREATE TABLE admin_users (
###    id SERIAL PRIMARY KEY,
###    username VARCHAR(50) NOT NULL UNIQUE,
###    password VARCHAR(255) NOT NULL
### );

### -- Insert an admin user with username 'admin' and password 'admin'
### INSERT INTO admin_users (username, password)
### VALUES ('admin', 'admin');


