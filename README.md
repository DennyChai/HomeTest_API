#### Testcase for Jikan API
|Test Case Title|Steps|Expected Result|Actual Result|Status|
|:----|:----|:----|:----|:----|
|Check successfully call endpoint|1. Request the api endpoint<br>2. Response status should be 200|Response should be 200|Response is 200|Pass|
|Check Anime not existing ID|1. Request with unexist id<br>2. Rsponse status should be 404|Response should be 404|Response is 404|Pass|
|Check Anime full data correctness|1. Request the api with id<br>2. Response status should be 200<br>3. Reponse content type should be JSON<br>4. Check the Anime title is equal to expected tile name|Get the anime title and should be as expected|The title is expected|Pass|
|Check Anime full data and short data are the same|1. Request the api with full data and short data<br>2. Check both content should be JSON<br>3. Check title, episodes are the same with same id|The id, title, episodes of the Anime should be the same|The data are all the same as expected|Pass|
