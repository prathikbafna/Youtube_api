Backend Task:

Author: Prathik B Jain , 
	prathikbafna0@gmail.com
	9148489627

Note:
Database used : mongoDB
Frame work : Flask (python)


How to Install and run the project?

1.install all the requirements as mentioned in the requirement.txt using 
the cmd : pip install -r requirement.txt

2. use the cmd python app.py or flask run to run the server

3. you can fetch and search the data using the requests mentioned below on postman:

	I. A basic search API to search the stored videos using their title and description.
	http://127.0.0.1:5000/search/<title>/<description>
	example :
	GET  :	http://127.0.0.1:5000/search/7 BEST TRICEPS WORKOUT AT GYM WITH BARBELL ONLY
	/7 BEST TRICEPS WORKOUT AT GYM WITH BARBELL ONLY 6 BEST TRICEPS WORKOUT AT GYM THAT YOU NEVER DID 22 BEST TRICEP EXERICES AT ...

	
	II.GET API which returns the stored video data in a paginated response sorted in descending order of published datetime.
	http://127.0.0.1:5000/get/<query>
	example :
	GET   :  http://127.0.0.1:5000/get/mobile
	
	III Server should call the YouTube API continuously in background
	The server runs continuously till we reach the daily limit on making api calls 
