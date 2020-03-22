# Casting Agency API

Casting Agency API is an app, provided to simplify process of creating movies and managing and assigning actors to those movies

The application can:
1. Create, edit, delete and retrieve movies records 
2. Create, edit, delete and retrieve actors records
3. Link actors to movies records


## To run the app locally:

1. Create and activate virtualenv
```
python3 -m venv venv
source venv/bin/activate
```
2. Install dependencies
```
pip install -r requirements.txt
```
3. Setup a database
```
createdb agency
psql agency < agency.psql
```
4. Run the server in debug mode (will restart on each code change)
```
export FLASK_DEBUG=True
flask run
```
5. Navigate to http://localhost:3000/
6. To run the tests, execute
```
dropdb agency_test
createdb agency_test
psql agency_test < agency.psql
python test_app.py
```

## ENDPOINTS

#### GET '/movies'
- Fetches a list of movies objects
- Requires authorisation: yes
- Request arguments: None
- Returns: 
'movies' an array of objects
'success' a boolean value, which depends on successfulness of the request
```
{
    "movies": [
        {
            "id": 6,
            "release_date": "2016-08-31",
            "title": "La La Land"
        }
    ],
    "success": true
}
```

#### GET '/actors'
- Fetches a list of actors objects
- Requires authorisation: yes
- Request arguments: None
- Returns: 
'actors' an array of objects
'success' a boolean value, which depends on successfulness of the request
```
{
  "actors": [
    {
      "age": 41,
      "gender": "male",
      "id": 7,
      "movie_id": null,
      "name": "Ian Somerhalder"
    }
  ],
  "success": true
}
```

#### POST '/actors'
- Creates new actor's record 
- Requires authorisation: yes
- Request Arguments: name (actor's name, string - required argument), age (actor's age, integer), gender (actor's gender, string)
- Returns: 
'actor' an array of a created object
'success' a boolean value, which depends on successfulness of the request

#### POST '/movies'
- Creates new movie record 
- Requires authorisation: yes
- Request Arguments: title (movies name, string - required argument), release_date (movies release date, datetime object or string)
- Returns: 
'movie' an array of a created object
'success' a boolean value, which depends on successfulness of the request

#### PATCH '/movies/<int:movie_id>'
- Edits movies record 
- Requires authorisation: yes
- Request Arguments: title (movies title, string), release_date (movies release date, datetime object or string). All arguments are not required
- Returns: 
'movie' an array of an edited object
'success' a boolean value, which depends on successfulness of the request

#### PATCH '/actors/<int:actor_id>'
- Edits actor's record 
- Requires authorisation: yes
- Request Arguments: name (actor's name, string), age (actor's age, integer), gender (actor's gender, string), movie_id (movie_id for which the actor is assigned). All arguments are not required
- Returns: 
'actor' an array of an edited object
'success' a boolean value, which depends on successfulness of the request

#### DELETE '/actors/<int:actor_id>'
- Deletes actor by id
- Requires authorisation: yes
- Request Arguments: actor_id (required)
- Returns: 
'deleted' an array of a deleted object
'success' a boolean value, which depends on successfulness of the request
```  
"deleted": [
    {
      "age": 33,
      "gender": null,
      "id": 1,
      "movie_id": null,
      "name": "Mary-Kate Olsen"
    }
```

#### DELETE '/movies/<int:movie_id>'
- Deletes movie by id
- Requires authorisation: yes
- Request Arguments: movie_id (required)
- Returns: 
'deleted' an array of a deleted object
'success' a boolean value, which depends on successfulness of the request
