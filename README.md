## Beehive Insight

### Local setup
1. Create the database with `createdb beehive_insight_development`
2. Setup the database with `python db_create.py`
3. Start app with `BEEHIVE_INSIGHT_TOKEN=<YOUR TOKEN> python app.py`
4. Visit `http://localhost:5000/update` to create initial analysis data.

### Usage
Send a `POST` request to `https://beehive-insight.herokuapp.com/beneficiaries` with basic_auth and JSON body:

```
# Authentication
...
basic_auth: {
              username: BEEHIVE_INSIGHT_TOKEN, # 'username' in Development
              password: BEEHIVE_INSIGHT_SECRET # 'password' in Development
            }
...

# JSON
{
  'data': {
    'animals':      1, 'buildings': 0, 'care':        0, 'crime':        0, 'disabilities':  1,
    'disasters':    0, 'education': 0, 'environment': 0, 'ethnic':       1, 'exploitation':  1,
    'food':         0, 'housing':   0, 'mental':      0, 'organisation': 1, 'organisations': 1,
    'orientation':  0, 'physical':  0, 'poverty':     0, 'public':       1, 'refugees':      1,
    'relationship': 0, 'religious': 0, 'services':    0, 'unemployed':   1, 'water':         0
	}
}
```
To get a JSON response of Fund recommendation scores:
```
{
  '2015-esmee-fairbairn-foundation-finance-fund-grants':            0.0,
  '2015-esmee-fairbairn-foundation-food':                           0.15850567812182481,
  '2015-esmee-fairbairn-foundation-main-grants':                    0.62853936105470887,
  ...
  '2015-lloyds-bank-foundation-for-england-and-wales-enable-north': 0.098905684253000059,
  '2015-lloyds-bank-foundation-for-england-and-wales-enable-south': 0.20220406960500981,
  '2015-lloyds-bank-foundation-for-england-and-wales-invest-north': 0.03558200677189427,
  '2015-lloyds-bank-foundation-for-england-and-wales-invest-south': 0.50722677474358457
}
```
