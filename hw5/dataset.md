# Dataset for HW5

This dataset is a subset of lobbying data from the City of Chicago Data Portal. Data maybe modified for testing functionality

The following descriptions are of the full dataset. Note that the assignment uses a subset of these tables (and a subset of the attributes)

### Employers
https://data.cityofchicago.org/Ethics/Lobbyist-Data-Employers/dmeb-2zra

Employers of registered lobbyists as reported in the Lobbyist Statement of Registration. Due to requirements for lobbyists to re-register, the importance of showing year for most lobbying-related data, and some employers being reported by multiple lobbyists, the same employer often will have multiple records
See http://www.cityofchicago.org/city/en/depts/ethics/provdrs/lobby.html for more information on the Board of Ethics' role in regulating and reporting on lobbying in Chicago.

```
Year	The year for which this record was created. Number
EMPLOYER_ID	A unique identifier for the employer record. This ID can be used to link records in other datasets that contain an ID column with the same name. Number
NAME	Employer name.Plain Text
ADDRESS_1	Plain Text
ADDRESS_2	Plain Text
CITY	Plain Text
STATE	Plain Text
ZIP	Plain Text
COUNTRY	Plain Text
PHONE	Plain Text
FAX	Plain Text
CREATED_DATE	The date the record was created. Date & Time
ACTIVE	Whether the employer record is active in the Board of Ethics system for use in further registrations.
```

### Clients

https://data.cityofchicago.org/Ethics/Lobbyist-Data-Clients/g8p5-y4m5

Clients represented by registered lobbyists as reported in their Lobbyist Statements of Registration. Due to requirements for lobbyists to re-register and the importance of showing year for most lobbying-related data, the same client often will have multiple records. See http://www.cityofchicago.org/city/en/depts/ethics/provdrs/lobby.html for more information on the Board of Ethics' role in regulating and reporting on lobbying in Chicago.

```
Year	 The year in which the lobbyist registered the client with the information shown. Number
CLIENT_ID	 A unique ID for the client that can be used to link to the same column name in other datasets. Number
NAME	 The name of the client. Plain Text
ADDRESS_1	 Plain Text
ADDRESS_2	Plain Text
CITY	Plain Text
STATE	Plain Text
ZIP	Plain Text
COUNTRY	 Plain Text
CREATED_DATE	  The date the record was created. Date & Time
ACTIVE	Plain Text
```

### Lobbyists

https://data.cityofchicago.org/Ethics/Lobbyist-Data-Lobbyists/tq3e-t5yq

Lobbyists registered with the Chicago Board of Ethics since 2012. Due to requirements for lobbyists to re-register and the importance of showing year for most lobbying-related data, the same lobbyist often will have multiple records

```
YEAR	 The year in which the lobbyist registered with the information shown. Number
LOBBYIST_ID	 A unique identifier for the lobbyist record. This ID can be used to link records in other datasets that contain an ID column with the same name. Number
SALUTATION	 Plain Text
FIRST_NAME	Plain Text
MIDDLE_INITIAL	 Plain Text
LAST_NAME	Plain Text
SUFFIX	 Plain Text
ADDRESS_1	Plain Text
ADDRESS_2	Plain Text
CITY	Plain Text
STATE	Plain Text
ZIP	Plain Text
COUNTRY	Plain Text
EMAIL	Plain Text
PHONE	Plain Text
FAX	Plain Text
EMPLOYER_ID	A unique identifier for the employer record associated with the lobbyist record. This ID can be used to link records in other datasets that contain an ID column with the same name. A lobbyist with multiple employers will have multiple records in this dataset.Number
EMPLOYER_NAME	The name of the employer associated with the lobbyist record. A lobbyist with multiple employers will have multiple records in this dataset.Plain Text
CREATED_DATE  The date the record was created. Date & Time
```

### Lobbyist, Client, Employer Combinations
https://data.cityofchicago.org/Ethics/Lobbyist-Data-Lobbyist-Employer-Client-Combination/2eqz-3nvz
Each unique combination of a lobbyist, his/her employer, and a client of that employer. This dataset can be used to see relationships between these three entities. Each has a separate dataset with more detailed information about each lobbyist, employer, or client.

```
Year	The year to which this record applies.Number
LOBBYIST_ID	A unique identifier for the lobbyist record. This ID can be used to link records in other datasets that contain an ID column with the same name. Number
EMPLOYER_ID	A unique identifier for the employer record. This ID can be used to link records in other datasets that contain an ID column with the same name.Number
CLIENT_ID	A unique identifier for the client record. This ID can be used to link records in other datasets that contain an ID column with the same name.Number
LOBBYIST_SALUTATION	 Plain Text
LOBBYIST_FIRST_NAME	Plain Text
LOBBYIST_MIDDLE_INITIAL	Plain Text
LOBBYIST_LAST_NAME	Plain Text
LOBBYIST_SUFFIX	Plain Text
EMPLOYER_NAME	Plain Text
CLIENT_NAME	Plain Text
```



### Expenditures:
See https://data.cityofchicago.org/Ethics/Lobbyist-Data-Expenditures-Large/xika-473c (and small)

```
EXPENDITURE_ID	A unique identifier for the expenditure record. Number
PERIOD_START	Start of the reporting period for which this record was created. Date & Time
PERIOD_END	End of the reporting period for which this record was created. Date & Time
LOBBYIST_ID	A unique identifier for the lobbyist record. This ID can be used to link records in other datasets that contain an ID column with the same name. Number
LOBBYIST_FIRST_NAME	 Plain Text
LOBBYIST_MIDDLE_INITIAL	 Plain Text
LOBBYIST_LAST_NAME	Plain Text
ACTION	 The purpose of the lobbying for which this expenditure was made. Plain Text
AMOUNT	Money
EXPENDITURE_DATE	Date & Time
PURPOSE	The type of expenditure.Plain Text
RECIPIENT	 The party to whom the expense was paid. Plain Text
CLIENT_ID	A unique ID for the client on whose behalf the lobbying related to this expenditure was done. This ID can be used to link to the same column name in other datasets. Number
CLIENT_NAME The name of the client on whose behalf the lobbying related to this expenditure was done. Plain Text
CREATED_DATE	The date the record was created. Date & Time
```

### Compensation
https://data.cityofchicago.org/Ethics/Lobbyist-Data-Compensation/dw2f-w78u

Lobbying-related compensation received by registered lobbyists as reported in their quarterly reports.

```
COMPENSATION_ID	 A unique ID for this record. Number
PERIOD_START	Start of the reporting period for which this record was created. Date & Time
PERIOD_END	 End of the reporting period for which this record was created Date & Time
LOBBYIST_ID	A unique identifier for the lobbyist record. This ID can be used to link records in other datasets that contain an ID column with the same name. Number
LOBBYIST_FIRST_NAME	Plain Text
LOBBYIST_MIDDLE_INITIAL	Plain Text
LOBBYIST_LAST_NAME	Plain Text
COMPENSATION_AMOUNT	Money
CLIENT_ID	 A unique ID for the client that can be used to link to the same column name in other datasets. Number
CLIENT_NAME	Plain Text
CREATED_DATE The date the record was created. Date & Time
```

### Contributions

https://data.cityofchicago.org/Ethics/Lobbyist-Data-Contributions/p9p7-vfqc

Political contributions by registered lobbyists, who must report every political contribution made to any candidate for City office, any elected official of the City, and any official or employee of the City seeking election to an office other that a City office during the reporting period.
See http://www.cityofchicago.org/city/en/depts/ethics/provdrs/lobby.html for more information on the Board of Ethics' role in regulating and reporting on lobbying in Chicago.

```
CONTRIBUTION_ID	 A unique identifier for the contribution record. Number
PERIOD_START	Start of the reporting period for which this record was created. Date & Time
PERIOD_END	 End of the reporting period for which this record was created. Date & Time
CONTRIBUTION_DATE	 Date & Time
RECIPIENT	Plain Text
AMOUNT	Money
LOBBYIST_ID	 A unique identifier for the lobbyist record. This ID can be used to link records in other datasets that contain an ID column with the same name. Number
LOBBYIST_FIRST_NAME	Plain Text
LOBBYIST_LAST_NAME	Plain Text
CREATED_DATE	The date the record was created.Date & Time
```

### Lobbying Activity
https://data.cityofchicago.org/Ethics/Lobbyist-Data-Lobbying-Activity/pahz-egmi

List of each City agency lobbied, whether it involved legislative or administrative action (or both) and a brief description of the action promoted or opposed, as reported by registered lobbyists.

```
LOBBYING_ACTIVITY_ID	 A unique identifier for the lobbying activity record.Number
PERIOD_START	Start of the reporting period for which this record was created. Date & Time
PERIOD_END	End of the reporting period for which this record was created. Date & Time
ACTION	 Whether the action sought was Administrative, Legislative, or Both. Plain Text
ACTION_SOUGHT	Plain Text
DEPARTMENT	Plain Text
CLIENT_ID	A unique identifier for the client record. This ID can be used to link records in other datasets that contain an ID column with the same name.Number
CLIENT_NAME	Plain Text
LOBBYIST_ID	 A unique identifier for the lobbyist record. This ID can be used to link records in other datasets that contain an ID column with the same name. Number
LOBBYIST_FIRST_NAME	Plain Text
LOBBYIST_MIDDLE_INITIAL	Plain Text
LOBBYIST_LAST_NAME	Plain Text
CREATED_DATE	The date the record was created. Date & Time
```

### Gifts
https://data.cityofchicago.org/Ethics/Lobbyist-Data-Gifts/5d79-9xqr

Every gift made by a registered lobbyist during the reporting period to an official or employee of the City.

```
GIFT_ID	 A unique identifier for the gift record. Number
PERIOD_START	Start of the reporting period for which this record was created. Date & Time
PERIOD_END	 End of the reporting period for which this record was created. Date & Time
GIFT	 Plain Text
RECIPIENT_FIRST_NAME	Plain Text
RECIPIENT_LAST_NAME	Plain Text
RECIPIENT_TITLE	Plain Text
VALUE	Money
DEPARTMENT	Plain Text
LOBBYIST_ID	A unique identifier for the lobbyist record. This ID can be used to link records in other datasets that contain an ID column with the same name. Number
LOBBYIST_FIRSTNAME	Plain Text
LOBBYIST_LASTNAME	Plain Text
CREATED_DATE	The date the record was created.Date & Time
```
