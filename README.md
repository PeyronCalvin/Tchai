
# Tchaî - CCC project

![Tchaî](https://github.com/PeyronCalvin/Tchai_PEYRON_Calvin_LOPES-CASTANHEIRA_Marcelo/blob/main/Images/Tcha%C3%AE.jpg)

## Purpose of this project

This project has for goal to help the understanding of data security inside a server. For this, there is several versions of a server which are security-incremented. The first one being the least secured and the fourthh one the most secured. The versions are the following:
* TchaîV1: really basic, this server version has zero security, it's open bar 
* TchaîV2: a little bit more secured, we can check transactions data integrity, so they cannot be modified 
* TchaîV3: even more secured, we can check if data has been deleted illegally
* TchaîV4: most secured, we cannot insert new transaction inside database without verifying the transaction is legal

## Instructions:

1) Go to the wanted version folder with your terminal.

2) Enter the following command: 
```
 docker run --name myredis -p 6379:6379 redis
 ```

3) Enter the following command:  
```
 docker build . -t back
 docker run --name server -p 5000:5000 back
```
If there is already a docker named myredis or server and you want to delete it, just type the following command: 
```
docker rm [dockername]
```


![Redis](https://img.shields.io/badge/redis-CC0000.svg?&style=for-the-badge&logo=redis&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![Python](https://img.shields.io/badge/a%20CCC%20project-blue)
