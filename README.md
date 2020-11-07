
# Welcome to ChatApp 

## Requirements
- NodeJS 12.14 (minimum)
- Python 3.7 (minimum)
- To run this project we need API keys for weather and giphy 
    - get weather api at this [link](https://home.openweathermap.org/api_keys) by signing up
    - get giphy api at this [link](https://developers.giphy.com/dashboard/) by signing up
- Docker for local database integration (optional)

## Installation
#### Clone this repository
```https://github.com/kpatoliya/chatApp-React-Flask-Socket```

#### Installation
Run the following commands to install the required library and tools for this project.
```
npm install
pip install -r requirements.txt 
```

#### Environment Variables
Create .env file at root folder and paste the following lines 
with your unique keys and tokens in the 'key' part and source the file after modified.
```
POSTGRES_USER=key
POSTGRES_DB=key
POSTGRES_PASSWORD=key
DATABASE_URL=postgresql://POSTGRES_USER:POSTGRES_PASSWORD@localhost/POSTGRES_DB
WEATHER_API=key
GIPHY_API=key
```
#### Setting up OAuth
- Google Auth <br/>
Follow this [link](https://developers.google.com/adwords/api/docs/guides/authentication#webapp) to get client ID<br />
Paste this Client ID in file GoogleAuth.tsx<br/>
```<GoogleLogin clientId="YOUR_CLIENT_ID" />```

- Facebook Auth <br/>
Follow this [link](https://developers.facebook.com/apps) to get client ID by creating a new app<br />
Paste this Client ID in file FacebookAuth.tsx<br/>
```<FacebookLogin clientId="YOUR_CLIENT_ID" />```

## Running Locally

- Start React app in development mode
    ```
    npm start
    ```
   
    The page will reload if you make edits.<br />
    You will also see any lint errors in the console.
    This will start the React Development server on http://localhost:3000.

- Start the server
    ```
     npm run dev
    ```
    This will start the server on http://localhost:4000.
    
- Running docker for database (optional)
    ```
    docker-compose up 
   ```
  This command would spin up the the container that has our database.
  
- Database setup locally

    This web application uses `psql` as the database to provide persistence with the bulletin boards. In order to get psql to work with python, run the following commands:
    1. `sudo yum update`, say yes for all the prompts.
    2. `sudo pip install --upgrade pip`
    3. `sudo pip install psycopg2-binary`
    4. `sudo pip install Flask-SQLAlchemy==2.1`
    
    If you have not already created a psql database, follow these steps in order to initialize one.
    
    1. `sudo yum install postgresql postgresql-server postgresql-devel postgresql-contrib postgresql-docs`, Enter yes to all prompts.    
    2. `sudo service postgresql initdb`  
    3. `sudo service postgresql start`    
    4. Make a new superuser: `sudo -u postgres createuser --superuser $USER` 
    5. Make a new database: `sudo -u postgres createdb $USER`   
    6. Make sure your user shows up and make a new one:    
        1. `psql`    
        2. `\du` look for yourself as a user    
        3. `\l` look for yourself as a database 
        4. `create user [some_username_here] superuser password '[password]';` 
        5. Make sure you remember the quotes around password and the semicolon. 
            1. Check `\du` to ensure it worked.
        6. `\q` to quit out of psql
        
## Deploy to Heroku
- Follow this [step](https://devcenter.heroku.com/articles/creating-apps) to create a project in Heroku
- Procfile is the configuration needed for Heroku.
- Create a Postgres Database on Heroku, [instructions here](https://devcenter.heroku.com/articles/heroku-postgresql)
- To deploy your application, [follow this](https://devcenter.heroku.com/articles/git)
- Set ```WEATHER_API``` & ```GIPHY_API``` Config Variable in your Heroku app's console.

## Linting
If you wish to check the linting on this project, execute the following commands.
1. `pip install pylint`
2. `pip install black`
3. `npm install -g eslint`
4. `eslint --init`, select the following options.
	1. "To check syntax, find problems, and enforce code style"
	2. "Javascript modules (import/export)"
	3. "React"
	4. "No"
	5. "Browser"
	6. "Use a popular style guide"
	7. "Airbnb"
	8. "Javascript"
	9. When asked if you want to install dependencies with npm, say "Yes"
5. Run `eslint scripts/[FILE]` on any of the `.js/.jsx`  files in the scripts directory.
	1.  Run `eslint --fix scripts/[FILE]` in order to automatically fix some of the linting errors
6. Run `pylint [FILE]` on any of the python files.

## Available Scripts
### `npm build`

Builds the app for production to the `build` folder.<br />
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.<br />
Your app is ready to be deployed!


