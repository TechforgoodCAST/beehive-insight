## Beehive Insight

### Local setup
1. Create the database with `createdb beehive_insight_development`
2. Setup the database with `python db_create.py`
3. Start app with `BEEHIVE_DATA_TOKEN=<YOUR TOKEN> python app.py`
4. Visit `http://localhost:5000/update_beneficiaries` to create initial analysis data for beneficiaries.
5. Visit `http://localhost:5000/update_amounts` to create initial analysis data for amounts.
6. Visit `http://localhost:5000/update_durations` to create initial analysis data for durations.

### Usage

Send a `POST` request with `basic_auth` and `body` as follows:

#### Authentication
```
basic_auth: {
              username: BEEHIVE_INSIGHT_TOKEN, # 'username' in Development
              password: BEEHIVE_INSIGHT_SECRET # 'password' in Development
            }
```

#### Beneficiaries
`POST` to `http://insight.beehivegiving.org/beneficiaries` with the following `body`:

```
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
To get a JSON response of Fund recommendation scores based on beneficiaries.

#### Amounts
`POST` to `http://insight.beehivegiving.org/amounts` with the following `body`:

```
{
   "data":{
      "amount":10000
   }
}
```
To get a JSON response of Fund recommendation scores based on the amount requested.

#### Durations
`POST` to `http://insight.beehivegiving.org/durations` with the following `body`:

```
{
   "data":{
      "duration":12
   }
}
```
To get a JSON response of Fund recommendation scores based on the duration requested.

#### Example response
Example of Fund recommendation scores:
```
{
  'esmee-fairbairn-foundation-finance-fund-grants':            0.0,
  'esmee-fairbairn-foundation-food':                           0.15850567812182481,
  'esmee-fairbairn-foundation-main-grants':                    0.62853936105470887,
  ...
  'lloyds-bank-foundation-for-england-and-wales-enable-north': 0.098905684253000059,
  'lloyds-bank-foundation-for-england-and-wales-enable-south': 0.20220406960500981,
  'lloyds-bank-foundation-for-england-and-wales-invest-north': 0.03558200677189427,
  'lloyds-bank-foundation-for-england-and-wales-invest-south': 0.50722677474358457
}
```
