## Beehive Funder Recommender API

### Local setup
1. Create the database with `createdb beehive_insight_development`
2. Setup the database with `python db_create.py`

### Usage
Send a `POST` request to `http://<API-DOMAIN-TBC>/recommend` with basic_auth and JSON body:

```
# Authentication
...
basic_auth: {
              username: RECOMMENDER_API_TOKEN,
              password: RECOMMENDER_API_SECRET
            }
...

# JSON
{
  'data': {
    'animals':      1, 'buildings':     0, 'care':        0,
    'crime':        0, 'disabilities':  1, 'disasters':   0,
    'education':    0, 'environment':   0, 'ethnic':      1,
    'exploitation': 1, 'food':          0, 'housing':     0,
    'mental':       0, 'organisations': 1, 'orientation': 0,
    'physical':     0, 'poverty':       0, 'public':      1,
    'refugees':     1, 'relationship':  0, 'religious':   0,
    'services':     0, 'unemployed':    1, 'water':       0,
	}
}
```
To get a JSON response of funder recommendation scores:
```
{
  'arts-council-england':       0.22603473860618983,
  'city-bridge-trust':          0.46549485130908264,
  'comic-relief':               0.6155196854623204,
  'esmee-fairbairn-foundation': 0.0,
  'garfield-weston-foundation': 0.29237209322797386,
  ...
  'john-ellerman-foundation':   0.0,
  'john-lyons-charity':         0.0,
  'paul-hamlyn-foundation':     0.0,
  'the-dulverton-trust':        0.2685075611165554,
  'trust-for-london':           0.5973849998069914
}
```
