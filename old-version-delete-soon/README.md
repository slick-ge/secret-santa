```md
# Secret Santa API

This API is built with Flask and provides several endpoints for managing a Secret Santa game.

## Endpoints

### Health Check

- **URL:** `/secret-santa/health`
- **Method:** `GET`
- **Response:** Status of the API.

### Store Data

- **URL:** `/secret-santa/store_data`
- **Method:** `POST`
- **Request Body:**

```json
{
  "Group": "group_name",
  "Name": "participant_name",
  "Surname": "participant_surname",
  "Email": "participant_email"
}
```

- **Response:** Confirmation of data storage.

**CURL Example:**

```sh
curl -X POST http://localhost:5000/secret-santa/store_data -H 'Content-Type: application/json' -d '{"Group": "group_name", "Name": "participant_name", "Surname": "participant_surname", "Email": "participant_email"}'
```

### Randomize Secret Santa

- **URL:** `/secret-santa/randomize_secret_santa`
- **Method:** `POST`
- **Response:** Randomized Secret Santa assignments.

**CURL Example:**

```sh
curl -X POST http://localhost:5000/secret-santa/randomize_secret_santa
```

### Get Rooms

- **URL:** `/secret-santa/get-rooms`
- **Method:** `POST`
- **Response:** List of rooms.

**CURL Example:**

```sh
curl -X POST http://localhost:5000/secret-santa/get-rooms
```

## Running the API

To run the API, use the following command:

```sh
python api.py
```

This will start the API at `http://localhost:5000`.
