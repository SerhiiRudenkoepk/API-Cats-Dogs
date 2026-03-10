================================================================================
                    CATS & DOGS API — README (V 0.1)
================================================================================

  This project provides a REST API for managing a collection of virtual pets
  (cats and dogs). I played way too much in Mewgenics and, for some reason, decided
  to make this API.
  It is intended for educational use and for practising API testing with tools
  such as Postman.

--------------------------------------------------------------------------------
PURPOSE AND DISCLAIMER
--------------------------------------------------------------------------------

  This API was created primarily for practice and as a learning project. It is
  also offered to anyone who wishes to practise testing REST APIs (e.g. via
  Postman) and to run experiments with typical CRUD operations, filtering,
  pagination, and custom endpoints. At the time of writing, I was not
  able to find a similarly straightforward, open API for this kind of hands-on
  practice (because for some reason, most of the links/sites are not working anymore),
  so I hoped that this project can fill that gap.

  I also hoped that this API will be useful to learners and testers. The
  project is maintained in good faith and will continue to be developed and
  improved over time. Feedback and suggestions are welcome.

  This API is provided "as is" for non-commercial, educational use. It is not
  intended for production or sensitive data.

--------------------------------------------------------------------------------
REQUIREMENTS
--------------------------------------------------------------------------------

  - Python 3.8 or higher
  - Flask (install via: pip install flask)

  Recommended: use a virtual environment and install dependencies from
  requirements.txt if present.

--------------------------------------------------------------------------------
RUNNING THE API
--------------------------------------------------------------------------------

  1. Open a terminal in the project directory.

  2. (Optional) Activate your virtual environment:
       source .venv/bin/activate   (Linux/macOS)
       .venv\Scripts\activate      (Windows)

  3. Start the server:
       python main.py

  4. By default the API runs at:
       http://127.0.0.1:5000

  5. You can send requests with a browser, Postman, curl, or any HTTP client.

--------------------------------------------------------------------------------
DATA STORAGE
--------------------------------------------------------------------------------

  Pet data is stored in the file "pets.json" in the project folder. The file
  is read when the application starts and is updated when pets are created,
  updated, or deleted. If "pets.json" is missing or invalid, the API starts
  with an empty list. Ensure the application has read and write permissions
  in the project directory.

--------------------------------------------------------------------------------
PET MODEL
--------------------------------------------------------------------------------

  Each pet is represented by a JSON object with the following fields:

    - id              (integer)  Unique identifier
    - name            (string)  Pet name
    - type            (string)  Usually "cat" or "dog" (or "hybrid" for bred)
    - age             (integer) Age in years
    - mischief_level  (integer) 1–10
    - special_ability (string)  Optional ability description
    - status          (string)  e.g. "sleepy", "active"

--------------------------------------------------------------------------------
API ENDPOINTS
--------------------------------------------------------------------------------

  Base URL: http://127.0.0.1:5000  (unless configured otherwise)

  ----------------------------------------------------------------------------
  Discovery
  ----------------------------------------------------------------------------
  GET  /routes
       Returns a list of all registered routes, methods, and endpoint names.
       Useful for exploring the API.

  ----------------------------------------------------------------------------
  Collection: list and create
  ----------------------------------------------------------------------------
  GET  /pets
       Returns all pets. Status: 200.

  POST /pets
       Creates a new pet. Body: JSON with name, type, age (optional),
       mischief_level (optional), special_ability (optional), status (optional).
       Returns the created pet. Status: 201.

  ----------------------------------------------------------------------------
  Single pet: get, update, delete
  ----------------------------------------------------------------------------
  GET    /pets/<pet_id>
         Returns the pet with the given ID. Status: 200 or 404.

  PUT    /pets/<pet_id>
         Full update of the pet. Body: JSON with name, type, and optional
         fields. Status: 200 or 404.

  PATCH  /pets/<pet_id>
         Partial update. Body: JSON with only the fields to change.
         Status: 200 or 404.

  DELETE /pets/<pet_id>
         Removes the pet. Status: 200 or 404.

  ----------------------------------------------------------------------------
  Create pet with specific ID
  ----------------------------------------------------------------------------
  POST   /pets/<pet_id>
         Creates a new pet with the given ID. Body: JSON as for POST /pets.
         Fails if the ID already exists. Status: 201 or 409.

  ----------------------------------------------------------------------------
  Search, pagination, sorting
  ----------------------------------------------------------------------------
  GET  /pets/search
       Query parameters: type (e.g. "cat", "dog"), status (e.g. "sleepy").
       Returns filtered list. Status: 200.

  GET  /pets/page
       Query parameters: page (default 1), limit (default 5).
       Returns paginated list with page, limit, total count, and results.
       Status: 200.

  GET  /pets/sort_by
       Query parameters: sort_by (field name, e.g. age, mischief_level),
       order ("asc" or "desc", default "asc"). Returns sorted list. Status: 200.

  ----------------------------------------------------------------------------
  Extra features
  ----------------------------------------------------------------------------
  GET  /pets/random_pet_info
       Returns one randomly chosen pet. Status: 200 (or error if no pets).

  POST /pets/bulk_production
       Creates multiple pets. Body: JSON array of objects; each object may
       omit fields to get random values. Status: 201.

  POST /pets/breed
       Creates a "child" pet from two parents. Body: JSON with parent1_id and
       parent2_id. Status: 201.

  POST /pets/fight
       Compares two pets by a simple formula. Body: JSON with pet1_id and
       pet2_id. Returns winner ID. Status: 200.

--------------------------------------------------------------------------------
TESTING WITH POSTMAN
--------------------------------------------------------------------------------

  - Set the base URL to http://127.0.0.1:5000.
  - Use GET /routes to see all available endpoints.
  - For POST, PUT, PATCH, and /pets/fight, set the body to "raw" and "JSON",
    and send the required fields as described above.
  - For GET endpoints with query parameters, add them in the Params tab or
    in the URL (e.g. ?page=1&limit=10, ?type=cat&status=sleepy).

  You can practise typical scenarios: create pets, update with PUT and PATCH,
  delete, paginate, filter, sort, and use the breed and fight endpoints for
  extra variety.

--------------------------------------------------------------------------------
VERSION AND UPDATES
--------------------------------------------------------------------------------

  This document describes the API as of the current version. Endpoints and
  behaviour may be extended or adjusted in future updates. The author
  intends to continue maintaining and improving this project.

--------------------------------------------------------------------------------
CONTACT AND FEEDBACK
--------------------------------------------------------------------------------

  For issues, suggestions, or contributions, please refer to the project
  repository or contact the author through the usual project channels.

================================================================================
                              End of README
================================================================================
