The server Communicates to the client using HTTP/HTTPS for fetching data and posting it to the database.
For communication only the GET and POST HTTP functions are used, utilizing URI paths to differentiate between fetching and posting.

# GET

When the server gets a request for data, one of these paths define how it is resolved, some of them just send static data, so they're coupled together here.

## Static pages (/conntest, /add_hunt, /spse)

The pages conntest and add_hunt send a static html, conntest contains a message that the server is up, and add_hunt contains a message that this path is for posting only.
The page spse redirects to the site of SPŠE Plzeň.

## i_venture_forth_to_hunt

This path is used to fetch data from the database with filtering based on the hunt hash.
As URI parameters the client uses key value pairs, where the key is always "f" while the value is the hunt hash to filter by. The client can use any mumber of pairs
The server responds with the hunt hash, that the client can confirm and the number of times it was completed.

# POST

When the server gets a request to store data, the request has to come with a JSON of the data, the interpretation of which is based on the path.

## /add_hunt

When the user is adding a hunt the JSON contains the column row values for the hunt. When the hash is the first recorded one as a new row, while if it's not it just increments the count value in the db. After resolving it, the server sends a confirmation to the client.

## /add_user

>[!WARNING] 
>this is not supported right now

When the user is adding a user, the JSON contains the column row values of the user, when the server get's the request, it adds the user to the database and sends a confirmation to the client.
