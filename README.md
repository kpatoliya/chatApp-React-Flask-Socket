
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
https://github.com/NJIT-CS490/project2-m1-kmp87

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
    
- Running docker for database
    ```
    docker-compose up 
   ```
  This command would spin up the the container that has our database.
  

## Deploy to Heroku
- Follow this [step](https://devcenter.heroku.com/articles/creating-apps) to create a project in Heroku
- Procfile is the configuration needed for Heroku.
- Create a Postgres Database on Heroku, [instructions here](https://devcenter.heroku.com/articles/heroku-postgresql)
- To deploy your application, [follow this](https://devcenter.heroku.com/articles/git)
- Set ```WEATHER_API``` & ```GIPHY_API``` Config Variable in your Heroku app's console.

 ## Issues
 - I was using ```@socketio.on('connect')``` initially which didn't allow me to get email from auth login and using other method 
    was making duplicate codes which was redundant, so I ended up replacing the method with ```@socketio.on('update_total_users')```
    and emitting from auth component so that every time login is successful the state get set to updated values. 
     
 - I was having the issue of input field not setting as required even after explicitly defining the input tag as required
    so I solved this issue by handling the function that is called at the time of submit.
    ```
    if(message !== ''){
            onMessageSubmit(e)
        }
    ```
 - Displaying gif and image when user inputs the link was displaying image with variable size. So I made this easy 
 using the this library `html-react-parser`. With this library I can just explicitly mention size of the image tag like
 ```<img src='" + giphy + "' width='250' height='250'>``` and return to frontend. 
 I used this [documentation](https://www.npmjs.com/package/html-react-parser) to solve this issue.
 
  
 ## Known Problems
 - None
 
 ## Improvements
 - If I had more time I would have added search box in the app to add the functionality of searching a term in the chat.
 I found a good article on steps to implement this feature which could 
 be found at this [link](https://www.iamtimsmith.com/blog/lets-build-a-search-bar-in-react/).
 - I could have added timestamp for each message displayed and also stored in database which could useful 
 to search or group messages according to the time. I would have added a new column named timestamp to store the time 
 when message was created, this would always load the timestamp as it is rendered with other infromation from the database.

 
## Available Scripts
### `npm build`

Builds the app for production to the `build` folder.<br />
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.<br />
Your app is ready to be deployed!


