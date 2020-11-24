# Oh My Bills!
Identifying recurring payments on the bank statement.

_Oh My Bills_ takes a bank statement in CSV and identifies payments that are likely to be recurring. It provides an web API for getting results about input bank data.

This is written in Python as a good prototyping language, but other languages could also be fun, for example Go, Scala, C# or whatever you like. 

**This is a proof of concept**. It is meant to demonstrate the idea, and is not production ready. 

This means: 
1. That it probably won't work correctly with bank statement data from every bank. 
2. That it is not yet optimized to work under heavy load or with very large files.
3. That there is not yet any documentation for the api. 

## API documentation

The API only contains a single endpoint: `GET /recurring`. 

This endpoint returns a JSON object in the following shape:
```json
{
  "data": [
    {
      "members": [
        {
          "amount": -96.15,
          "date": "Tue, 10 Nov 2020 00:00:00 GMT",
          "description": "Recurring payment"
        },
        {
          "amount": -96.58,
          "date": "Thu, 08 Oct 2020 00:00:00 GMT",
          "description": "Recurring payment "
        }
      ],
      "variance": 3.933
    }
  ]
}
``` 

The `data` field contains the result data. It is an object with two fields:
- `members`: The recurring payments.
- `variance`: An indication of how regular the payments are. The higher the number the less regular. Everything over 10 is not included.

## Running with Docker

To run my example image, first downlad the image:
```shell script
docker pull stenskjaer/oh-my-bills
```

```
docker run -p 5000:5000 -t stenskjaer/oh-my-bills 
```

Now you can visit the endoint `localhost:5000/recurring` to get an analysis result. Note that for privacy reasons the data provided in the public Docker image is not that rich.

## Provide you own data

This example uses my default data. If you want to try with your own data, you can build a custom docker image and send in your own data as a CSV file.

To build the image, run the following from the root of the application directory:
```
docker build -t oh-my-bills --build-arg data=data/export-from-my-bank.csv .
```

Where the file `data/export-from-my-bank.csv` is available from the current working directory.

The file that you refer to has to be a CSV file. However, as this is just a proof of concept, the following restrictions apply:
- It is most likely to work with a CSV exported from Lån og Spar Bank. This means that:
- It is assumed that the cells in the CSV are separated by `;` and a newline indicates a new row.
- It assumes that the second cell in the CSV is the transaction date, that the third is the description and that the fourth is the amount transferred.

This means that a valid example CSV could look like this:
```text
"09-11-2020";"09-11-2020";"Example entry 1";"-2.123,00"
"02-11-2020";"02-11-2020";"Example entry 2";"100,00"
```


## Next steps

Given that this is only a very minimal proof of concept, the first obvious next steps would be:
1. Start a documentation of the API – for example with Swagger/OpenAPI.
2. Create endpoints for providing data in a `POST` call.
3. Refine the algorithm for identifying 
3. Optimize performance on larger datasets. 
4. Extend the modes of presentation and endpoints.
