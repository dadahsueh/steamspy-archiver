# Steam Spy API
| https://steamspy.com/api.php

This API provides data from Steam Spy in JSON format via GET requests. The data is refreshed once daily, so there’s no need to request the same information more than once every 24 hours.

> [!IMPORTANT]  
> Please read this document thoroughly, as some details may have changed.

## API Usage Guidelines

- **Poll Rate:**
  - General requests: 1 request per second.
  - `all` requests: 1 request per 60 seconds.

## Common Parameters

- `request` - The API request code.

## Accepted Requests

### `appdetails`

Returns details for a specific application. Requires the `appid` parameter.
- **Get details for a specific app:**  
  `steamspy.com/api.php?request=appdetails&appid=730`  
  *(Returns data for Counter-Strike: Global Offensive)*

### `genre`

Returns games in a specific genre. Requires the `genre` parameter.

Example:  
`steamspy.com/api.php?request=genre&genre=Early+Access`

### `tag`

Returns games with a specific tag. Requires the `tag` parameter.

Example:  
`steamspy.com/api.php?request=tag&tag=Early+Access`

### `top100in2weeks`

Returns the Top 100 games by players in the last two weeks.
- **Get Top 100 apps by players in the last two weeks:**  
  `steamspy.com/api.php?request=top100in2weeks`

### `top100forever`

Returns the Top 100 games by players since March 2009.

Example:  
`steamspy.com/api.php?request=top100forever`

### `top100owned`

Returns the Top 100 games by owners.

Example:  
`steamspy.com/api.php?request=top100owned`

### `all`

Returns all games with owners data, sorted by owners. Returns 1,000 entries per page.

- `page` - Page number for the list (starting from 0).

- **Get all apps with owners data (1000 entries per page):**  
  `steamspy.com/api.php?request=all&page=1`


### Fields Description

- **`appid`** - Steam Application ID. If this is `999999`, data for this app is hidden by the developer's request.
- **`name`** - The name of the game.
- **`developer`** - A comma-separated list of the game's developers.
- **`publisher`** - A comma-separated list of the game's publishers.
- **`score_rank`** - The game's score rank based on user reviews.
- **`owners`** - The range of owners for this application on Steam.
- **`positive`** - Positive reviews?
- **`negative`** - Negative reviews?
- **`userscore`** - Not used?
- **`average_forever`** - The average playtime since March 2009 (in minutes).
- **`average_2weeks`** - The average playtime in the last two weeks (in minutes).
- **`median_forever`** - The median playtime since March 2009 (in minutes).
- **`median_2weeks`** - The median playtime in the last two weeks (in minutes).
- **`price`** - The current price in the US (in cents).
- **`initialprice`** - The original price in the US (in cents).
- **`discount`** - The current discount percentage.
- **`ccu`** - The peak concurrent users (CCU) yesterday.
- **`languages`** - A list of supported languages.
- **`genre`** - A list of genres.
- **`tags`** - A JSON array of the game's tags with votes.

## Return Format

Here is an example of the JSON response for `appdetails` of `appid=730`:

```json
{
  "appid": 730,
  "name": "Counter-Strike: Global Offensive",
  "developer": "Valve",
  "publisher": "Valve",
  "score_rank": "",
  "owners": "100,000,000 .. 200,000,000",
  "positive": 7222296,
  "negative": 1070407,
  "userscore": 0,
  "average_forever": 0,
  "average_2weeks": 0,
  "median_forever": 0,
  "median_2weeks": 0,
  "price": "0",
  "initialprice": "0",
  "discount": "0",
  "ccu": 1463726,
  "languages": "English, Czech",
  "genre": "Action, Free To Play",
  "tags": {
    "FPS": 90384,
    "Shooter": 65029
  }
}
```
